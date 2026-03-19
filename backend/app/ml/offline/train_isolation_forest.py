from pathlib import Path
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

DATA_PATH = Path("app/ml/offline/paysim_training_dataset.csv")
ARTIFACT_DIR = Path("app/ml/artifacts")

ANOMALY_FEATURES = [
    "amount",
    "balance_delta_orig",
    "balance_delta_dest",
    "type_CASH_OUT",
    "type_DEBIT",
    "type_PAYMENT",
    "type_TRANSFER",
]

def main():
    print("Loading training data...")
    df = pd.read_csv(DATA_PATH)

    X = df[ANOMALY_FEATURES].fillna(0)

    print("Training Isolation Forest...")
    model = IsolationForest(
        n_estimators=200,
        contamination=0.01, 
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X)

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, ARTIFACT_DIR / "isolation_forest.joblib")

    print("Isolation Forest trained and saved")

if __name__ == "__main__":
    main()