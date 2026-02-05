# app/ml/offline/offline_evaluation.py

import pandas as pd
import joblib
import json
from pathlib import Path
from sklearn.metrics import precision_score, recall_score, roc_auc_score, confusion_matrix

# ---------------- PATHS ----------------

ARTIFACT_DIR = Path("app/ml/artifacts")
OFFLINE_DIR = Path("app/ml/offline")

DATASET_PATH = OFFLINE_DIR / "paysim_test_v2.csv"
LABELS_PATH  = OFFLINE_DIR / "paysim_test_labels_v2.csv"
CACHE_PATH   = OFFLINE_DIR / "offline_metrics.json"

MODEL_PATH = ARTIFACT_DIR / "logreg_model.joblib"
SCALER_PATH = ARTIFACT_DIR / "scaler.joblib"
FEATURE_NAMES_PATH = ARTIFACT_DIR / "feature_names.joblib"

# CURRENT OPERATING POINT
OPERATING_THRESHOLD = 0.20

# Reference (comparison only)
REFERENCE_THRESHOLD = 0.50


         
# PUBLIC API: LOAD CACHED METRICS (FAST, SAFE)
         

def load_cached_offline_metrics():
    """
    Used by API / UI.
    NEVER computes metrics.
    """
    if not CACHE_PATH.exists():
        return {
            "status": "missing",
            "message": "Offline metrics not computed yet. Run offline_evaluation.py manually."
        }

    with open(CACHE_PATH, "r") as f:
        return json.load(f)


         
# OFFLINE COMPUTATION (CLI ONLY)
         

def compute_and_cache_offline_metrics():
    """
    Heavy offline evaluation.
    MUST NOT be called from API.
    """
    print("🚀 Running OFFLINE evaluation (Labeled Test Set)")

    # 1. Load artifacts
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_names = joblib.load(FEATURE_NAMES_PATH)

    # 2. Load test data
    X_df = pd.read_csv(DATASET_PATH)
    y = pd.read_csv(LABELS_PATH).iloc[:, 0].values

    X = X_df[feature_names].values

    # 3. Scale
    X_scaled = scaler.transform(X)

    # 4. Predict probabilities
    y_prob = model.predict_proba(X_scaled)[:, 1]

    # -------- Reference threshold --------
    y_pred_ref = (y_prob >= REFERENCE_THRESHOLD).astype(int)

    reference = {
        "threshold": REFERENCE_THRESHOLD,
        "precision": round(precision_score(y, y_pred_ref), 4),
        "recall": round(recall_score(y, y_pred_ref), 4),
        "confusion_matrix": confusion_matrix(y, y_pred_ref).tolist(),
    }

    # -------- Operating threshold --------
    y_pred_op = (y_prob >= OPERATING_THRESHOLD).astype(int)

    operating = {
        "threshold": OPERATING_THRESHOLD,
        "precision": round(precision_score(y, y_pred_op), 4),
        "recall": round(recall_score(y, y_pred_op), 4),
        "confusion_matrix": confusion_matrix(y, y_pred_op).tolist(),
    }

    metrics = {
        "model": "Logistic Regression",
        "evaluation_type": "Offline (Labeled Test Set)",
        "samples": int(len(y)),
        "features_used": len(feature_names),
        "roc_auc": round(roc_auc_score(y, y_prob), 4),
        "reference": reference,
        "operating": operating,
    }

    # Cache
    with open(CACHE_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    # -------- Terminal output --------
    print("\n================ OFFLINE MODEL EVALUATION ================\n")
    print(f"Samples evaluated     : {metrics['samples']}")
    print(f"ROC-AUC               : {metrics['roc_auc']}")
    print(f"Features used         : {metrics['features_used']}")

    print(f"\n--- Reference @ {REFERENCE_THRESHOLD:.2f} ---")
    print(f"Precision             : {reference['precision']}")
    print(f"Recall                : {reference['recall']}")
    print(f"Confusion Matrix      : {reference['confusion_matrix']}")

    print(f"\n--- Operating @ {OPERATING_THRESHOLD:.2f} ---")
    print(f"Precision             : {operating['precision']}")
    print(f"Recall                : {operating['recall']}")
    print(f"Confusion Matrix      : {operating['confusion_matrix']}")

    print("\n==========================================================\n")
    print("Offline metrics cached at:", CACHE_PATH)

    return metrics


         
# ENTRY POINT (CLI ONLY)
         

if __name__ == "__main__":
    compute_and_cache_offline_metrics()