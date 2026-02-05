# app/api/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.deps import get_db
from app.db.models.transaction import Transaction
from app.schemas.dashboard import DashboardKPIResponse

router = APIRouter()


@router.get("/kpis", response_model=DashboardKPIResponse)
def get_dashboard_kpis(db: Session = Depends(get_db)):
    # app/api/dashboard.py

    total_transactions = db.query(func.count(Transaction.id)).scalar()

    flagged_transactions = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.decision.in_(["REVIEW", "BLOCK"]))
        .scalar()
    )

    high_severity_alerts = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.decision == "BLOCK")
        .scalar()
    )

    flag_rate = (
        flagged_transactions / total_transactions
        if total_transactions > 0
        else 0.0
    )

    return {
        "total_transactions": total_transactions,
        "flagged_transactions": flagged_transactions,
        "high_severity_alerts": high_severity_alerts,
        "flag_rate": flag_rate,
    }

    
@router.get("/risk-stats")
def get_risk_stats(db: Session = Depends(get_db)):
    txs = (
        db.query(
            Transaction.ingested_at,
            Transaction.fraud_prob,
            Transaction.anomaly_score,
        )
        .order_by(Transaction.ingested_at.desc())
        .limit(200)   
        .all()
    )

    data = []
    for tx in reversed(txs):
        risk = max(tx.fraud_prob or 0, tx.anomaly_score or 0)
        data.append({
            "timestamp": tx.ingested_at.isoformat(),
            "risk_score": round(risk * 100, 2),  
        })

    return data
