import joblib
import numpy as np
from sklearn.ensemble import IsolationForest
from app.db.session import SessionLocal
from app.db.models.transaction import Transaction
from app.ml.anomaly.isolation_forest import IF_FEATURES, ARTIFACT_PATH


def train():
    db = SessionLocal()

    rows = db.query(Transaction).limit(200_000).all()

    X = []
    for tx in rows:
        X.append([
            getattr(tx, f, 0.0) or 0.0
            for f in IF_FEATURES
        ])

    X = np.array(X)

    model = IsolationForest(
        n_estimators=300,
        contamination=0.02,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X)

    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, ARTIFACT_PATH)

    print("✅ Isolation Forest trained and saved")


if __name__ == "__main__":
    train()
