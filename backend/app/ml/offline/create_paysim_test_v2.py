import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

DATA_PATH = Path("app/ml/offline/paysim_training_dataset.csv")

TEST_FEATURES_PATH = Path("app/ml/offline/paysim_test_v2.csv")
TEST_LABELS_PATH   = Path("app/ml/offline/paysim_test_labels_v2.csv")

TEST_SIZE = 0.2
RANDOM_STATE = 42


def main():
    print("📦 Loading FEATURE-ENGINEERED training dataset...")
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["label"])
    y = df["label"]

    print("✂️ Splitting train / test...")
    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    X_test.to_csv(TEST_FEATURES_PATH, index=False)
    y_test.to_csv(TEST_LABELS_PATH, index=False)

    print("Test split v2 created")
    print("Rows:", len(X_test))
    print("Fraud cases:", y_test.sum())


if __name__ == "__main__":
    main()