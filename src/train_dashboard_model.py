import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, average_precision_score

from xgboost import XGBClassifier


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "ieee_processed.parquet"

MODEL_PATH = BASE_DIR / "models" / "dashboard_risk_model.pkl"


# =========================================================
# LOAD DATA
# =========================================================

print("Loading IEEE processed dataset...")

df = pd.read_parquet(DATA_PATH)

print("Dataset loaded:", df.shape)


# =========================================================
# FEATURES FOR INTERACTIVE DASHBOARD
# =========================================================

features = [
    "TransactionAmt",
    "ProductCD",
    "card4",
    "card6",
    "P_emaildomain"
]

target = "isFraud"


# Keep only columns that exist
available_features = [
    col for col in features
    if col in df.columns
]

print("Available features:", available_features)


X = df[available_features].copy()

y = df[target].copy()


# =========================================================
# FEATURE TYPES
# =========================================================

numeric_features = [
    "TransactionAmt"
]

categorical_features = [
    col for col in available_features
    if col not in numeric_features
]


# =========================================================
# PREPROCESSING
# =========================================================

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ]
)


categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),

        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_features
        ),

        (
            "categorical",
            categorical_pipeline,
            categorical_features
        )
    ]
)


# =========================================================
# MODEL
# =========================================================

fraud_count = y.sum()

normal_count = len(y) - fraud_count

scale_pos_weight = (
    normal_count / fraud_count
)


model = XGBClassifier(
    n_estimators=250,
    max_depth=5,
    learning_rate=0.05,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    eval_metric="logloss"
)


# =========================================================
# COMPLETE PIPELINE
# =========================================================

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            model
        )
    ]
)


# =========================================================
# TRAIN / TEST
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("Training dashboard model...")

pipeline.fit(
    X_train,
    y_train
)


# =========================================================
# EVALUATION
# =========================================================

probabilities = pipeline.predict_proba(
    X_test
)[:, 1]


roc_auc = roc_auc_score(
    y_test,
    probabilities
)


pr_auc = average_precision_score(
    y_test,
    probabilities
)


print()
print("Dashboard model results")
print("-----------------------")
print(f"ROC-AUC: {roc_auc:.4f}")
print(f"PR-AUC:  {pr_auc:.4f}")


# =========================================================
# SAVE MODEL
# =========================================================

joblib.dump(
    pipeline,
    MODEL_PATH
)


print()
print("Model saved to:")
print(MODEL_PATH)