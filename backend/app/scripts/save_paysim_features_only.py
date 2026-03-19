import pandas as pd
from pathlib import Path

DATA_PATH = Path("app/ml/offline/paysim_training_dataset.csv")
OUT_PATH = Path("app/ml/offline/paysim_features_only.csv")

def main():
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["label"])
    X.to_csv(OUT_PATH, index=False)

    print("Saved PaySim features-only file")
    print("Shape:", X.shape)

if __name__ == "__main__":
    main()
