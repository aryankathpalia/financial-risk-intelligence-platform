from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
             
# Paths             
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "PaySim_Synthetic_Financial_Dataset.csv"

ARTIFACT_DIR = BASE_DIR / "ml" / "artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
             
# Load data             
df = pd.read_csv(DATA_PATH)
             
# One-hot encode transaction type             
df = pd.get_dummies(df, columns=["type"], prefix="type")

FEATURES = [
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "type_CASH_OUT",
    "type_DEBIT",
    "type_PAYMENT",
    "type_TRANSFER",
]

X = df[FEATURES]
y = df["isFraud"]
             
# Train / test split             
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42,
)
             
# Scale             
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
             
# Model             
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    n_jobs=-1,
)

model.fit(X_train_scaled, y_train)
             
# Evaluation             
probs = model.predict_proba(X_test_scaled)[:, 1]

print("\n================ RAW FRAUD MODEL =================\n")
print("ROC-AUC:", round(roc_auc_score(y_test, probs), 4))
print(classification_report(y_test, probs > 0.5))
             
# Save artifacts             
joblib.dump(model, ARTIFACT_DIR / "raw_fraud_model.joblib")
joblib.dump(scaler, ARTIFACT_DIR / "raw_fraud_scaler.joblib")
joblib.dump(FEATURES, ARTIFACT_DIR / "raw_fraud_features.joblib")

print("\nSaved artifacts:")
print(" - raw_fraud_model.joblib")
print(" - raw_fraud_scaler.joblib")
print(" - raw_fraud_features.joblib")
