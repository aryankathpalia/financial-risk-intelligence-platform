import pandas as pd
import joblib
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_auc_score
)

# IMPORTANT: import the correct builder
from build_synthetic_features import build_synthetic_features


       
# LOAD DATASET
       
df = pd.read_csv("app/data/synthetic_dataset/synthetic_fraud_dataset.csv")
y_true = df["is_fraud"].astype(int)

       
# BUILD FEATURES
       
X = build_synthetic_features(df)

       
# LOAD MODEL + SCALER
       
model = joblib.load("app/ml/artifacts/logreg_model.joblib")
scaler = joblib.load("app/ml/artifacts/scaler.joblib")

       
# SCALE FEATURES
       
X_scaled = scaler.transform(X)

       
# PREDICT
       
y_prob = model.predict_proba(X_scaled)[:, 1]
y_pred = (y_prob >= 0.5).astype(int)

       
# METRICS
       
print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))

print("\nClassification Report:")
print(classification_report(y_true, y_pred, digits=4))

print("\nROC AUC Score:")
print(roc_auc_score(y_true, y_prob))