from pathlib import Path
import pandas as pd
import numpy as np

from app.db.deps import get_db
from app.db.models.transaction import Transaction


       
# Paths
       
BASE_DIR = Path(__file__).resolve().parent

SNAPSHOT_PATH = (
    BASE_DIR / "outputs" / "ieee_test_lgbm_raw_predictions.csv"
)

       
# Config
       
ABS_TOL = 1e-6       # acceptable numeric drift
REVIEW_TH = 0.30
BLOCK_TH = 0.70


def main():
    print("\n========== IEEE ONLINE vs SNAPSHOT CHECK ==========\n")

      
    # Load snapshot predictions
      
    snap = pd.read_csv(SNAPSHOT_PATH)

    snap["TransactionID"] = snap["TransactionID"].astype(str)

    snap_map = dict(
        zip(snap["TransactionID"], snap["fraud_prob"])
    )

    print(f"Snapshot transactions loaded : {len(snap_map)}")

      
    # Load online-scored txns
      
    db = next(get_db())

    txs = (
        db.query(Transaction)
        .filter(Transaction.TransactionID.isnot(None))
        .filter(Transaction.fraud_prob.isnot(None))
        .all()
    )

    print(f"Online transactions loaded   : {len(txs)}")

      
    # Compare
      
    matched = 0
    mismatched = 0
    deltas = []

    review_mismatch = 0
    block_mismatch = 0

    for tx in txs:
        tid = str(tx.TransactionID)

        snap_prob = snap_map.get(tid)
        if snap_prob is None:
            continue

        matched += 1

        online_prob = float(tx.fraud_prob)
        delta = abs(online_prob - snap_prob)
        deltas.append(delta)

        # numeric drift check
        if delta > ABS_TOL:
            mismatched += 1

        # threshold behavior check
        if (online_prob >= REVIEW_TH) != (snap_prob >= REVIEW_TH):
            review_mismatch += 1

        if (online_prob >= BLOCK_TH) != (snap_prob >= BLOCK_TH):
            block_mismatch += 1

      
    # Report
      
    print("\n--------------- COVERAGE ---------------")
    print(f"Matched transactions         : {matched}")
    print(f"Unmatched (ignored)          : {len(txs) - matched}")

    if matched == 0:
        print("\n❌ NO OVERLAP FOUND — CHECK TransactionID PIPELINE")
        return

    deltas = np.array(deltas)

    print("\n--------------- NUMERIC CHECK ---------------")
    print(f"Max abs delta                : {deltas.max():.8f}")
    print(f"Mean abs delta               : {deltas.mean():.8f}")
    print(f"Exact matches (≤ tol)        : {matched - mismatched}")
    print(f"Mismatches (> tol)           : {mismatched}")

    print("\n--------------- DECISION CHECK ---------------")
    print(f"REVIEW threshold mismatches  : {review_mismatch}")
    print(f"BLOCK threshold mismatches   : {block_mismatch}")

      
    # Final verdict
      
    print("\n=============== VERDICT ===============")

    if mismatched == 0 and review_mismatch == 0 and block_mismatch == 0:
        print("✅ ONLINE SYSTEM MATCHES OFFLINE SNAPSHOT PERFECTLY")
    else:
        print("⚠️  DISCREPANCIES FOUND")
        print("→ Numeric drift:", mismatched)
        print("→ Review drift :", review_mismatch)
        print("→ Block drift  :", block_mismatch)

    print("\n=======================================\n")


if __name__ == "__main__":
    main()
