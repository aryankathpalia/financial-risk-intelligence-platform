from pathlib import Path
import os
import joblib
import numpy as np
import warnings

warnings.filterwarnings(
    "ignore",
    message="LightGBM binary classifier with TreeExplainer shap values output has changed*"
)


class FraudClassifier:
    """
    Lazy-loading Fraud Classifier.
    - No ML artifacts touched at import time
    - Model + SHAP loaded only when predict/explain is called
    """

    def __init__(self):
        self.model = None
        self.explainer = None

        ml_dir = Path(__file__).resolve().parent
        self.model_path = ml_dir / os.getenv(
            "MODEL_PATH",
            "ieee/artifacts/lightgbm_model.joblib",
        )

    def _load_model(self):
        if self.model is not None:
            return

        if not self.model_path.exists():
            raise RuntimeError(
                f"Model artifact missing at {self.model_path}. "
                "ML inference is disabled."
            )

        # LAZY imports (CRITICAL)
        import shap
        from app.ml.features import build_features

        self._build_features = build_features
        self.model = joblib.load(self.model_path)
        self.explainer = shap.TreeExplainer(self.model)

    def predict(self, tx) -> float:
        self._load_model()

        X = self._build_features(tx)
        prob = float(self.model.predict(X)[0])
        return float(np.clip(prob, 0.0, 1.0))

    def explain(self, tx, top_k: int = 10):
        self._load_model()

        X = self._build_features(tx)
        shap_raw = self.explainer.shap_values(X)

        if isinstance(shap_raw, list):
            shap_vals = shap_raw[-1][0]
        else:
            shap_vals = shap_raw[0]

        shap_pairs = sorted(
            zip(X.columns.tolist(), shap_vals),
            key=lambda x: abs(x[1]),
            reverse=True,
        )

        return [
            {"feature": f, "contribution": float(v)}
            for f, v in shap_pairs[:top_k]
        ]
