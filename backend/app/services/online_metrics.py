from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import SessionLocal

from app.db.models.transaction import Transaction


def get_online_model_stats():
    db: Session = SessionLocal()

    rows = (
        db.query(
            Transaction.decision,
            func.count(Transaction.id)
        )
        .group_by(Transaction.decision)
        .all()
    )

    db.close()

    counts = {"ALLOW": 0, "REVIEW": 0, "BLOCK": 0}
    total = 0

    for decision, count in rows:
        counts[decision] = count
        total += count

    total = total or 1  # prevent division by zero

    return {
        "total": total,
        "allow_pct": round(counts["ALLOW"] / total * 100, 2),
        "review_pct": round(counts["REVIEW"] / total * 100, 2),
        "block_pct": round(counts["BLOCK"] / total * 100, 2),
    }
