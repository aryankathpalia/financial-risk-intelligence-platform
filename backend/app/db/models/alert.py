from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.sql import func
import uuid

from app.db.base import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = Column(String, index=True, nullable=False)

    risk_score = Column(Float, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, default="pending")

    analyst_decision = Column(String, nullable=True)
    analyst_reason = Column(String, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
