import pandas as pd
from collections import defaultdict

CSV_PATH = "app/data/PaySim_Synthetic_Financial_Dataset.csv"

# Load data
df = pd.read_csv(CSV_PATH)

# Use enough rows for signal
df = df.iloc[:50000]

# Keep only meaningful fraud types
df = df[df["type"].isin(["TRANSFER", "CASH_OUT"])]

# Sort by event time
df = df.sort_values("step")

user_tx_count = defaultdict(int)
rows = []

for _, row in df.iterrows():
    user = row["nameOrig"]

    prev_count = user_tx_count[user]

    rows.append({
        "isFraud": int(row["isFraud"]),
        "prev_user_tx_count": prev_count,
        "amount": row["amount"]
    })

    # Update AFTER computing features (NO LEAKAGE)
    user_tx_count[user] += 1

feat_df = pd.DataFrame(rows)

print("Total rows used:", len(feat_df))

print("\nFRAUD TRANSACTIONS:")
print(
    feat_df[feat_df["isFraud"] == 1][
        ["prev_user_tx_count", "amount"]
    ].describe()
)

print("\nNON-FRAUD TRANSACTIONS:")
print(
    feat_df[feat_df["isFraud"] == 0][
        ["prev_user_tx_count", "amount"]
    ].describe()
)
