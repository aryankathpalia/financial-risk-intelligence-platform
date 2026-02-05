# app/api/alerts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Literal

from app.db.deps import get_db
from app.db.models.transaction import Transaction

router = APIRouter()


def decision_to_severity(decision: str) -> str:
    return {
        "BLOCK": "high",
        "REVIEW": "medium",
        "ALLOW": "low",
    }.get(decision, "low")


class ResolveAlertPayload(BaseModel):
    decision: Literal["APPROVE", "CONFIRM_FRAUD"]
    reason: str | None = None


@router.get("/")
def get_alerts(db: Session = Depends(get_db)):
    txs = (
        db.query(Transaction)
        .filter(Transaction.decision.in_(["REVIEW", "BLOCK"]))
        .filter(Transaction.analyst_decision.is_(None))
        .order_by(Transaction.ingested_at.desc())
        .limit(50)
        .all()
    )

    return [
    {
        "id": str(tx.id),
        "transaction_id": str(tx.id),
        "user_id": f"user_{tx.id.hex[:6]}",
        "risk_score": tx.fraud_prob or 0.0,
        "severity": tx.severity,                  
        "decision": tx.decision,                  
        "anomaly_score": tx.anomaly_score,        
        "reasons": tx.decision_reasons or [],     
        "status": "pending",
        "created_at": tx.ingested_at.isoformat(),
    }
    for tx in txs
]



@router.post("/{transaction_id}/resolve")
def resolve_transaction(
    transaction_id: str,
    payload: ResolveAlertPayload,
    db: Session = Depends(get_db),
):
    tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not tx:
        raise HTTPException(404, "Transaction not found")

    tx.analyst_decision = payload.decision
    tx.analyst_reason = payload.reason
    tx.labeled_at = datetime.now(timezone.utc)

    db.commit()

    return {
        "transaction_id": str(tx.id),
        "status": "resolved",
    }
