import streamlit as st

from textwrap import dedent

from config import (
    TEXT,
    WHITE,
    BACKGROUND,
    GRID
)


# =========================================================
# HTML
# =========================================================

def html(content):

    st.html(
        dedent(content).strip()
    )


# =========================================================
# PAGE HEADER
# =========================================================

def page_header(label, title, subtitle):

    html(f"""
    <div class="page-label">
        {label}
    </div>

    <div class="page-title">
        {title}
    </div>

    <div class="page-subtitle">
        {subtitle}
    </div>
    """)


# =========================================================
# SECTION
# =========================================================

def section(title, label=None):

    if label:

        html(f"""
        <div class="section-label">
            {label}
        </div>

        <div class="section-title">
            {title}
        </div>
        """)

    else:

        html(f"""
        <div class="section-title">
            {title}
        </div>
        """)


# =========================================================
# EXPLANATION CARD
# =========================================================

def explanation_card(title, description, example=None):

    example_html = ""

    if example:

        example_html = f"""
        <div class="explanation-example">
            {example}
        </div>
        """

    html(f"""
    <div class="explanation-card">

        <div class="explanation-title">
            {title}
        </div>

        <div class="explanation-text">
            {description}
        </div>

        {example_html}

    </div>
    """)


# =========================================================
# INSIGHT CARD
# =========================================================

def insight_card(label, title, text):

    html(f"""
    <div class="insight-card">

        <div class="card-label">
            {label}
        </div>

        <div class="insight-title">
            {title}
        </div>

        <div class="insight-text">
            {text}
        </div>

    </div>
    """)


# =========================================================
# PLOTLY STYLE
# =========================================================

def style_chart(fig):

    fig.update_layout(

        paper_bgcolor=BACKGROUND,

        plot_bgcolor=BACKGROUND,

        font=dict(
            color=TEXT
        ),

        title=dict(
            font=dict(
                color=WHITE,
                size=19
            )
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    fig.update_xaxes(
        gridcolor=GRID,
        zerolinecolor=GRID
    )

    fig.update_yaxes(
        gridcolor=GRID,
        zerolinecolor=GRID
    )

    return fig