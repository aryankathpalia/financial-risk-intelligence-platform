import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance

from app.ml.risk_model import RiskModel
from app.db.database import SessionLocal

from app.db.models.transaction import Transaction
from app.ml.features import TransactionFeatures

def compute_feature_importance(n_samples: int = 500):
    db = SessionLocal()


    rows = (
        db.query(Transaction)
        .filter(Transaction.is_fraud.isnot(None))
        .limit(n_samples)
        .all()
    )

    if len(rows) < 50:
        return []
    

    X = []
    for tx in rows:
        feats = TransactionFeatures(tx)
        X.append(feats.vector())

    
        X = pd.DataFrame(X, columns=[
        "amount",
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
    ])
        
    model = RiskModel()
    model.load()

    result = permutation_importance(
        model.model,
        X,
        n_repeats=5,
        random_state=42,
        scoring=None
    )

    importances = result.importances_mean

    output = [
        {
            "name" : feature,
            "importance": float(score)
        }
        for feature, score in zip(X.columns, importances)
    ]

    output.sort(key=lambda x: x["importance"], reverse=True)

    return output