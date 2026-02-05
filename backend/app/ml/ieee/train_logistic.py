from pathlib import Path
import pandas as pd
import joblib
import lightgbm as lgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score


  
# Paths
  
BASE_DIR = Path(__file__).resolve().parents[3]   # backend/
DATA_DIR = BASE_DIR / "app" / "data" / "ieee"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

TX_PATH = DATA_DIR / "train_transaction.csv"


  
# Load data
  
df = pd.read_csv(TX_PATH)

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

df = df[FEATURES + [TARGET]].dropna()

X = pd.get_dummies(df[FEATURES], drop_first=True)
y = df[TARGET]


  
# Train / Validation split
  
X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42,
)


  
# Compute scale_pos_weight (CRITICAL FOR RECALL)
  
neg = (y_train == 0).sum()
pos = (y_train == 1).sum()
scale_pos_weight = neg / pos

print(f"\nUsing scale_pos_weight = {scale_pos_weight:.2f}")


  
# LightGBM Dataset
  
train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)


  
# Parameters (RECALL-OPTIMIZED)
  
params = {
    "objective": "binary",
    "metric": "auc",
    "boosting_type": "gbdt",

    # imbalance handling
    "scale_pos_weight": scale_pos_weight,

    # model capacity
    "learning_rate": 0.05,
    "num_leaves": 63,

    # regularization
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
        lgb.early_stopping(stopping_rounds=40),
        lgb.log_evaluation(period=50),
    ],
)


  
# Evaluation
  
probs = model.predict(X_val)
auc = roc_auc_score(y_val, probs)

print("\n================ IEEE LIGHTGBM (IMBALANCE-AWARE) ================\n")
print("ROC-AUC:", round(auc, 4))


  
# Save artifacts
  
joblib.dump(model, ARTIFACT_DIR / "lightgbm_model.joblib")
joblib.dump(X.columns.tolist(), ARTIFACT_DIR / "features_lgbm.joblib")

print("\n✅ Updated LightGBM artifacts saved.")
