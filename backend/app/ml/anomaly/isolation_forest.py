import joblib
import numpy as np
from pathlib import Path
from sklearn.ensemble import IsolationForest

IF_FEATURES = [
    "TransactionAmt",
    "card1", "card2", "card3", "card5",
    "addr1", "addr2",
    "C1", "C2", "C5", "C7", "C9",
    "D1", "D2", "D4", "D10",
]

ARTIFACT_PATH = Path("app/ml/ieee/artifacts/isolation_forest.joblib")


class AnomalyScorer:
    def __init__(self):
        if not ARTIFACT_PATH.exists():
            raise RuntimeError("Isolation Forest model not found")
        self.model = joblib.load(ARTIFACT_PATH)

    def score(self, tx) -> float:
        """
        Returns anomaly score in [0, 1]
        Higher = more anomalous
        """
        x = np.array([
            getattr(tx, f, 0.0) or 0.0
            for f in IF_FEATURES
        ]).reshape(1, -1)

        # sklearn: higher = more normal → invert
        raw = self.model.score_samples(x)[0]
        anomaly_score = -raw

        return float(anomaly_score)
