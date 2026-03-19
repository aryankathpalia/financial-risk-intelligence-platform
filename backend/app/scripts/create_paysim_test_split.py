import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

DATA_PATH = Path("app/ml/offline/paysim_training_dataset.csv")
TEST_FEATURES_PATH = Path("app/ml/offline/paysim_test.csv")
TEST_LABELS_PATH = Path("app/ml/offline/paysim_test_labels.csv")

TEST_SIZE = 0.2
RANDOM_STATE = 42


def main():
    print("Loading training dataset...")
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["label"])
    y = df["label"]

    print("Splitting train / test...")
    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE
    )

    # Save test features ONLY (what model will see in production)
    X_test.to_csv(TEST_FEATURES_PATH, index=False)

    # Save labels separately (offline evaluation only)
    y_test.to_csv(TEST_LABELS_PATH, index=False)

    print("Test split created")
    print("Test feature rows:", len(X_test))
    print("Test fraud cases:", y_test.sum())


if __name__ == "__main__":
    main()
