# app/ml/offline/build_training_dataset.py

from sqlalchemy.orm import Session
import pandas as pd
import joblib
from pathlib import Path

from app.db.database import SessionLocal

from app.db.models.transaction import Transaction

ARTIFACT_DIR = Path("app/ml/artifacts")


def build_training_dataset():
    db: Session = SessionLocal()

    rows = (
        db.query(Transaction)
        .filter(Transaction.analyst_label.isnot(None))
        .all()
    )

    data = []
    for tx in rows:
        data.append({
            "amount": tx.amount,
            "balance_delta_orig": tx.balance_delta_orig,
            "balance_delta_dest": tx.balance_delta_dest,
            "user_tx_count": tx.user_tx_count,
            "user_avg_amount": tx.user_avg_amount,
            "dest_tx_count": tx.dest_tx_count,
            "dest_fraud_rate": tx.dest_fraud_rate,
            "type_CASH_OUT": tx.type_CASH_OUT,
            "type_DEBIT": tx.type_DEBIT,
            "type_PAYMENT": tx.type_PAYMENT,
            "type_TRANSFER": tx.type_TRANSFER,
            "label": tx.analyst_label,
        })

    df = pd.DataFrame(data)

    #  GLOBAL STATS (CRITICAL)
    amount_mean = df["amount"].mean()
    amount_std = df["amount"].std()

    df["amount_zscore_global"] = (df["amount"] - amount_mean) / amount_std
    df["amount_vs_user_avg_ratio"] = df["amount"] / df["user_avg_amount"].clip(lower=1.0)

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"mean": amount_mean, "std": amount_std},
        ARTIFACT_DIR / "amount_stats.joblib",
    )

    return df


if __name__ == "__main__":
    df = build_training_dataset()
    print(df.head())