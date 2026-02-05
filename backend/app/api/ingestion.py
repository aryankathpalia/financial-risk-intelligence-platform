from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.ingestion import ingest_ieee_rows
from app.data.ieee_loader import load_ieee_test_rows

router = APIRouter()


@router.post("/start")
def start_ingestion(
    limit: int = 1000,
    db: Session = Depends(get_db),
):
    """
    Start IEEE test ingestion into the system.
    Batch ingestion (NOT async streaming).
    """

    rows = load_ieee_test_rows(limit=limit)

    ingest_ieee_rows(db, rows)

    return {
        "status": "ieee_ingestion_complete",
        "rows_ingested": len(rows),
    }
