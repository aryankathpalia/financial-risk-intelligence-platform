# app/ml/offline/offline_evaluation_online.py

import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import precision_score, recall_score, roc_auc_score, confusion_matrix

ARTIFACT_DIR = Path("app/ml/artifacts")
OFFLINE_DIR = Path("app/ml/offline")

DATASET_PATH = OFFLINE_DIR / "paysim_test_v2.csv"
LABELS_PATH = OFFLINE_DIR / "paysim_test_labels_v2.csv"

MODEL_PATH = ARTIFACT_DIR / "logreg_model_online.joblib"
SCALER_PATH = ARTIFACT_DIR / "scaler_online.joblib"
FEATURE_NAMES_PATH = ARTIFACT_DIR / "feature_names_online.joblib"

OPERATING_THRESHOLD = 0.20
REFERENCE_THRESHOLD = 0.50


def compute_and_cache_offline_online_metrics():
    print("Running OFFLINE evaluation (ONLINE MODEL, 10 features)")

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_names = joblib.load(FEATURE_NAMES_PATH)

    print(f"Features used ({len(feature_names)}): {feature_names}")

    X_df = pd.read_csv(DATASET_PATH)
    labels_df = pd.read_csv(LABELS_PATH)

    # FIX IS HERE
    y = labels_df["label"].values.astype(int)

    X = X_df[feature_names]
    X_scaled = scaler.transform(X)

    y_prob = model.predict_proba(X_scaled)[:, 1]

    y_pred_ref = (y_prob >= REFERENCE_THRESHOLD).astype(int)
    y_pred_op = (y_prob >= OPERATING_THRESHOLD).astype(int)

    print("\n================ ONLINE MODEL EVALUATION ================\n")
    print(f"Samples evaluated : {len(y)}")
    print(f"ROC-AUC           : {roc_auc_score(y, y_prob):.4f}")

    print(f"\n--- Reference @ {REFERENCE_THRESHOLD:.2f} ---")
    print("Precision:", precision_score(y, y_pred_ref, zero_division=0))
    print("Recall   :", recall_score(y, y_pred_ref, zero_division=0))
    print("CM       :", confusion_matrix(y, y_pred_ref).tolist())

    print(f"\n--- Operating @ {OPERATING_THRESHOLD:.2f} ---")
    print("Precision:", precision_score(y, y_pred_op, zero_division=0))
    print("Recall   :", recall_score(y, y_pred_op, zero_division=0))
    print("CM       :", confusion_matrix(y, y_pred_op).tolist())


if __name__ == "__main__":
    compute_and_cache_offline_online_metrics()