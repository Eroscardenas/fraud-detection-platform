import streamlit as st
import pandas as pd
import joblib

from pathlib import Path

from components import (
    html,
    page_header,
    section,
    explanation_card
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "dashboard_risk_model.pkl"
)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    return joblib.load(
        MODEL_PATH
    )


model = load_model()


# =========================================================
# PAGE
# =========================================================

def render():

    page_header(
        "Transaction Risk",
        "Is this transaction suspicious?",
        (
            "Enter basic transaction information. "
            "The system will compare it with historical fraud patterns "
            "and estimate its level of risk."
        )
    )


    st.info(
        "This tool uses a simplified XGBoost fraud model trained "
        "with real IEEE-CIS transaction data."
    )


    # =====================================================
    # TRANSACTION FORM
    # =====================================================

    section(
        "Tell us about the transaction",
        "Step 1"
    )


    st.caption(
        "You do not need technical knowledge. "
        "Enter the information available for the transaction below."
    )


    with st.form("fraud_form"):

        col1, col2 = st.columns(2)


        # -------------------------------------------------
        # AMOUNT
        # -------------------------------------------------

        with col1:

            transaction_amount = st.number_input(
                "Transaction amount",
                min_value=0.0,
                value=150.0,
                step=10.0,
                help="Total amount charged in the transaction."
            )


        # -------------------------------------------------
        # PRODUCT CATEGORY
        # -------------------------------------------------

        with col2:

            product_options = {
                "Lower historical fraud rate — 2.0%": "W",
                "Highest historical fraud rate — 11.7%": "C",
                "Moderate historical fraud rate — 3.8%": "R",
                "Moderate historical fraud rate — 4.8%": "H",
                "Elevated historical fraud rate — 5.9%": "S"
            }

            product_label = st.selectbox(
                "Transaction category",
                list(product_options.keys()),
                help=(
                    "The original IEEE-CIS dataset anonymizes the exact "
                    "commercial category. The percentage shown represents "
                    "the historical fraud rate observed for that category."
                )
            )

            product_cd = product_options[
                product_label
            ]


        # -------------------------------------------------
        # CARD NETWORK
        # -------------------------------------------------

        with col1:

            card4 = st.selectbox(
                "Card network",
                [
                    "visa",
                    "mastercard",
                    "american express",
                    "discover"
                ],
                help="Payment network associated with the card."
            )


        # -------------------------------------------------
        # CARD TYPE
        # -------------------------------------------------

        with col2:

            card6 = st.selectbox(
                "Card funding type",
                [
                    "debit",
                    "credit"
                ],
                help=(
                    "Indicates whether the transaction was made "
                    "using a debit or credit card."
                )
            )


        # -------------------------------------------------
        # EMAIL
        # -------------------------------------------------

        email_domain = st.selectbox(
            "Customer email provider",
            [
                "gmail.com",
                "yahoo.com",
                "hotmail.com",
                "anonymous.com",
                "aol.com",
                "icloud.com",
                "outlook.com"
            ],
            help=(
                "Email provider associated with the transaction. "
                "Historical fraud patterns can differ between providers."
            )
        )


        st.caption(
            "Transaction categories are anonymized by the original dataset. "
            "Their exact commercial meaning is not publicly defined."
        )


        submitted = st.form_submit_button(
            "Analyze transaction",
            use_container_width=True
        )


    # =====================================================
    # PREDICTION
    # =====================================================

    if submitted:

        transaction = pd.DataFrame({

            "TransactionAmt": [
                transaction_amount
            ],

            "ProductCD": [
                product_cd
            ],

            "card4": [
                card4
            ],

            "card6": [
                card6
            ],

            "P_emaildomain": [
                email_domain
            ]
        })


        probability = model.predict_proba(
            transaction
        )[0][1]


        risk_percent = (
            probability * 100
        )


        # =================================================
        # BUSINESS INTERPRETATION
        # =================================================

        if probability < 0.30:

            risk_level = "LOW"

            action = (
                "Approve normally"
            )

            explanation = (
                "The model found relatively little similarity "
                "with historical fraud patterns."
            )


        elif probability < 0.70:

            risk_level = "MEDIUM"

            action = (
                "Verify before approval"
            )

            explanation = (
                "The transaction contains some characteristics "
                "that have appeared more frequently in historical "
                "fraud cases."
            )


        else:

            risk_level = "HIGH"

            action = (
                "Send to manual review"
            )

            explanation = (
                "The transaction shows a stronger similarity "
                "to patterns that were historically associated "
                "with fraudulent activity."
            )


        # =================================================
        # RESULT
        # =================================================

        st.markdown("---")


        section(
            "Transaction assessment",
            "Step 2"
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Estimated fraud risk",
            f"{risk_percent:.1f}%"
        )


        col2.metric(
            "Risk level",
            risk_level
        )


        col3.metric(
            "Recommended action",
            action
        )


        st.html("<br>")


        # =================================================
        # FRIENDLY RESULT CARD
        # =================================================

        html(f"""
        <div class="risk-panel">

            <div class="risk-small">
                TRANSACTION ANALYSIS
            </div>

            <div class="risk-title">
                {risk_percent:.1f}% FRAUD RISK
            </div>

            <div class="risk-score">
                Risk level: {risk_level}
            </div>

            <div class="risk-text">

                <strong>
                    Recommended action
                </strong>

                <br>

                {action}

                <br><br>

                <strong>
                    What does this mean?
                </strong>

                <br>

                {explanation}

                <br><br>

                This score is a decision-support signal.
                It does not prove that a transaction is fraudulent.

            </div>

        </div>
        """)


        st.html("<br>")


        # =================================================
        # RISK SCALE
        # =================================================

        section(
            "How to read the score",
            "Risk guide"
        )


        risk_guide = pd.DataFrame({

            "Fraud probability": [
                "0% – 29%",
                "30% – 69%",
                "70% – 100%"
            ],

            "Meaning": [
                "Low risk",
                "Needs verification",
                "High risk"
            ],

            "Suggested action": [
                "Approve normally",
                "Verify before approval",
                "Manual review"
            ]
        })


        st.dataframe(
            risk_guide,
            use_container_width=True,
            hide_index=True
        )


        st.html("<br>")


        # =================================================
        # TRANSACTION SUMMARY
        # =================================================

        section(
            "What was analyzed?",
            "Transaction summary"
        )


        summary = pd.DataFrame({

            "Information": [
                "Transaction amount",
                "Transaction category",
                "Card network",
                "Card funding type",
                "Email provider"
            ],

            "Value": [
                f"${transaction_amount:,.2f}",
                product_label,
                card4.title(),
                card6.title(),
                email_domain
            ]
        })


        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )


        st.html("<br>")
