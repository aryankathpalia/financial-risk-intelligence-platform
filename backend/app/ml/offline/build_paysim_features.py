# app/ml/offline/build_paysim_features.py

import pandas as pd
from pathlib import Path
import joblib
from collections import defaultdict

# --------------------------------------------------
# PATHS
# --------------------------------------------------

DATA_PATH = Path(
    r"C:\Users\NewUser123\Downloads\PaySim_Synthetic_Financial_Dataset.csv"
)

OUTPUT_PATH = Path(
    "app/ml/offline/paysim_training_dataset.csv"
)

ARTIFACT_DIR = Path("app/ml/artifacts")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_paysim():
    print(" Loading PaySim dataset...")
    df = pd.read_csv(DATA_PATH)
    print("Shape:", df.shape)
    return df

# --------------------------------------------------
# FEATURE ENGINEERING (STREAMING, CAUSAL, SAFE)
# --------------------------------------------------

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    print("Building strictly causal features (streaming-safe)...")

     
    # 1. Sort by time (CRITICAL)
     

    df = df.sort_values("step").reset_index(drop=True)

     
    # 2. Transaction-level deltas
     

    df["balance_delta_orig"] = df["oldbalanceOrg"] - df["newbalanceOrig"]
    df["balance_delta_dest"] = df["newbalanceDest"] - df["oldbalanceDest"]

     
    # 3. Encode transaction type
     

    type_dummies = pd.get_dummies(
        df["type"],
        prefix="type",
        drop_first=True
    )
    df = pd.concat([df, type_dummies], axis=1)

     
    # 4. STREAMING USER STATE (O(N), NO LEAKAGE)
     

    user_count = defaultdict(int)
    user_sum = defaultdict(float)

    user_tx_count = []
    user_avg_amount = []

    for orig, amt in zip(df["nameOrig"], df["amount"]):
        count = user_count[orig]
        total = user_sum[orig]

        user_tx_count.append(count)
        user_avg_amount.append(total / count if count > 0 else 0.0)

        user_count[orig] += 1
        user_sum[orig] += amt

    df["user_tx_count"] = user_tx_count
    df["user_avg_amount"] = user_avg_amount

     
    # 5. GLOBAL AMOUNT STATS (TRAINING ONLY)
     

    amount_mean = df["amount"].mean()
    amount_std = df["amount"].std()

    joblib.dump(
        {"mean": amount_mean, "std": amount_std},
        ARTIFACT_DIR / "amount_stats.joblib"
    )

    df["amount_zscore_global"] = (
        (df["amount"] - amount_mean) / amount_std
    )

     
    # 6. FIRST TX HIGH AMOUNT FLAG
     

    df["is_first_tx_high_amount"] = (
        (df["user_tx_count"] == 0) &
        (df["amount_zscore_global"] > 1.5)
    ).astype(int)

     
    # 7. FINAL DATASET (ONLINE FEATURES ONLY)
     

    feature_cols = [
        "amount",
        "balance_delta_orig",
        "balance_delta_dest",
        "user_tx_count",
        "user_avg_amount",
        "is_first_tx_high_amount",
    ] + list(type_dummies.columns)

    final_df = df[feature_cols].fillna(0).copy()
    final_df["label"] = df["isFraud"].astype(int)

    print("Final training shape:", final_df.shape)
    print("Fraud distribution:")
    print(final_df["label"].value_counts())

    return final_df


# MAIN

def main():
    df = load_paysim()
    training_df = build_features(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    training_df.to_csv(OUTPUT_PATH, index=False)

    print("Saved training dataset to:", OUTPUT_PATH)
    print("Saved amount stats to:", ARTIFACT_DIR / "amount_stats.joblib")

if __name__ == "__main__":
    main()