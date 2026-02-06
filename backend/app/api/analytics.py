from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.db.deps import get_db
from app.db.models.transaction import Transaction

router = APIRouter(tags=["Analytics"])


@router.get("/score-distribution")
def score_distribution(db: Session = Depends(get_db)):
    """
    Returns 10 risk-score buckets over ALL transactions.
    Risk score = max(fraud_prob, anomaly_score)
    """

    # Clamp risk to [0,1] and bucket into 10 bins
    bucket_expr = func.floor(
        func.least(
            func.greatest(
                func.coalesce(
                    func.greatest(Transaction.fraud_prob, Transaction.anomaly_score),
                    0.0
                ),
                0.0
            ),
            0.999
        ) * 10
    )

    rows = (
        db.query(
            bucket_expr.label("bucket"),
            func.count().label("count")
        )
        .group_by("bucket")
        .all()
    )

    buckets = [0] * 10
    for row in rows:
        buckets[int(row.bucket)] = row.count

    return {
        "buckets": buckets
    }
