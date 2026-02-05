from pydantic import BaseModel
from typing import List
from typing import Literal

class Alert(BaseModel):
    alert_id: str
    transaction_id: str
    user: str
    severity: str
    decision: str
    reasons: List[str]
    risk_score: float
    status: str = "pending"
    decision: Literal["APPROVE", "CONFIRM_FRAUD"]
