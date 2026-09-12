import streamlit as st
import pandas as pd
import plotly.express as px

from data import (
    THRESHOLD_IEEE,
    THRESHOLD_ULB
)

from config import (
    PURPLE,
    PURPLE_LIGHT,
    VIOLET
)

from components import (
    page_header,
    section,
    insight_card,
    explanation_card,
    style_chart
)


def render():

    page_header(
        "Fraud Detection Strategy",
        "How strict should the fraud system be?",
        (
            "A stricter system can catch more fraud, "
            "but it may also interrupt more legitimate customers."
        )
    )


    # =====================================================
    # DATASET
    # =====================================================

    dataset = st.selectbox(
        "Analysis dataset",
        [
            "IEEE-CIS",
            "ULB Credit Card Fraud"
        ],
        help=(
            "Select which fraud experiment you want "
            "to analyze."
        )
    )


    if dataset == "IEEE-CIS":

        data = THRESHOLD_IEEE

    else:

        data = THRESHOLD_ULB


    # =====================================================
    # FRIENDLY BUSINESS POLICY
    # =====================================================

    policy_options = {

        "High fraud protection": 0.30,

        "Balanced protection": 0.50,

        "Lower customer friction": 0.70
    }


    policy = st.selectbox(
        "Detection strategy",
        list(policy_options.keys()),
        help=(
            "Choose how aggressive the system should be "
            "when deciding whether a transaction is suspicious."
        )
    )


    threshold = policy_options[
        policy
    ]


    selected = data[
        data["Threshold"] == threshold
    ].iloc[0]


    # =====================================================
    # POLICY EXPLANATION
    # =====================================================

    if policy == "High fraud protection":

        description = (
            "The system reacts to lower levels of fraud risk. "
            "This catches more fraudulent transactions, but also "
            "creates more alerts for legitimate customers."
        )


    elif policy == "Balanced protection":

        description = (
            "The system tries to balance fraud prevention "
            "with customer experience."
        )


    else:

        description = (
            "The system requires stronger evidence before flagging "
            "a transaction. This reduces customer interruptions, "
            "but more fraud may go undetected."
        )


    insight_card(
        "Selected strategy",
        policy,
        description
    )


    st.html("<br>")


    # =====================================================
    # RESULTS
    # =====================================================

    section(
        "What happens with this strategy?",
        "Business impact"
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Fraud detected",
        f'{int(selected["Frauds Detected"]):,}'
    )


    col2.metric(
        "Fraud missed",
        f'{int(selected["Frauds Missed"]):,}'
    )


    col3.metric(
        "Legitimate transactions flagged",
        f'{int(selected["False Positives"]):,}'
    )


    st.caption(
        f"Technical classification threshold: {threshold:.2f}"
    )


    st.markdown("---")


    # =====================================================
    # HUMAN-FRIENDLY COMPARISON
    # =====================================================

    section(
        "Compare the three strategies",
        "Trade-off"
    )


    comparison = data.copy()


    comparison["Strategy"] = [
        "High fraud protection",
        "Balanced protection",
        "Lower customer friction"
    ]


    comparison = comparison[
        [
            "Strategy",
            "Frauds Detected",
            "Frauds Missed",
            "False Positives"
        ]
    ]


    comparison = comparison.rename(
        columns={
            "Frauds Detected":
                "Fraud detected",

            "Frauds Missed":
                "Fraud missed",

            "False Positives":
                "Legitimate transactions flagged"
        }
    )


    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )


    st.html("<br>")


    # =====================================================
    # GRAPH
    # =====================================================

    chart_data = comparison.melt(

        id_vars="Strategy",

        value_vars=[
            "Fraud detected",
            "Fraud missed",
            "Legitimate transactions flagged"
        ],

        var_name="Outcome",

        value_name="Transactions"
    )


    fig = px.bar(

        chart_data,

        x="Strategy",

        y="Transactions",

        color="Outcome",

        barmode="group",

        color_discrete_sequence=[
            PURPLE,
            VIOLET,
            PURPLE_LIGHT
        ],

        title=(
            "Business impact of each fraud strategy"
        )
    )


    fig = style_chart(
        fig
    )


    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


    # =====================================================
    # SIMPLE EXPLANATION
    # =====================================================

    st.html("<br>")


    explanation_card(
        "What is a threshold?",
        (
            "The fraud model produces a probability between 0% and 100%. "
            "The threshold is the point at which the company decides "
            "that a transaction should be treated as suspicious."
        ),
        (
            "Example: with a 30% threshold, a transaction with 35% "
            "estimated fraud probability would already trigger an alert. "
            "With a 70% threshold, the same transaction would not."
        )
    )


    st.html("<br>")