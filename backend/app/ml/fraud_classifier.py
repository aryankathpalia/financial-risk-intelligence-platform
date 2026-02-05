from pathlib import Path
import os
import joblib
import numpy as np
import shap
from app.ml.features import build_features

import warnings
warnings.filterwarnings(
    "ignore",
    message="LightGBM binary classifier with TreeExplainer shap values output has changed*"
)


class FraudClassifier:
    """
    Lazy-loading Fraud Classifier.
    Model + SHAP explainer are loaded ONLY when needed.
    App will NOT crash at startup if artifacts are missing.
    """

    def __init__(self):
        self.model = None
        self.explainer = None

        ml_dir = Path(__file__).resolve().parent  # backend/app/ml

        self.model_path = ml_dir / os.getenv(
            "MODEL_PATH",
            "ieee/artifacts/lightgbm_model.joblib",
        )

    # -------------------------
    # INTERNAL: LOAD MODEL ONCE
    # -------------------------
    def _load_model(self):
        if self.model is not None:
            return

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model artifact not found at {self.model_path}. "
                f"Deploy artifacts or disable ML endpoints."
            )

        self.model = joblib.load(self.model_path)
        self.explainer = shap.TreeExplainer(self.model)

    # -------------------------
    # PREDICTION
    # -------------------------
    def predict(self, tx) -> float:
        self._load_model()

        X = build_features(tx)   # DataFrame
        prob = float(self.model.predict(X)[0])
        return float(np.clip(prob, 0.0, 1.0))

    # -------------------------
    # SHAP EXPLANATION
    # -------------------------
    def explain(self, tx, top_k: int = 10):
        """
        Returns top-k SHAP contributors for FRAUD class.
        Positive value => increases fraud risk
        """
        self._load_model()

        X = build_features(tx)   # DataFrame (1 row)

        shap_raw = self.explainer.shap_values(X)

        # --- Robust SHAP handling ---
        if isinstance(shap_raw, list):
            shap_vals = shap_raw[-1][0]  # fraud class
        else:
            shap_vals = shap_raw[0]

        feature_names = X.columns.tolist()
        shap_pairs = list(zip(feature_names, shap_vals))

        shap_pairs.sort(key=lambda x: abs(x[1]), reverse=True)

        return [
            {
                "feature": feature,
                "contribution": float(value),
            }
            for feature, value in shap_pairs[:top_k]
        ]
