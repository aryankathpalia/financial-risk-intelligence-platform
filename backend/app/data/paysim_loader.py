# app/data/paysim_loader.py

import csv
from pathlib import Path

DATA_PATH = Path(
    r"C:\Users\NewUser123\Downloads\PaySim_Synthetic_Financial_Dataset.csv"
)

def load_paysim_sample(limit: int = 5000):
    """
    IMPORTANT:
    - paysim_row_test_id MUST be the REAL row index
    - This MUST match paysim_test_labels.csv
    """

    rows = []

    with open(DATA_PATH, newline="") as f:
        reader = csv.DictReader(f)

        for real_row_id, row in enumerate(reader):
            if real_row_id >= limit:
                break

            rows.append({
                # 🔑 REAL USER ID
                "nameOrig": row["nameOrig"],

                # ✅ REAL PaySim ROW INDEX (CRITICAL FIX)
                "paysim_row_test_id": real_row_id,

                # RAW AMOUNTS (NO TRANSFORMS)
                "amount": float(row["amount"]),
                "oldbalanceOrg": float(row["oldbalanceOrg"]),
                "newbalanceOrig": float(row["newbalanceOrig"]),
                "oldbalanceDest": float(row["oldbalanceDest"]),
                "newbalanceDest": float(row["newbalanceDest"]),

                # ONE-HOT TX TYPE
                "type_CASH_OUT": int(row["type"] == "CASH_OUT"),
                "type_DEBIT": int(row["type"] == "DEBIT"),
                "type_PAYMENT": int(row["type"] == "PAYMENT"),
                "type_TRANSFER": int(row["type"] == "TRANSFER"),
            })

    return rows
