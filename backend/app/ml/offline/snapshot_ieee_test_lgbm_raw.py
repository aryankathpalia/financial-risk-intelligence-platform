from pathlib import Path
import pandas as pd
import joblib
import json
import numpy as np

          
# Paths
          
BASE_DIR = Path(__file__).resolve().parents[2]  # -> backend/app
DATA_DIR = BASE_DIR / "data" / "ieee"

ARTIFACT_DIR = BASE_DIR / "ml" / "ieee" / "artifacts"


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

TX_PATH = DATA_DIR / "test_transaction.csv"
ID_PATH = DATA_DIR / "test_identity.csv"

MODEL_PATH = ARTIFACT_DIR / "lightgbm_model.joblib"
FEATURES_PATH = ARTIFACT_DIR / "features_lgbm.joblib"

OUT_PRED_PATH = OUTPUT_DIR / "ieee_test_lgbm_raw_predictions.csv"
OUT_STATS_PATH = OUTPUT_DIR / "ieee_test_lgbm_stats.json"

          
# Load artifacts
          
print("Loading model & feature list...")
model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURES_PATH)

          
# Load & merge test data
          
print("Loading test data...")
tx = pd.read_csv(TX_PATH)
identity = pd.read_csv(ID_PATH)

df = tx.merge(identity, on="TransactionID", how="left")

          
# Feature sets (IDENTICAL to training)
          
TX_FEATURES = [
    "TransactionAmt",
    "ProductCD",
    "card1",
    "addr1",
    "C1",
    "C2",
    "D1",
]

ID_FEATURES = [
    "DeviceType",
    "DeviceInfo",
] + [f"id_{i:02d}" for i in range(1, 39)]

FEATURES = TX_FEATURES + ID_FEATURES

          
# Keep only existing feature columns (IEEE test is sparse)
          
available_features = [c for c in FEATURES if c in df.columns]

df = df[["TransactionID"] + available_features]


          
# One-hot encode
          
X = pd.get_dummies(df[available_features], drop_first=True)


X.columns = (
    X.columns
    .str.replace(r"[^A-Za-z0-9_]", "_", regex=True)
)

X = X.loc[:, ~X.columns.duplicated()]

          
# Align features EXACTLY
          
X = X.reindex(columns=features, fill_value=0)

          
# Raw inference
          
print("Running LightGBM inference...")
fraud_probs = model.predict(X)

          
# Save predictions
          
pred_df = pd.DataFrame({
    "TransactionID": df["TransactionID"].values,
    "fraud_prob": fraud_probs,
})

pred_df.to_csv(OUT_PRED_PATH, index=False)

          
# STATS (RAW MODEL BEHAVIOR)
          
thresholds = [0.3, 0.5, 0.7, 0.9]

stats = {
    "total_transactions": int(len(fraud_probs)),
    "mean_fraud_prob": float(np.mean(fraud_probs)),
    "median_fraud_prob": float(np.median(fraud_probs)),
    "percentiles": {
        "p50": float(np.percentile(fraud_probs, 50)),
        "p90": float(np.percentile(fraud_probs, 90)),
        "p95": float(np.percentile(fraud_probs, 95)),
        "p99": float(np.percentile(fraud_probs, 99)),
    },
    "threshold_analysis": {},
}

for t in thresholds:
    count = int((fraud_probs >= t).sum())
    stats["threshold_analysis"][f">={t}"] = {
        "count": count,
        "rate_pct": round(count / len(fraud_probs) * 100, 3),
    }

          
# Save stats
          
with open(OUT_STATS_PATH, "w") as f:
    json.dump(stats, f, indent=2)

          
# Print summary
          
print("\n================ IEEE TEST SNAPSHOT STATS ================\n")
print(f"Total transactions evaluated : {stats['total_transactions']}")
print(f"Mean fraud probability       : {stats['mean_fraud_prob']:.4f}")
print(f"Median fraud probability     : {stats['median_fraud_prob']:.4f}")
print("\nProbability distribution:")
for k, v in stats["percentiles"].items():
    print(f"  {k}: {v:.4f}")

print("\nThreshold analysis:")
for t, v in stats["threshold_analysis"].items():
    print(f"  {t} → {v['count']} txns ({v['rate_pct']}%)")

print("\nPredictions saved to:", OUT_PRED_PATH)
print("Stats saved to:", OUT_STATS_PATH)
