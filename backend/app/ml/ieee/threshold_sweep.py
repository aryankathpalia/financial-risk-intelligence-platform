from pathlib import Path
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split


# Paths
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "app" / "data" / "ieee"

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
tx = pd.read_csv(TX_PATH)
identity = pd.read_csv(ID_PATH)

df = tx.merge(identity, on="TransactionID", how="left")
df = df[FEATURES + [TARGET]].dropna()


# One-hot encode
X = pd.get_dummies(df[FEATURES], drop_first=True)
y = df[TARGET]

# sanitize feature names for LightGBM
X.columns = X.columns.str.replace(r"[^A-Za-z0-9_]", "_", regex=True)

# remove duplicate columns (DeviceInfo collisions)
X = X.loc[:, ~X.columns.duplicated()]


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

print(f"\nUsing scale_pos_weight = {scale_pos_weight:.2f}")

# Train LightGBM (same setup as training)
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

print("\nBest iteration:", model.best_iteration)


# Validation probabilities
probs = model.predict(X_val)


# Threshold sweep
print("\n========== THRESHOLD SWEEP (IDENTITY MODEL) ==========\n")
print("Threshold | Recall  | False Positive Rate")
print("--------------------------------------------")

thresholds = [i / 100 for i in range(5, 96, 5)]

for th in thresholds:
    tp = fp = fn = tn = 0

    for p, label in zip(probs, y_val):
        pred = p >= th

        if label == 1 and pred:
            tp += 1
        elif label == 1 and not pred:
            fn += 1
        elif label == 0 and pred:
            fp += 1
        else:
            tn += 1

    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0

    marker = " <==" if fpr <= 0.10 else ""

    print(f"{th:8.2f} | {recall:6.2%} | {fpr:8.2%}{marker}")

print("\n<== marks thresholds with ≤10% false positives")
