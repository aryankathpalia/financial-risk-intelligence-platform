import joblib
from pathlib import Path

ARTIFACT_DIR = Path("app/ml/artifacts")

model = joblib.load(ARTIFACT_DIR / "fraud_model.joblib")
scaler = joblib.load(ARTIFACT_DIR / "scaler.joblib")
feature_names = joblib.load(ARTIFACT_DIR / "feature_names.joblib")

print("\n=== FEATURE CONTRACT (SOURCE OF TRUTH) ===")
for i, f in enumerate(feature_names):
    print(f"{i+1}. {f}")

print("\nTotal features:", len(feature_names))
