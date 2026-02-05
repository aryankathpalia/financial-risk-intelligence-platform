from pathlib import Path
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

DATA_PATH = Path("app/ml/offline/paysim_training_dataset.csv")
ARTIFACT_DIR = Path("app/ml/artifacts")

ONLINE_FEATURES = [
    "amount",
    "balance_delta_orig",
    "balance_delta_dest",
    "user_tx_count",
    "user_avg_amount",
    "is_first_tx_high_amount",
    "type_CASH_OUT",
    "type_DEBIT",
    "type_PAYMENT",
    "type_TRANSFER",
]

def main():
    print("Loading causal training dataset...")
    df = pd.read_csv(DATA_PATH)

    X = df[ONLINE_FEATURES].fillna(0)
    y = df["label"]

    print("Fitting scaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("Training ONLINE Logistic Regression (recall-optimized)...")
    model = LogisticRegression(
        max_iter=2000,
        class_weight={0: 1, 1: 40},  # recall boost
        C=0.5,                      # reduce overconfidence
        solver="lbfgs"
    )
    model.fit(X_scaled, y)

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, ARTIFACT_DIR / "logreg_model_online.joblib")
    joblib.dump(scaler, ARTIFACT_DIR / "scaler_online.joblib")
    joblib.dump(ONLINE_FEATURES, ARTIFACT_DIR / "feature_names_online.joblib")

    print("Online fraud model trained")
    print("Features:", ONLINE_FEATURES)

if __name__ == "__main__":
    main()