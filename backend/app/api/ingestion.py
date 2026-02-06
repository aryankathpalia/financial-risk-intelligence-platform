from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.deps import get_db
from app.services.ingestion import ingest_ieee_rows

router = APIRouter()

@router.post("/start")
def start_ingestion(
    limit: int = 2000,
    db: Session = Depends(get_db),
):
    """
    Ingest rows FROM RAW TABLE into ML pipeline
    """

    rows = db.execute(
        text("""
            SELECT
                "TransactionID",
                "TransactionAmt",
                "ProductCD",
                card1,
                addr1,
                "C1",
                "C2",
                "D1",
                "DeviceType",
                "DeviceInfo"
            FROM railway.ieee_raw_transactions
            ORDER BY ingested_at ASC
            LIMIT :limit
        """),
        {"limit": limit}
    ).mappings().all()

    ingest_ieee_rows(db, rows)

    return {
        "status": "db_ingestion_complete",
        "rows_fetched": len(rows),
    }
