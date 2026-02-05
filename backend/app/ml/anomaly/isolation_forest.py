import joblib
import numpy as np
from pathlib import Path
import os


IF_FEATURES = [
    "TransactionAmt",
    "card1", "card2", "card3", "card5",
    "addr1", "addr2",
    "C1", "C2", "C5", "C7", "C9",
    "D1", "D2", "D4", "D10",
]


class AnomalyScorer:
    """
    Lazy-loaded Isolation Forest scorer.
    App will NOT crash if model is missing at startup.
    """

    def __init__(self):
        self.model = None

        ml_dir = Path(__file__).resolve().parent
        self.model_path = ml_dir / os.getenv(
            "IF_MODEL_PATH",
            "ieee/artifacts/isolation_forest.joblib",
        )

    def _load_model(self):
        if self.model is not None:
            return

        if not self.model_path.exists():
            raise RuntimeError(
                f"Isolation Forest model not found at {self.model_path}. "
                f"Upload artifact or disable anomaly scoring."
            )

        self.model = joblib.load(self.model_path)

    def score(self, tx) -> float:
        """
        Returns anomaly score in [0, 1]
        Higher = more anomalous
        """
        self._load_model()

        x = np.array([
            getattr(tx, f, 0.0) or 0.0
            for f in IF_FEATURES
        ]).reshape(1, -1)

        # sklearn: higher = more normal → invert
        raw = self.model.score_samples(x)[0]
        anomaly_score = -raw

        return float(anomaly_score)
