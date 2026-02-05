from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.db.models.transaction import Transaction


def get_online_model_stats():
    db: Session = SessionLocal()

    total = db.query(func.count(Transaction.id)).scalar() or 1

    allow = db.query(func.count(Transaction.id)) \
        .filter(Transaction.decision == "ALLOW") \
        .scalar()

    review = db.query(func.count(Transaction.id)) \
        .filter(Transaction.decision == "REVIEW") \
        .scalar()

    block = db.query(func.count(Transaction.id)) \
        .filter(Transaction.decision == "BLOCK") \
        .scalar()

    db.close()

    return {
        "total": total,
        "allow_pct": round(allow / total * 100, 2),
        "review_pct": round(review / total * 100, 2),
        "block_pct": round(block / total * 100, 2),
    }
