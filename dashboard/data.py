import pandas as pd


# =========================================================
# MODEL RESULTS
# =========================================================

MODEL_RESULTS = pd.DataFrame({
    "Dataset": [
        "ULB",
        "IEEE-CIS"
    ],

    "ROC-AUC": [
        0.9847,
        0.9364
    ],

    "PR-AUC": [
        0.8464,
        0.6721
    ],

    "Precision": [
        0.49,
        0.26
    ],

    "Recall": [
        0.87,
        0.81
    ],

    "F1": [
        0.63,
        0.39
    ],

    "Fraud Rate (%)": [
        0.17,
        3.50
    ],

    "Transactions": [
        284807,
        590540
    ]
})


# =========================================================
# DATASET INFORMATION
# =========================================================

DATASETS = {

    "ULB": {
        "name": "ULB Credit Card Fraud",
        "transactions": 284807,
        "fraud_cases": 492,
        "normal_cases": 284315,
        "fraud_rate": 0.17,
        "features": 30,

        "description": (
            "Credit card transaction dataset with anonymized "
            "numerical variables and extreme class imbalance."
        )
    },

    "IEEE-CIS": {
        "name": "IEEE-CIS Fraud Detection",
        "transactions": 590540,
        "fraud_cases": 20663,
        "normal_cases": 569877,
        "fraud_rate": 3.50,
        "features": 434,

        "description": (
            "Large fraud dataset containing transaction, "
            "identity, categorical and behavioral information."
        )
    }
}


# =========================================================
# CONFUSION MATRICES
# =========================================================

CONFUSION_MATRICES = {

    "ULB": {
        "true_negative": 56777,
        "false_positive": 87,
        "false_negative": 13,
        "true_positive": 85
    },

    "IEEE-CIS": {
        "true_negative": 104342,
        "false_positive": 9633,
        "false_negative": 804,
        "true_positive": 3329
    }
}


# =========================================================
# THRESHOLD RESULTS
# =========================================================

THRESHOLD_IEEE = pd.DataFrame({
    "Threshold": [
        0.30,
        0.50,
        0.70
    ],

    "Frauds Detected": [
        3702,
        3329,
        2866
    ],

    "Frauds Missed": [
        431,
        804,
        1267
    ],

    "False Positives": [
        23940,
        9633,
        3112
    ]
})


THRESHOLD_ULB = pd.DataFrame({
    "Threshold": [
        0.30,
        0.50,
        0.70
    ],

    "Frauds Detected": [
        85,
        85,
        83
    ],

    "Frauds Missed": [
        13,
        13,
        15
    ],

    "False Positives": [
        184,
        87,
        47
    ]
})


# =========================================================
# TRANSACTION CATEGORY FRAUD RATES
# IEEE-CIS
# =========================================================

PRODUCT_FRAUD_RATES = {
    "W": 2.04,
    "C": 11.69,
    "R": 3.78,
    "H": 4.77,
    "S": 5.90
}