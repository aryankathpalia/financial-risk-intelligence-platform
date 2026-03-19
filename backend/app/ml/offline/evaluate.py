
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)

import joblib
from pathlib import Path


        
# Config
        
DATA_PATH = r"C:\Users\NewUser123\Downloads\creditcard.csv"

ARTIFACT_DIR = Path("app/ml/artifacts")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


        
# Load data
        
print("📥 Loading dataset...")
df = pd.read_csv(DATA_PATH)

print("Shape:", df.shape)
print(df["Class"].value_counts())


        
# Features / labels
        
X = df.drop(columns=["Class"])
y = df["Class"]

# Scale ONLY Amount (others are already PCA-scaled)
scaler = StandardScaler()
X["Amount"] = scaler.fit_transform(X[["Amount"]])


        
# Train / Test split
        
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)


        
# Model
        
model = LogisticRegression(
    class_weight="balanced",
    max_iter=1000,
    n_jobs=-1
)

print("🚀 Training Logistic Regression...")
model.fit(X_train, y_train)


        
# Evaluation
        
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\n Classification Report")
print(classification_report(y_test, y_pred))

print(" Confusion Matrix")
print(confusion_matrix(y_test, y_pred))

roc_auc = roc_auc_score(y_test, y_proba)
print(f" ROC-AUC: {roc_auc:.4f}")


        
# Save artifacts
        
joblib.dump(model, ARTIFACT_DIR / "logreg_model.joblib")
joblib.dump(scaler, ARTIFACT_DIR / "scaler.joblib")

print("✅ Model and scaler saved to app/ml/artifacts/")
