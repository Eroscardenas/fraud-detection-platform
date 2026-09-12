import streamlit as st
import pandas as pd
import plotly.express as px

from components import (
    html,
    explanation_card,
    insight_card,
    section,
    style_chart
)

from data import DATASETS

from config import (
    PURPLE,
    PURPLE_LIGHT,
    VIOLET,
    LAVENDER
)


def render():

    # =====================================================
    # HERO
    # =====================================================

    html("""
    <div class="hero-label">
        FRAUD ANALYTICS
    </div>

    <div class="hero-title">
        Understand fraud.<br>
        Make better decisions.
    </div>

    <div class="hero-description">
        Explore two real fraud detection datasets, understand
        how rare fraudulent transactions are, and see how
        machine learning can support risk-based decisions.
    </div>
    """)

    st.html("<br>")


    # =====================================================
    # DATA
    # =====================================================

    ulb = DATASETS["ULB"]
    ieee = DATASETS["IEEE-CIS"]

    total_transactions = (
        ulb["transactions"]
        + ieee["transactions"]
    )

    total_fraud = (
        ulb["fraud_cases"]
        + ieee["fraud_cases"]
    )


    # =====================================================
    # KPIs
    # =====================================================

    section(
        "Platform snapshot",
        "Overview"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Transactions analyzed",
        f"{total_transactions:,}"
    )

    col2.metric(
        "Fraud cases",
        f"{total_fraud:,}"
    )

    col3.metric(
        "Datasets",
        "2"
    )

    col4.metric(
        "ML models",
        "2 XGBoost"
    )

    st.caption(
        "The two datasets are modeled separately because "
        "they contain different variables and represent "
        "different fraud detection environments."
    )

    st.markdown("---")


    # =====================================================
    # WHY FRAUD DETECTION IS DIFFICULT
    # =====================================================

    section(
        "Why is fraud detection difficult?",
        "The problem"
    )

    col1, col2 = st.columns(
        [1.15, 0.85]
    )


    # =====================================================
    # DONUT
    # =====================================================

    with col1:

        dataset_choice = st.selectbox(
            "Dataset",
            [
                "IEEE-CIS",
                "ULB"
            ],
            key="overview_dataset"
        )

        selected = DATASETS[
            dataset_choice
        ]

        distribution = pd.DataFrame({
            "Transaction type": [
                "Legitimate",
                "Fraud"
            ],

            "Transactions": [
                selected["normal_cases"],
                selected["fraud_cases"]
            ]
        })

        fig = px.pie(
            distribution,
            names="Transaction type",
            values="Transactions",
            hole=0.68,
            color="Transaction type",
            color_discrete_map={
                "Legitimate": PURPLE,
                "Fraud": LAVENDER
            }
        )

        fig.update_traces(
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "%{value:,} transactions<br>"
                "%{percent}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            title=(
                f"{dataset_choice} transaction distribution"
            )
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


    # =====================================================
    # EXPLANATION
    # =====================================================

    with col2:

        st.html("<br><br>")

        explanation_card(
            "Fraud is rare",
            (
                f"In {dataset_choice}, only "
                f'{selected["fraud_rate"]:.2f}% '
                "of transactions are fraudulent."
            ),
            (
                f'Out of {selected["transactions"]:,} transactions, '
                f'only {selected["fraud_cases"]:,} are fraud cases.'
            )
        )

        st.html("<br>")

        explanation_card(
            "Why accuracy can be misleading",
            (
                "When almost every transaction is legitimate, "
                "a model could achieve very high accuracy simply "
                "by predicting most transactions as normal."
            ),
            (
                "That is why this project also evaluates Recall, "
                "Precision, F1, ROC-AUC and PR-AUC."
            )
        )


    st.markdown("---")


    # =====================================================
    # FRAUD RATE COMPARISON
    # =====================================================

    section(
        "The datasets behave very differently",
        "Fraud prevalence"
    )

    fraud_rates = pd.DataFrame({
        "Dataset": [
            "ULB",
            "IEEE-CIS"
        ],

        "Fraud rate": [
            ulb["fraud_rate"],
            ieee["fraud_rate"]
        ]
    })

    fig = px.bar(
        fraud_rates,
        x="Dataset",
        y="Fraud rate",
        text="Fraud rate",
        color="Dataset",
        color_discrete_sequence=[
            PURPLE_LIGHT,
            PURPLE
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Fraud rate: %{y:.2f}%"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        title="Fraud rate by dataset",
        showlegend=False
    )

    fig.update_yaxes(
        title="Fraudulent transactions (%)"
    )

    fig.update_xaxes(
        title=""
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


    insight_card(
        "Why this matters",
        "One fraud strategy does not fit every dataset.",
        (
            "ULB contains extremely rare fraud, while IEEE-CIS "
            "contains a larger and more complex fraud population. "
            "This is why the models are trained and evaluated "
            "separately instead of combining both datasets."
        )
    )


    st.markdown("---")


    # =====================================================
    # PLATFORM FLOW
    # =====================================================

    section(
        "How does the platform work?",
        "From data to decision"
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        explanation_card(
            "1. Analyze",
            (
                "Historical transactions are explored and prepared "
                "to understand normal behavior, fraud patterns "
                "and class imbalance."
            )
        )


    with col2:

        explanation_card(
            "2. Detect",
            (
                "XGBoost models learn patterns associated with "
                "fraud and estimate the probability that a "
                "transaction is suspicious."
            )
        )


    with col3:

        explanation_card(
            "3. Decide",
            (
                "Model probabilities are translated into practical "
                "actions such as approve, verify or manually "
                "review a transaction."
            )
        )


    st.markdown("---")


    # =====================================================
    # DATASET CARDS
    # =====================================================

    section(
        "Two fraud detection environments",
        "Datasets"
    )

    col1, col2 = st.columns(2)


    with col1:

        html(f"""
        <div class="info-card">

            <div class="card-label">
                ULB CREDIT CARD FRAUD
            </div>

            <div class="insight-title">
                Extreme class imbalance
            </div>

            <div class="insight-text">
                Fraud represents only
                {ulb["fraud_rate"]:.2f}% of transactions,
                making fraudulent behavior extremely rare.
            </div>

            <div class="explanation-example">
                {ulb["transactions"]:,} transactions ·
                {ulb["fraud_cases"]:,} fraud cases ·
                {ulb["features"]} features
            </div>

        </div>
        """)


    with col2:

        html(f"""
        <div class="info-card">

            <div class="card-label">
                IEEE-CIS FRAUD DETECTION
            </div>

            <div class="insight-title">
                Higher dimensional complexity
            </div>

            <div class="insight-text">
                IEEE-CIS combines transaction and identity
                information with hundreds of variables and
                substantial missing data.
            </div>

            <div class="explanation-example">
                {ieee["transactions"]:,} transactions ·
                {ieee["fraud_cases"]:,} fraud cases ·
                {ieee["features"]} original features
            </div>

        </div>
        """)