import pandas as pd
import psycopg2

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "aryankathpalia",
}

LABELS_PATH = "app/ml/offline/paysim_test_labels.csv"


def main():
    print("📥 Loading PaySim test labels...")
    labels = pd.read_csv(LABELS_PATH)["label"].tolist()

    print("🔌 Connecting to DB (read-only)...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("📦 Fetching ingested transactions...")
    cur.execute("""
        SELECT id, decision
        FROM transactions
        ORDER BY ingested_at ASC
    """)
    rows = cur.fetchall()

    tx_ids = [str(r[0]) for r in rows]
    decisions = [r[1] for r in rows]

    n = len(tx_ids)
    labels = labels[:n]  # align to ingested slice

    # Confusion counts
    TP = FP = FN = TN = 0

    for decision, label in zip(decisions, labels):
        flagged = decision in ("BLOCK", "REVIEW")

        if flagged and label == 1:
            TP += 1
        elif flagged and label == 0:
            FP += 1
        elif not flagged and label == 1:
            FN += 1
        elif not flagged and label == 0:
            TN += 1

    print("\nONLINE MODEL EVALUATION (INGESTED DATA)\n")
    print(f"Total ingested: {n}")
    print(f"True Positives  (TP): {TP}")
    print(f"False Positives (FP): {FP}")
    print(f"False Negatives (FN): {FN}")
    print(f"True Negatives  (TN): {TN}")

    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    flag_rate = (TP + FP) / n

    print("\nMetrics")
    print(f"Recall    : {recall:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Flag rate : {flag_rate:.4%}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()