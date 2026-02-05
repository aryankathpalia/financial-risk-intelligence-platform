# app/scripts/create_paysim_test_raw.py

import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

DATA_PATH = Path("app/ml/offline/paysim_training_dataset.csv")
OUT_PATH = Path("app/ml/offline/paysim_test_raw.csv")

def main():
    print(" Loading training dataset...")
    df = pd.read_csv(DATA_PATH)

    # Separate label
    X = df.drop(columns=["label"])
    y = df["label"]

    print("Splitting train / test...")
    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    # IMPORTANT:
    # Save RAW test rows (NO labels)
    X_test.to_csv(OUT_PATH, index=False)

    print("Test split saved")
    print(f"Rows: {len(X_test)}")
    print(f"Fraud cases (hidden): {y_test.sum()}")

if __name__ == "__main__":
    main()
