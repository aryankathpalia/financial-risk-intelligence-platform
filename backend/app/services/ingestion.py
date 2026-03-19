from uuid import uuid4
from datetime import datetime, timezone
import time
import math

from sqlalchemy.orm import Session

from app.db.models.transaction import Transaction
from app.ml.pipeline import RiskPipeline

               
# GLOBAL, REUSED PIPELINE (LOADED ONCE)
               
pipeline = RiskPipeline()

               
# INGESTION TUNING (REAL-TIME SIMULATION)
               
CHUNK_SIZE = 25          # smaller chunk = smoother UI growth
YIELD_SECONDS = 0.05     # ~20 commits/sec (realistic)


def _clean(v):
    """
    DB-safe value cleaning
    """
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    return v


def ingest_ieee_rows(db: Session, rows: list):
    """
    Production-grade IEEE ingestion

    Guarantees:
    - UUID is the ONLY system identity
    - IEEE TransactionID is metadata only
    - Idempotent on IEEE TransactionID
    - Chunked commits (real-time simulation)
    - ML scoring happens ONCE (ingestion-time)
    """

    total = len(rows)

    for start in range(0, total, CHUNK_SIZE):
        chunk = rows[start : start + CHUNK_SIZE]

        for row in chunk:
            source_id = str(row["TransactionID"])


            # 1️ IDEMPOTENCY (IEEE DATASET ID)

            exists = (
                db.query(Transaction)
                .filter(Transaction.TransactionID == source_id)
                .first()
            )
            if exists:
                continue

                
            # 2️ CREATE TRANSACTION (UUID)
                
            tx = Transaction(
                id=uuid4(),
                TransactionID=source_id,
                ingested_at=datetime.now(timezone.utc),

                TransactionAmt=_clean(row.get("TransactionAmt")),
                ProductCD=row.get("ProductCD"),

                card1=_clean(row.get("card1")),
                addr1=_clean(row.get("addr1")),

                C1=_clean(row.get("C1")),
                C2=_clean(row.get("C2")),
                D1=_clean(row.get("D1")),

                DeviceType=row.get("DeviceType"),
                DeviceInfo=row.get("DeviceInfo"),

                **{
                    f"id_{i:02d}": _clean(row.get(f"id_{i:02d}"))
                    for i in range(1, 39)
                },
            )

            db.add(tx)
            db.flush()  # UUID assigned here (NO COMMIT YET)

                
            # 3️ ML SCORING (ONCE, EVER)
                
            result = pipeline.score(tx)

            tx.fraud_prob = result["fraud_prob"]
            tx.anomaly_score = result.get("anomaly_score")
            tx.decision = result["decision"]
            tx.severity = result.get("severity")
            tx.decision_reasons = result.get("reasons", [])
            tx.shap_values = result.get("shap_values", [])



                 
        # 4️ COMMIT CHUNK → UI CAN SEE IT
                 
        db.commit()

                 
        # 5️ YIELD CPU (SIMULATES STREAMING)
                 
        time.sleep(YIELD_SECONDS)
