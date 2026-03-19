from pydantic import BaseModel

class DashboardKPIResponse(BaseModel):
    total_transactions: int
    flagged_transactions: int
    high_severity_alerts: int
    flag_rate: float
