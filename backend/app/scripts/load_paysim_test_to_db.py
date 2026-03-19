import uuid
from datetime import datetime

import pandas as pd
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models.transaction import Transaction


CSV_PATH = "app/ml/offline/paysim_test_raw.csv"
BATCH_SIZE = 5000


def main():
    print("Loading PaySim test dataset...")
    df = pd.read_csv(CSV_PATH)

    print(f"Rows to load: {len(df)}")

    db: Session = SessionLocal()

    records = []

    for i, row in df.iterrows():
        tx = Transaction(
            id=uuid.uuid4(),

            amount=row["amount"],
            balance_delta_orig=row["balance_delta_orig"],
            balance_delta_dest=row["balance_delta_dest"],

            user_tx_count=int(row["user_tx_count"]),
            user_avg_amount=row["user_avg_amount"],

            dest_tx_count=int(row["dest_tx_count"]),
            dest_fraud_rate=row["dest_fraud_rate"],

            type_CASH_OUT=int(row["type_CASH_OUT"]),
            type_DEBIT=int(row["type_DEBIT"]),
            type_PAYMENT=int(row["type_PAYMENT"]),
            type_TRANSFER=int(row["type_TRANSFER"]),

            ingested_at=datetime.utcnow()
        )

        records.append(tx)

        if len(records) >= BATCH_SIZE:
            db.bulk_save_objects(records)
            db.commit()
            records.clear()

            print(f"Inserted {i + 1} rows")

    if records:
        db.bulk_save_objects(records)
        db.commit()

    db.close()

    print("PaySim test data successfully loaded into DB")


if __name__ == "__main__":
    main()
