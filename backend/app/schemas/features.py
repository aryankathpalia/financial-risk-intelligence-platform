from pydantic import BaseModel
from datetime import datetime

class TransactionFeatures(BaseModel):
    transaction_id: str
    user: str
    amount: float
    timestamp: datetime

    # Rolling window features
    tx_count_1h: int
    tx_sum_1h: float

    tx_count_24h: int
    tx_avg_24h: float
