from pathlib import Path
import joblib
import numpy as np
import shap
import os
from app.ml.features import build_features


import warnings
warnings.filterwarnings(
    "ignore",
    message="LightGBM binary classifier with TreeExplainer shap values output has changed*"
)


class FraudClassifier:
    def __init__(self):
        ml_dir = Path(__file__).resolve().parent  # backend/app/ml
        artifact_dir = ml_dir / "ieee" / "artifacts"



        MODEL_PATH = os.getenv(
            "MODEL_PATH",
            "ieee/artifacts/lightgbm_model.joblib",
        )

        model_path = ml_dir / MODEL_PATH


        if not model_path.exists():
            raise FileNotFoundError(f"Missing model file: {model_path}")

        self.model = joblib.load(model_path)

        # SHAP explainer (loaded ONCE)
        self.explainer = shap.TreeExplainer(self.model)

            
    # PREDICTION

    def predict(self, tx) -> float:
        X = build_features(tx)   # DataFrame
        prob = float(self.model.predict(X)[0])
        return float(np.clip(prob, 0.0, 1.0))

            
    # SHAP EXPLANATION
            
    def explain(self, tx, top_k: int = 10):
        """
        Returns top-k SHAP contributors for FRAUD class.
        Positive value => increases fraud risk
        """

        X = build_features(tx)   # DataFrame (1 row)

        shap_raw = self.explainer.shap_values(X)

        # --- Robust SHAP handling (NO ASSUMPTIONS) ---
        if isinstance(shap_raw, list):
            # Binary classifier → take fraud class (last)
            shap_vals = shap_raw[-1][0]
        else:
            # Single-output model
            shap_vals = shap_raw[0]

        feature_names = X.columns.tolist()

        shap_pairs = list(zip(feature_names, shap_vals))

        # Sort by absolute impact
        shap_pairs.sort(key=lambda x: abs(x[1]), reverse=True)

        return [
            {
                "feature": feature,
                "contribution": float(value),
            }
            for feature, value in shap_pairs[:top_k]
        ]
