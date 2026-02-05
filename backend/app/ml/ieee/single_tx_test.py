from pathlib import Path
import pandas as pd
import joblib
import lightgbm as lgb
from sklearn.model_selection import train_test_split


# Paths
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "app" / "data" / "ieee"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"

TX_PATH = DATA_DIR / "train_transaction.csv"


# Load data
FEATURES_BASE = [
    "TransactionAmt",
    "ProductCD",
    "card1",
    "addr1",
    "C1",
    "C2",
    "D1",
]

TARGET = "isFraud"

df = pd.read_csv(TX_PATH)
df = df[FEATURES_BASE + [TARGET]].dropna()

X = pd.get_dummies(df[FEATURES_BASE], drop_first=True)
y = df[TARGET]


# Train / Validation split (CRITICAL)
X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42,
)


# Train LightGBM ONLY on training split
train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val)

params = {
    "objective": "binary",
    "metric": "auc",
    "boosting_type": "gbdt",
    "learning_rate": 0.05,
    "num_leaves": 31,
    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq": 5,
    "verbosity": -1,
}

model = lgb.train(
    params,
    train_data,
    num_boost_round=300,
    valid_sets=[val_data],
    callbacks=[lgb.early_stopping(30)],
)


# Single-transaction bulk test (VALIDATION ONLY)
N = 1000  # change to 500 or 1000 safely

val_df = X_val.copy()
val_df["isFraud"] = y_val.values

sample = val_df.sample(min(N, len(val_df)), random_state=42)

REVIEW_TH = 0.30
BLOCK_TH = 0.70

total_fraud = 0
caught_review = 0
caught_block = 0
false_positives = 0

for idx, row in sample.iterrows():
    x = row.drop("isFraud").values.reshape(1, -1)
    prob = float(model.predict(x)[0])

    if row.isFraud == 1:
        total_fraud += 1
        if prob >= REVIEW_TH:
            caught_review += 1
        if prob >= BLOCK_TH:
            caught_block += 1
    else:
        if prob >= REVIEW_TH:
            false_positives += 1


# Results
print("\n========== VALIDATION SINGLE-TX TEST ==========\n")
print(f"Sample size              : {len(sample)}")
print(f"Frauds in sample         : {total_fraud}")

if total_fraud > 0:
    print(f"Recall @ REVIEW (0.30)   : {caught_review / total_fraud:.2%}")
    print(f"Recall @ BLOCK  (0.70)   : {caught_block / total_fraud:.2%}")

print(f"False positives (REVIEW+): {false_positives}")
print(
    f"False positive rate      : "
    f"{false_positives / max(1, (len(sample) - total_fraud)):.2%}"
)
