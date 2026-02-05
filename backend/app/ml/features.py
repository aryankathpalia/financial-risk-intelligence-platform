from pathlib import Path
import pandas as pd
import joblib
import numpy as np


# Artifact paths
ML_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = ML_DIR / "ieee" / "artifacts"

import os

FEATURES_PATH = ARTIFACT_DIR / os.getenv(
    "FEATURES_PATH",
    "ieee/artifacts/features_lgbm.joblib",
)



if not FEATURES_PATH.exists():
    raise FileNotFoundError(f"Missing features file: {FEATURES_PATH}")

FEATURE_COLUMNS = joblib.load(FEATURES_PATH)



# Feature builder (INFERENCE-SAFE)
def build_features(tx):
    """
    Build IEEE features EXACTLY matching training contract.
    - No feature creation
    - No category learning
    - Strict numeric coercion (LightGBM-safe)
    """

    row = {
        "TransactionAmt": tx.TransactionAmt,
        "ProductCD": tx.ProductCD,
        "card1": tx.card1,
        "addr1": tx.addr1,
        "C1": tx.C1,
        "C2": tx.C2,
        "D1": tx.D1,
        "DeviceType": tx.DeviceType,
        "DeviceInfo": tx.DeviceInfo,
    }

    for i in range(1, 39):
        key = f"id_{i:02d}"
        row[key] = getattr(tx, key)

    # Single-row DataFrame
    df = pd.DataFrame([row])

    # Sanitize column names (must match training)
    df.columns = df.columns.str.replace(
        r"[^A-Za-z0-9_]", "_", regex=True
    )

    # Align to training feature contract
    X = df.reindex(columns=FEATURE_COLUMNS, fill_value=0)

    # CRITICAL STEP: FORCE NUMERIC TYPES
    X = X.apply(pd.to_numeric, errors="coerce")

    # Replace NaN / inf with 0
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0.0)

    # LightGBM prefers float32
    X = X.astype("float32")

    return X
