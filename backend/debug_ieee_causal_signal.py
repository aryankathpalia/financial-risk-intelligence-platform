import pandas as pd
from collections import defaultdict

# Paths
BASE = "app/data/ieee"
TX_PATH = f"{BASE}/train_transaction.csv"

# Load IEEE train transactions
df = pd.read_csv(TX_PATH)

# Keep only needed columns
df = df[
    [
        "TransactionDT",
        "TransactionAmt",
        "card1",
        "isFraud",
    ]
].dropna()

# Sort by time (CRITICAL — no leakage)
df = df.sort_values("TransactionDT")

# Limit rows for speed (enough for signal)
df = df.iloc[:200000]

# History container
card_tx_count = defaultdict(int)
rows = []

for _, row in df.iterrows():
    card = row["card1"]

    prev_count = card_tx_count[card]

    rows.append({
        "isFraud": int(row["isFraud"]),
        "prev_card_tx_count": prev_count,
        "amount": row["TransactionAmt"],
    })

    # Update AFTER feature computation (NO LEAKAGE)
    card_tx_count[card] += 1

feat_df = pd.DataFrame(rows)

print("Total rows used:", len(feat_df))
print("Fraud rate:", feat_df["isFraud"].mean())

print("\n=== FRAUD TRANSACTIONS ===")
print(
    feat_df[feat_df["isFraud"] == 1][
        ["prev_card_tx_count", "amount"]
    ].describe()
)

print("\n=== NON-FRAUD TRANSACTIONS ===")
print(
    feat_df[feat_df["isFraud"] == 0][
        ["prev_card_tx_count", "amount"]
    ].describe()
)
