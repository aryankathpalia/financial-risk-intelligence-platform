# app.api.scoring.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.db.deps import get_db
from app.db.models.transaction import Transaction
from app.ml.pipeline import RiskPipeline

router = APIRouter()
pipeline = RiskPipeline()


# -----------------------------
# Runtime scoring (NO DB writes)
# -----------------------------
@router.post("/score/{transaction_id}")
def score_transaction(transaction_id: str, db: Session = Depends(get_db)):
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

    result = pipeline.score(tx)

    return {
        "transaction_id": str(tx.id),
        "amount": tx.TransactionAmt,
        **result,
    }


# -----------------------------
# Persist scoring (DB writes)
# -----------------------------
@router.post("/persist/{transaction_id}")
def persist_transaction(transaction_id: str, db: Session = Depends(get_db)):
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

    result = pipeline.score(tx)

    tx.fraud_prob = result["fraud_prob"]
    tx.anomaly_score = result.get("anomaly_score")
    tx.decision = result["decision"]
    tx.severity = result["severity"]       
    tx.decision_reasons = result.get("reasons", [])  


    db.commit()

    return {
        "status": "persisted",
        "transaction_id": str(tx.id),
        "decision": tx.decision,
    }
