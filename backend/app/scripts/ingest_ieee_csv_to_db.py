import pandas as pd
from sqlalchemy import create_engine
import os
from uuid import uuid4
from datetime import datetime, timezone

# ---------- CONFIG ----------
DATABASE_URL = os.environ["DATABASE_URL"]




from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  

DATA_DIR = BASE_DIR / "app" / "data" / "ieee"

TX_CSV = DATA_DIR / "test_transaction.csv"
ID_CSV = DATA_DIR / "test_identity.csv"



CHUNK_SIZE = 5000
# ----------------------------


def main():
    engine = create_engine(DATABASE_URL)

    print("Loading CSVs...")
    tx = pd.read_csv(TX_CSV)
    idn = pd.read_csv(ID_CSV)


    print("Merging...")
    df = tx.merge(idn, on="TransactionID", how="left")

    print(f"Total rows: {len(df)}")

    # Minimal columns (match your Transaction model)
    keep_cols = [
        "TransactionID",
        "TransactionAmt",
        "ProductCD",
        "card1",
        "addr1",
        "C1",
        "C2",
        "D1",
        "DeviceType",
        "DeviceInfo",
    ]

    df = df[keep_cols]

    # Add system fields
    df["id"] = [uuid4() for _ in range(len(df))]
    df["ingested_at"] = datetime.now(timezone.utc)

    print("Inserting into DB...")
    df.to_sql(
        "ieee_raw_transactions", 
        engine,
        if_exists="append",
        index=False,
        chunksize=CHUNK_SIZE,
        method="multi",
    )

    print("DONE")


if __name__ == "__main__":
    main()
