# app/ml/risk_model.py

import joblib
from pathlib import Path
import pandas as pd

ARTIFACT_DIR = Path("app/ml/artifacts")

# --------------------------------------------------
# ANOMALY MODEL FEATURE CONTRACT
# --------------------------------------------------
# These MUST match EXACTLY what the Isolation Forest
# is trained on (and only include raw, stable signals).
# --------------------------------------------------

ANOMALY_FEATURES = [
    "amount",
    "balance_delta_orig",
    "balance_delta_dest",
    "type_CASH_OUT",
    "type_DEBIT",
    "type_PAYMENT",
    "type_TRANSFER",
]


class RiskModel:
    """
    Isolation Forest–based anomaly detector.

    Outputs a normalized anomaly score in range [0, 1],
    where higher = more anomalous.
    """

    def __init__(self):
        self.model = None

    def load(self):
        if self.model is None:
            self.model = joblib.load(
                ARTIFACT_DIR / "isolation_forest.joblib"
            )

    def predict(self, features) -> float:
        """
        `features` is a TransactionFeatures object.
        We explicitly extract ONLY anomaly-safe features.
        """
        self.load()

        X = pd.DataFrame(
            [[getattr(features, f) for f in ANOMALY_FEATURES]],
            columns=ANOMALY_FEATURES,
        )

        # Isolation Forest:
        # decision_function -> higher = more normal
        # so we invert it
        raw_score = -self.model.decision_function(X)[0]

        # Normalize roughly into [0, 1]
        anomaly_score = raw_score + 0.5

        # Clamp for safety
        anomaly_score = min(max(anomaly_score, 0.0), 1.0)

        return float(anomaly_score)