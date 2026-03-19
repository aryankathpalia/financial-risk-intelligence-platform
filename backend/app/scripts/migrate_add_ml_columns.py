from sqlalchemy import text
from app.db.session import engine

SQL = """
ALTER TABLE transactions
ADD COLUMN IF NOT EXISTS fraud_prob DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS anomaly_score DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS decision VARCHAR;

ALTER TABLE alerts
ADD COLUMN IF NOT EXISTS risk_score DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS severity VARCHAR,
ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'pending';
"""

with engine.connect() as conn:
    conn.execute(text(SQL))
    conn.commit()

print("✅ Migration completed successfully")
