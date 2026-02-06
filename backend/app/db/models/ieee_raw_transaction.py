from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from datetime import datetime, timezone
import uuid


class IEEERawTransaction(Base):
    __tablename__ = "ieee_raw_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    TransactionID = Column(String, unique=True, index=True)

    TransactionAmt = Column(Float)
    ProductCD = Column(String)
    card1 = Column(Float)
    addr1 = Column(Float)
    C1 = Column(Float)
    C2 = Column(Float)
    D1 = Column(Float)

    DeviceType = Column(String)
    DeviceInfo = Column(String)

    ingested_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
