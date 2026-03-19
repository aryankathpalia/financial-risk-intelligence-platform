from pathlib import Path
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

   
# Paths
   
BASE_DIR = Path(__file__).resolve().parents[3]   # backend/
DATA_DIR = BASE_DIR / "app" / "data" / "ieee"

TX_PATH = DATA_DIR / "train_transaction.csv"

   
# Config
   
SAMPLE_SIZE = 1000        
REVIEW_TH = 0.30
BLOCK_TH = 0.70

FEATURES = [
    "TransactionAmt",
    "ProductCD",
    "card1",
    "addr1",
    "C1",
    "C2",
    "D1",
]

TARGET = "isFraud"

   
# Load & prepare data
   
df = pd.read_csv(TX_PATH)
df = df[FEATURES + [TARGET]].dropna()

X = pd.get_dummies(df[FEATURES], drop_first=True)
y = df[TARGET]

   
# Train / Validation split (CRITICAL)
   
X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42,
)

   
# Imbalance handling (KEY FOR RECALL)
   
neg = (y_train == 0).sum()
pos = (y_train == 1).sum()
scale_pos_weight = neg / pos

print(f"\nUsing scale_pos_weight = {scale_pos_weight:.2f}")

   
# LightGBM datasets
   
train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val)

   
# LightGBM params (RECALL-OPTIMIZED)
   
params = {
    "objective": "binary",
    "metric": "auc",
    "boosting_type": "gbdt",
    "scale_pos_weight": scale_pos_weight,

    "learning_rate": 0.05,
    "num_leaves": 63,

    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq": 5,

    "verbosity": -1,
}

   
# Train model
   
model = lgb.train(
    params,
    train_data,
    num_boost_round=500,
    valid_sets=[val_data],
    callbacks=[
        lgb.early_stopping(40),
        lgb.log_evaluation(50),
    ],
)

print(f"\nBest iteration: {model.best_iteration}")

   
# AUC sanity check
   
val_probs = model.predict(X_val)
auc = roc_auc_score(y_val, val_probs)

print("\n================ VALIDATION AUC =================")
print(f"ROC-AUC: {auc:.4f}")

   
# SINGLE-TRANSACTION BULK TEST (VALIDATION ONLY)
   
val_df = X_val.copy()
val_df["isFraud"] = y_val.values

sample = val_df.sample(
    min(SAMPLE_SIZE, len(val_df)),
    random_state=42
)

total_fraud = 0
caught_review = 0
caught_block = 0
false_positives = 0

for _, row in sample.iterrows():
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
    print(f"Recall @ REVIEW ({REVIEW_TH:.2f}) : {caught_review / total_fraud:.2%}")
    print(f"Recall @ BLOCK  ({BLOCK_TH:.2f}) : {caught_block / total_fraud:.2%}")

print(f"False positives (REVIEW+): {false_positives}")
print(
    f"False positive rate      : "
    f"{false_positives / max(1, (len(sample) - total_fraud)):.2%}"
)

print("\n✅ Validation single-transaction test complete.")
