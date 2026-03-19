import pandas as pd
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.transaction import Transaction

def load_transactions(csv_path: str):
    df = pd.read_csv(csv_path)

    db: Session = SessionLocal()

    for _, row in df.iterrows():
        tx = Transaction(
            user_id=str(row["user_id"]),
            amount=float(row["amount"]),
            merchant=row["merchant"]
        )
        db.add(tx)

    db.commit()
    db.close()

    print(f"Loaded {len(df)} transactions into DB")

if __name__ == "__main__":
    load_transactions("app/data/raw/transactions.csv")
