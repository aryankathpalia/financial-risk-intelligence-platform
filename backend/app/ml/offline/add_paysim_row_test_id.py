# app/ml/offline/add_paysim_row_test_id.py

import pandas as pd
from pathlib import Path

# IMPORTANT: point to app/data
BASE_DIR = Path(__file__).resolve().parents[2] / "data"

FILES = [
    "paysim_features_only.csv",   
]

def add_row_id(path: Path):
    df = pd.read_csv(path)

    if "paysim_row_test_id" in df.columns:
        print(f"✅ Already exists: {path.name}")
        return

    df.insert(0, "paysim_row_test_id", range(len(df)))
    df.to_csv(path, index=False)

    print(f"🆕 Added paysim_row_test_id → {path.name}")

def main():
    for fname in FILES:
        path = BASE_DIR / fname
        if not path.exists():
            print(f"❌ Missing file: {path}")
            continue
        add_row_id(path)

    print("\n✅ Done")

if __name__ == "__main__":
    main()