from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class AlertFeedback(BaseModel):
    alert_id: UUID
    is_fraud: bool
    analyst: str
    timestamp: datetime
