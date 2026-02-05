import pandas as pd


def build_synthetic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adapt synthetic fraud dataset to PaySim feature contract.
    Training model & scaler remain unchanged.
    """

      
    # Sort by time surrogate
      
    df = df.sort_values("hour").copy()

      
    # USER-LEVEL FEATURES
      
    df["user_tx_count"] = df.groupby("user_id").cumcount() + 1

    df["user_avg_amount"] = (
        df.groupby("user_id")["amount"]
        .expanding()
        .mean()
        .reset_index(level=0, drop=True)
    )

      
    # DESTINATION / MERCHANT FEATURES
      
    df["dest_tx_count"] = df.groupby("merchant_category").cumcount() + 1

    df["dest_fraud_rate"] = (
        df.groupby("merchant_category")["is_fraud"]
        .expanding()
        .mean()
        .reset_index(level=0, drop=True)
    )

      
    # BALANCE DELTAS (NOT AVAILABLE)
      
    df["balance_delta_orig"] = 0.0
    df["balance_delta_dest"] = 0.0

      
    # TRANSACTION TYPE FLAGS
      
    df["type_CASH_OUT"] = (df["transaction_type"] == "ATM").astype(int)

    df["type_DEBIT"] = df["transaction_type"].isin(
        ["POS", "QR"]
    ).astype(int)

    df["type_PAYMENT"] = (df["transaction_type"] == "Online").astype(int)

    df["type_TRANSFER"] = 0  # no true transfer equivalent

      
    # FEATURE CONTRACT FIX
      
    # PaySim scaler was trained with capital-A "Amount"
    df["Amount"] = df["amount"]

      
    # FINAL FEATURE ORDER (CRITICAL)
      
    feature_cols = [
        "Amount",
        "balance_delta_orig",
        "balance_delta_dest",
        "user_tx_count",
        "user_avg_amount",
        "dest_tx_count",
        "dest_fraud_rate",
        "type_CASH_OUT",
        "type_DEBIT",
        "type_PAYMENT",
        "type_TRANSFER",
    ]

    return df[feature_cols]