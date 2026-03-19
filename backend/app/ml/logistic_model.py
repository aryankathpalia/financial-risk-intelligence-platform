import joblib
import numpy as np
from pathlib import Path

# backend/app/ml/artifacts/
ARTIFACT_DIR = Path(__file__).parent / "artifacts"


class LogisticFraudModel:
    def __init__(self):
        self.model = None
        self.scaler = None

    def load(self):
        if self.model is None or self.scaler is None:
            self.model = joblib.load(ARTIFACT_DIR / "logreg_model.joblib")
            self.scaler = joblib.load(ARTIFACT_DIR / "scaler.joblib")

    def predict_proba(self, features: np.ndarray) -> float:
        self.load()
        X_scaled = self.scaler.transform([features])
        return float(self.model.predict_proba(X_scaled)[0][1])
