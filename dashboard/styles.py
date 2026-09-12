import streamlit as st


def load_styles():

    st.html("""
    <style>

    /* =====================================================
       APP
    ===================================================== */

    .stApp {

        background:

            radial-gradient(
                circle at 15% 0%,
                rgba(109,40,217,.18),
                transparent 30%
            ),

            radial-gradient(
                circle at 90% 20%,
                rgba(168,85,247,.09),
                transparent 25%
            ),

            #07070b;

        color: #f8f7fc;
    }


    .block-container {

        max-width: 1450px;

        padding-top: 3rem;

        padding-bottom: 5rem;
    }


    /* =====================================================
       SIDEBAR
    ===================================================== */

    [data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #0d0b14,
                #07070b
            );

        border-right:
            1px solid rgba(139,92,246,.14);
    }


    .sidebar-brand {

        font-size: 19px;

        font-weight: 800;

        letter-spacing: 2px;

        color: white;
    }


    .sidebar-subtitle {

        color: #756d80;

        font-size: 10px;

        text-transform: uppercase;

        letter-spacing: 1.7px;

        margin-top: 4px;

        margin-bottom: 30px;
    }


    .sidebar-footer {

        color: #625b6d;

        font-size: 10px;

        line-height: 1.9;

        letter-spacing: 1px;
    }


    /* =====================================================
       HERO
    ===================================================== */

    .hero-label {

        color: #a78bfa;

        font-size: 11px;

        font-weight: 700;

        letter-spacing: 2.6px;

        text-transform: uppercase;
    }


    .hero-title {

        font-size: 54px;

        font-weight: 800;

        letter-spacing: -2.8px;

        line-height: 1.04;

        margin-top: 12px;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #ddd6fe,
                #a78bfa
            );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;
    }


    .hero-description {

        max-width: 720px;

        color: #91899f;

        line-height: 1.7;

        margin-top: 17px;

        font-size: 15px;
    }


    /* =====================================================
       TITLES
    ===================================================== */

    .page-label,
    .section-label {

        color: #9b75ff;

        font-size: 10px;

        font-weight: 700;

        letter-spacing: 2.2px;

        text-transform: uppercase;
    }


    .page-title {

        color: white;

        font-size: 39px;

        font-weight: 800;

        letter-spacing: -1.5px;

        margin-top: 7px;
    }


    .page-subtitle {

        color: #8e8799;

        font-size: 15px;

        margin-top: 8px;

        margin-bottom: 32px;
    }


    .section-title {

        color: #f7f5ff;

        font-size: 25px;

        font-weight: 750;

        margin-top: 5px;

        margin-bottom: 20px;
    }


    /* =====================================================
       METRICS
    ===================================================== */

    [data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(25,21,36,.96),
                rgba(13,12,20,.96)
            );

        border:
            1px solid rgba(167,139,250,.14);

        border-radius: 17px;

        padding: 20px;

        box-shadow:
            0 15px 40px rgba(0,0,0,.18);
    }


    [data-testid="stMetricLabel"] {

        color: #8d8599;

        font-size: 11px;

        text-transform: uppercase;

        letter-spacing: 1px;
    }


    [data-testid="stMetricValue"] {

        color: #f7f3ff;

        font-size: 29px;

        font-weight: 750;
    }


    /* =====================================================
       CARDS
    ===================================================== */

    .info-card,
    .insight-card,
    .explanation-card {

        padding: 27px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(26,21,38,.94),
                rgba(12,11,18,.96)
            );

        border:
            1px solid rgba(139,92,246,.16);

        box-shadow:
            0 18px 50px rgba(0,0,0,.15);
    }


    .card-label {

        color: #a78bfa;

        font-size: 10px;

        font-weight: 700;

        letter-spacing: 2px;

        text-transform: uppercase;
    }


    .insight-title,
    .explanation-title {

        color: white;

        font-size: 20px;

        font-weight: 730;

        margin-top: 8px;
    }


    .insight-text,
    .explanation-text {

        color: #91899e;

        font-size: 13px;

        line-height: 1.7;

        margin-top: 8px;
    }


    .explanation-example {

        color: #c4b5fd;

        background:
            rgba(139,92,246,.08);

        border:
            1px solid rgba(139,92,246,.12);

        padding: 12px 15px;

        border-radius: 10px;

        margin-top: 15px;

        font-size: 12px;
    }


    /* =====================================================
       RISK PANEL
    ===================================================== */

    .risk-panel {

        background:

            radial-gradient(
                circle at 90% 10%,
                rgba(139,92,246,.15),
                transparent 30%
            ),

            linear-gradient(
                145deg,
                rgba(30,23,44,.96),
                rgba(12,10,18,.97)
            );

        border:
            1px solid rgba(168,85,247,.22);

        border-radius: 22px;

        padding: 32px;

        margin-top: 20px;
    }


    .risk-small {

        color: #a78bfa;

        font-size: 10px;

        font-weight: 700;

        letter-spacing: 2px;

        text-transform: uppercase;
    }


    .risk-title {

        color: white;

        font-size: 44px;

        font-weight: 800;

        margin-top: 6px;
    }


    .risk-score {

        color: #c4b5fd;

        font-size: 20px;

        margin-top: 10px;
    }


    .risk-text {

        color: #91899e;

        font-size: 13px;

        line-height: 1.7;

        margin-top: 12px;
    }


    /* =====================================================
       CLEANUP
    ===================================================== */

    hr {

        border: none !important;

        border-top:
            1px solid rgba(168,85,247,.10)
            !important;

        margin:
            38px 0 !important;
    }


    #MainMenu {
        visibility: hidden;
    }


    footer {
        visibility: hidden;
    }


    header {
        background: transparent !important;
    }

    </style>
    """)