from pathlib import Path
import json
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

    
# Paths
    
BASE_DIR = Path(__file__).resolve().parents[3]   # backend/
DATA_DIR = BASE_DIR / "app" / "data" / "ieee"
OUT_DIR = BASE_DIR / "app" / "ml" / "offline"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_PATH = OUT_DIR / "ieee_offline_metrics.json"

TX_PATH = DATA_DIR / "train_transaction.csv"
ID_PATH = DATA_DIR / "train_identity.csv"

    
# Feature config (MUST MATCH TRAINING)
    
TX_FEATURES = [
    "TransactionAmt",
    "ProductCD",
    "card1",
    "addr1",
    "C1",
    "C2",
    "D1",
]

ID_FEATURES = (
    ["DeviceType", "DeviceInfo"]
    + [f"id_{i:02d}" for i in range(1, 39)]
)

FEATURES = TX_FEATURES + ID_FEATURES
TARGET = "isFraud"

    
# Load & merge data (NO LEAKAGE)
    
print("Loading IEEE training data...")
tx = pd.read_csv(TX_PATH)
identity = pd.read_csv(ID_PATH)

df = tx.merge(identity, on="TransactionID", how="left")
df = df[FEATURES + [TARGET]].dropna()

    
# One-hot encode
    
X = pd.get_dummies(df[FEATURES], drop_first=True)
y = df[TARGET].values

# sanitize feature names for LightGBM
X.columns = X.columns.str.replace(r"[^A-Za-z0-9_]", "_", regex=True)

# remove duplicates (DeviceInfo collisions)
X = X.loc[:, ~X.columns.duplicated()]
feature_names = X.columns.tolist()

    
# Train / validation split
    
X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42,
)

    
# Imbalance handling
    
neg = (y_train == 0).sum()
pos = (y_train == 1).sum()
scale_pos_weight = neg / pos

print(f"Using scale_pos_weight = {scale_pos_weight:.2f}")

    
# Train LightGBM
    
train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

params = {
    "objective": "binary",
    "metric": "auc",
    "scale_pos_weight": scale_pos_weight,
    "learning_rate": 0.05,
    "num_leaves": 64,
    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq": 5,
    "verbosity": -1,
}

model = lgb.train(
    params,
    train_data,
    num_boost_round=500,
    valid_sets=[val_data],
    callbacks=[lgb.early_stopping(40)],
)

print("Best iteration:", model.best_iteration)

    
# Validation predictions
    
probs = model.predict(X_val)

roc_auc = roc_auc_score(y_val, probs)

    
# Threshold sweep (REDUCED, MEANINGFUL)
    
thresholds = [round(x, 2) for x in np.arange(0.1, 1.0, 0.1)]

sweep = []
operating_point = None

for th in thresholds:
    pred = probs >= th

    tp = ((pred == 1) & (y_val == 1)).sum()
    fn = ((pred == 0) & (y_val == 1)).sum()
    fp = ((pred == 1) & (y_val == 0)).sum()
    tn = ((pred == 0) & (y_val == 0)).sum()

    recall = tp / (tp + fn) if (tp + fn) else 0
    fpr = fp / (fp + tn) if (fp + tn) else 0

    row = {
        "threshold": th,
        "recall": round(recall, 4),
        "fpr": round(fpr, 4),
    }
    sweep.append(row)

    # choose operating point: high recall, <2% FPR
    if operating_point is None and fpr <= 0.02:
        operating_point = row

# fallback safety
if operating_point is None:
    operating_point = sweep[0]

    
# Score distribution (VALIDATION)
    
score_dist = {
    "mean": round(float(np.mean(probs)), 4),
    "p50": round(float(np.percentile(probs, 50)), 4),
    "p90": round(float(np.percentile(probs, 90)), 4),
    "p95": round(float(np.percentile(probs, 95)), 4),
    "p99": round(float(np.percentile(probs, 99)), 4),
}

    
# Feature importance (GAIN)
    
importances = model.feature_importance(importance_type="gain")
feat_imp = sorted(
    zip(feature_names, importances),
    key=lambda x: x[1],
    reverse=True,
)

feature_importance = [
    {"feature": f, "gain": round(float(g), 2)}
    for f, g in feat_imp[:15]
]

    
# Final metrics payload
    
metrics = {
    "model": "LightGBM (IEEE + Identity)",
    "evaluation_type": "Offline validation (IEEE)",
    "dataset": "IEEE-CIS Fraud Detection",
    "validation_split": 0.20,

    "roc_auc": round(roc_auc, 4),

    "operating_point": operating_point,

    "threshold_sweep": sweep,

    "score_distribution": score_dist,

    "feature_importance": feature_importance,

    "notes": [
        "Metrics computed on validation split only",
        "Identity features included",
        "Static until retraining",
    ],
}

    
# Save
    
with open(OUT_PATH, "w") as f:
    json.dump(metrics, f, indent=2)

print("\n✅ IEEE offline metrics computed & cached")
print("ROC-AUC:", metrics["roc_auc"])
print("Operating threshold:", operating_point)
print("Saved to:", OUT_PATH)
