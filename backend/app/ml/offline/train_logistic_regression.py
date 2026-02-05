import pandas as pd
import joblib
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

DATA_PATH = Path("app/ml/offline/paysim_training_dataset.csv")
ARTIFACT_DIR = Path("app/ml/artifacts")

FEATURE_COLS = [
    "amount",
    "balance_delta_orig",
    "balance_delta_dest",
    "user_tx_count",
    "user_avg_amount",
    "dest_tx_count",
    "dest_fraud_rate",
    "amount_zscore_global",
    "amount_vs_user_avg_ratio",
    "is_first_tx_high_amount",
    "type_CASH_OUT",
    "type_DEBIT",
    "type_PAYMENT",
    "type_TRANSFER",
]

LABEL_COL = "label"


def main():
    print("Loading training dataset...")
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURE_COLS]
    y = df[LABEL_COL]

    print("Fitting scaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("Training Logistic Regression...")
    model = LogisticRegression(
    max_iter=2000,
    class_weight={0: 1, 1: 20}
)
    model.fit(X_scaled, y)

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, ARTIFACT_DIR / "logreg_model.joblib")
    joblib.dump(scaler, ARTIFACT_DIR / "scaler.joblib")
    joblib.dump(list(X.columns), ARTIFACT_DIR / "feature_names.joblib")

    print("Training complete")
    print("Features used:", list(X.columns))
    print("Model expects:", model.n_features_in_)
    print("Scaler fitted on:", scaler.n_features_in_)


if __name__ == "__main__":
    main()