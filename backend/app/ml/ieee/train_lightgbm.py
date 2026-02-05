from pathlib import Path
import pandas as pd
import joblib
import lightgbm as lgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score


# Paths
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "app" / "data" / "ieee"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

TX_PATH = DATA_DIR / "train_transaction.csv"
ID_PATH = DATA_DIR / "train_identity.csv"


# Load & merge data
tx = pd.read_csv(TX_PATH)
identity = pd.read_csv(ID_PATH)

df = tx.merge(identity, on="TransactionID", how="left")


# Feature sets
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
TARGET = "isFraud"

df = df[FEATURES + [TARGET]].dropna()

# One-hot encode
X = pd.get_dummies(df[FEATURES], drop_first=True)
y = df[TARGET]

# sanitize feature names for LightGBM
X.columns = (
    X.columns
    .str.replace(r"[^A-Za-z0-9_]", "_", regex=True)
)

# REMOVE duplicate columns created by sanitization
X = X.loc[:, ~X.columns.duplicated()]


 
# Train / validation split
 
X_train, X_val, y_train, y_val = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42,
)

 
# Imbalance handling
 
neg = (y_train == 0).sum()
pos = (y_train == 1).sum()
scale_pos_weight = neg / pos

print(f"\nUsing scale_pos_weight = {scale_pos_weight:.2f}")

 
# LightGBM datasets
 
train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

 
# Params
 
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

 
# Train
 
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

 
# Evaluation
 
probs = model.predict(X_val)
auc = roc_auc_score(y_val, probs)

print("\n================ IEEE LIGHTGBM (IDENTITY) ================\n")
print("ROC-AUC:", round(auc, 4))
print("Best iteration:", model.best_iteration)

 
# Save artifacts
 
joblib.dump(model, ARTIFACT_DIR / "lightgbm_model.joblib")
joblib.dump(list(X.columns), ARTIFACT_DIR / "features_lgbm.joblib")

print("\n✅ Identity-aware LightGBM artifacts saved.")
