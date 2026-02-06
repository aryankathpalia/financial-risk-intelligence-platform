from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "ieee"


TX_PATH = DATA_DIR / "test_transaction.csv"
ID_PATH = DATA_DIR / "test_identity.csv"


def load_ieee_test_rows(limit: int = 1000):
    tx = pd.read_csv(TX_PATH)
    identity = pd.read_csv(ID_PATH)

    df = tx.merge(identity, on="TransactionID", how="left")
    df = df.head(limit)

    return df.to_dict(orient="records")
