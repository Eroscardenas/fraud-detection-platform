import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data import (
    MODEL_RESULTS,
    CONFUSION_MATRICES
)

from config import (
    PURPLE,
    PURPLE_LIGHT,
    VIOLET,
    LAVENDER
)

from components import (
    page_header,
    section,
    explanation_card,
    insight_card,
    style_chart
)


def render():

    page_header(
        "Model Performance",
        "How well does the fraud detector work?",
        (
            "This section explains the model results in plain language, "
            "while keeping the technical metrics visible for deeper analysis."
        )
    )


    # =====================================================
    # DATASET SELECTOR
    # =====================================================

    dataset = st.selectbox(
        "Choose a dataset",
        [
            "ULB",
            "IEEE-CIS"
        ],
        help=(
            "The project contains two separate fraud detection models. "
            "Each dataset has different characteristics and difficulty."
        )
    )


    row = MODEL_RESULTS[
        MODEL_RESULTS["Dataset"] == dataset
    ].iloc[0]


    # =====================================================
    # HUMAN-FRIENDLY METRICS
    # =====================================================

    section(
        "What do the results mean?",
        "Model quality"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Fraud detection rate",
            f'{row["Recall"] * 100:.1f}%'
        )

        st.caption(
            "Technical metric: Recall"
        )

        st.write(
            f"The model detects about "
            f'{row["Recall"] * 100:.0f} out of every 100 '
            "fraudulent transactions."
        )


    with col2:

        st.metric(
            "Alert accuracy",
            f'{row["Precision"] * 100:.1f}%'
        )

        st.caption(
            "Technical metric: Precision"
        )

        st.write(
            f"Of every 100 transactions flagged as fraud, "
            f'about {row["Precision"] * 100:.0f} are actually fraudulent.'
        )


    with col3:

        st.metric(
            "Balance score",
            f'{row["F1"] * 100:.1f}%'
        )

        st.caption(
            "Technical metric: F1 Score"
        )

        st.write(
            "F1 summarizes the balance between detecting fraud "
            "and avoiding unnecessary alerts."
        )


    st.html("<br>")


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Overall separation",
            f'{row["ROC-AUC"] * 100:.1f}%'
        )

        st.caption(
            "Technical metric: ROC-AUC"
        )

        st.write(
            "Measures how well the model separates fraudulent "
            "transactions from legitimate transactions overall."
        )


    with col2:

        st.metric(
            "Fraud-focused performance",
            f'{row["PR-AUC"] * 100:.1f}%'
        )

        st.caption(
            "Technical metric: PR-AUC"
        )

        st.write(
            "Measures how well the model performs specifically "
            "on the rare fraud class, where false alerts matter."
        )


    st.markdown("---")


    # =====================================================
    # SIMPLE METRIC EXPLANATIONS
    # =====================================================

    section(
        "A simple guide to the metrics",
        "No Data Science background needed"
    )


    col1, col2 = st.columns(2)


    with col1:

        explanation_card(
            "Recall — Did we catch the fraud?",
            (
                "Recall answers one simple question: "
                "of all fraud cases that really happened, "
                "how many did the model find?"
            ),
            (
                "Higher recall means fewer fraudulent transactions "
                "escape detection."
            )
        )


    with col2:

        explanation_card(
            "Precision — Can we trust the alerts?",
            (
                "Precision asks: of all transactions flagged as fraud, "
                "how many were actually fraudulent?"
            ),
            (
                "Higher precision means analysts waste less time "
                "reviewing legitimate transactions."
            )
        )


    st.html("<br>")


    col1, col2 = st.columns(2)


    with col1:

        explanation_card(
            "ROC-AUC — Can the model separate fraud from normal activity?",
            (
                "ROC-AUC measures the model's overall ability "
                "to rank fraudulent transactions above legitimate ones."
            ),
            (
                "100% would represent perfect separation. "
                "50% would be similar to random guessing."
            )
        )


    with col2:

        explanation_card(
            "PR-AUC — How strong is the model when fraud is rare?",
            (
                "PR-AUC focuses on the relationship between "
                "finding fraud and avoiding false alerts."
            ),
            (
                "It is especially useful in fraud detection because "
                "fraud usually represents only a small part of all transactions."
            )
        )


    st.html("<br>")


    explanation_card(
        "F1 Score — Is the model balanced?",
        (
            "F1 combines Precision and Recall into one score."
        ),
        (
            "It is useful when we want both good fraud detection "
            "and a reasonable number of false alerts."
        )
    )


    st.markdown("---")


    # =====================================================
    # MODEL COMPARISON
    # =====================================================

    section(
        "How do the two models compare?",
        "ULB vs IEEE-CIS"
    )


    comparison = MODEL_RESULTS[
        [
            "Dataset",
            "ROC-AUC",
            "PR-AUC",
            "Precision",
            "Recall",
            "F1"
        ]
    ].copy()


    chart_data = comparison.melt(
        id_vars="Dataset",
        var_name="Metric",
        value_name="Score"
    )


    metric_labels = {
        "ROC-AUC": "Overall separation",
        "PR-AUC": "Fraud-focused performance",
        "Precision": "Alert accuracy",
        "Recall": "Fraud detection rate",
        "F1": "Balance score"
    }


    chart_data["Metric"] = chart_data[
        "Metric"
    ].map(metric_labels)


    fig = px.bar(
        chart_data,
        x="Metric",
        y="Score",
        color="Dataset",
        barmode="group",
        text="Score",
        color_discrete_sequence=[
            PURPLE,
            PURPLE_LIGHT
        ]
    )


    fig.update_traces(
        texttemplate="%{text:.0%}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Score: %{y:.1%}"
            "<extra></extra>"
        )
    )


    fig.update_yaxes(
        range=[0, 1.05],
        tickformat=".0%",
        title=""
    )


    fig.update_xaxes(
        title=""
    )


    fig.update_layout(
        title="Model performance comparison"
    )


    fig = style_chart(fig)


    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


    st.markdown("---")


    # =====================================================
    # CONFUSION MATRIX
    # =====================================================

    section(
        "What did the model get right and wrong?",
        "Technical name: Confusion Matrix"
    )


    matrix = CONFUSION_MATRICES[
        dataset
    ]


    tn = matrix["true_negative"]
    fp = matrix["false_positive"]
    fn = matrix["false_negative"]
    tp = matrix["true_positive"]


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Fraud correctly detected",
        f"{tp:,}"
    )

    col2.metric(
        "Fraud missed",
        f"{fn:,}"
    )

    col3.metric(
        "Legitimate transactions flagged",
        f"{fp:,}"
    )

    col4.metric(
        "Legitimate transactions approved",
        f"{tn:,}"
    )


    st.html("<br>")


    matrix_df = pd.DataFrame(
        [
            [tn, fp],
            [fn, tp]
        ],
        index=[
            "Actually legitimate",
            "Actually fraud"
        ],
        columns=[
            "Predicted legitimate",
            "Fraud alert"
        ]
    )


    fig_matrix = go.Figure(
        data=go.Heatmap(
            z=matrix_df.values,
            x=matrix_df.columns,
            y=matrix_df.index,
            text=matrix_df.values,
            texttemplate="%{text:,}",
            colorscale=[
                [0.0, "#17121F"],
                [0.5, PURPLE],
                [1.0, LAVENDER]
            ],
            showscale=False,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "%{x}<br>"
                "%{z:,} transactions"
                "<extra></extra>"
            )
        )
    )


    fig_matrix.update_layout(
        title=f"{dataset} classification results"
    )


    fig_matrix = style_chart(
        fig_matrix
    )


    st.plotly_chart(
        fig_matrix,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


    # =====================================================
    # INTERPRETATION
    # =====================================================

    if dataset == "ULB":

        insight_card(
            "Interpretation",
            "The ULB model catches most fraud with relatively few false alerts.",
            (
                "It correctly detected 85 fraud cases and missed 13. "
                "Only 87 legitimate transactions were incorrectly "
                "flagged in the test set."
            )
        )

    else:

        insight_card(
            "Interpretation",
            "IEEE-CIS is a more difficult fraud environment.",
            (
                "The model detected 3,329 fraud cases, but also "
                "generated 9,633 alerts on legitimate transactions. "
                "This shows why threshold selection is important."
            )
        )


    st.markdown("---")


    # =====================================================
    # BUSINESS TAKEAWAY
    # =====================================================

    section(
        "What should a non-technical user remember?",
        "Business takeaway"
    )


    if dataset == "ULB":

        explanation_card(
            "Strong fraud detection with low customer friction",
            (
                "The ULB model identifies approximately 87% of fraud "
                "while generating relatively few false alerts."
            ),
            (
                "In practice, this means the model can detect suspicious "
                "activity without sending too many legitimate transactions "
                "to manual review."
            )
        )

    else:

        explanation_card(
            "Good fraud coverage, but more manual review is required",
            (
                "The IEEE-CIS model detects approximately 81% of fraud, "
                "but its alerts are less precise."
            ),
            (
                "A business using this model would need to decide how much "
                "fraud risk it is willing to accept versus how many legitimate "
                "customers it is willing to review."
            )
        )