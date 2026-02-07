from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models.transaction import Transaction

router = APIRouter()


def decision_to_severity(decision: str) -> str:
    return {
        "BLOCK": "high",
        "REVIEW": "medium",
        "ALLOW": "low",
    }.get(decision, "low")


@router.get("", include_in_schema=True)
def list_transactions(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 15,
):
    offset = (page - 1) * page_size

    total = db.query(Transaction).count()

    transactions = (
        db.query(Transaction)
        .order_by(Transaction.ingested_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "items": [
            {
                "id": str(tx.id),

                # UI-only synthetic identity (NOT stored in DB)
                "user_id": f"user_{tx.id.hex[:6]}",

                # UI-only placeholder
                "merchant": "SIM_DEST",

                "amount": tx.TransactionAmt,

                "ingested_at": tx.ingested_at,
                "fraud_prob": tx.fraud_prob,
                "anomaly_score": tx.anomaly_score,
                "decision": tx.decision,
                "severity": decision_to_severity(tx.decision),
            }
            for tx in transactions
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


import uuid

@router.get("/{transaction_id}")
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    try:
        tx_id = uuid.UUID(transaction_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid transaction id")

    tx = (
        db.query(Transaction)
        .filter(Transaction.id == tx_id)   
        .first()
    )

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return {
        "id": str(tx.id),
        "user_id": f"user_{tx.id.hex[:6]}",
        "merchant": "SIM_DEST",
        "amount": tx.TransactionAmt,
        "ingested_at": tx.ingested_at,
        "fraud_prob": tx.fraud_prob,
        "anomaly_score": tx.anomaly_score,
        "decision": tx.decision,
        "shap_values": tx.shap_values or [],

    }
