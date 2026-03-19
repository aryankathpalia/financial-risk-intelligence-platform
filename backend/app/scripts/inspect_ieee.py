import os
import pandas as pd

              
# CONFIG
              
CSV_PATH = "app/data/ieee/train_transaction.csv"

              
# DEBUG: confirm working directory
              
print("Current working directory:")
print(os.getcwd())
print("-" * 60)

              
# CHECK FILE EXISTS
              
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(
        f"File not found: {CSV_PATH}\n"
        "Check that the IEEE dataset is placed correctly."
    )

print(f"Found file: {CSV_PATH}")
print("-" * 60)

              
# LOAD DATA
              
df = pd.read_csv(CSV_PATH)

              
# BASIC INSPECTION (NO ML YET)
              
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("-" * 60)

print("Column names:")
for col in df.columns:
    print(col)

print("-" * 60)
print("Sample rows:")
print(df.head())