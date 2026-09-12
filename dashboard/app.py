import streamlit as st

from styles import load_styles

from components import html

from views.overview import render as overview
from views.model_comparison import render as model_comparison
from views.risk_simulator import render as risk_simulator
from views.threshold_analysis import render as threshold_analysis

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Fraud Detection Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# STYLES
# =========================================================

load_styles()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    html("""
    <div class="sidebar-brand">
        FRAUD DETECTION
    </div>

    <div class="sidebar-subtitle">
        Intelligence Platform
    </div>
    """)


    page = st.radio(

        "Navigation",

        [
            "Overview",
            "Model Performance",
            "Decision Simulator",
            "Threshold Analysis"
        ],

        label_visibility="collapsed"
    )


    st.markdown("---")


    html("""
    <div class="sidebar-footer">
        MULTI-DATASET ML SYSTEM<br>
        XGBOOST · MLFLOW<br>
        ULB · IEEE-CIS
    </div>
    """)


# =========================================================
# ROUTER
# =========================================================

if page == "Overview":

    overview()


elif page == "Model Performance":

    model_comparison()


elif page == "Decision Simulator":

    risk_simulator()


elif page == "Threshold Analysis":

    threshold_analysis()