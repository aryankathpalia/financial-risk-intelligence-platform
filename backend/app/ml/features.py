from pathlib import Path
import pandas as pd
import joblib
import numpy as np
import os


BASE_DIR = Path(__file__).resolve().parents[2]  # backend/
ARTIFACT_DIR = BASE_DIR / "app" / "ml" / "ieee" / "artifacts"

FEATURES_PATH = ARTIFACT_DIR / "features_lgbm.joblib"


def _load_feature_columns():
    if not FEATURES_PATH.exists():
        raise RuntimeError(
            f"Feature artifacts missing at {FEATURES_PATH}"
        )
    return joblib.load(FEATURES_PATH)




def build_features(tx):
    feature_columns = _load_feature_columns()

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

    df = pd.DataFrame([row])

    df.columns = df.columns.str.replace(
        r"[^A-Za-z0-9_]", "_", regex=True
    )

    X = df.reindex(columns=feature_columns, fill_value=0)
    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    X = X.astype("float32")

    return X
