from sqlalchemy import text
from app.db.session import engine

SQL = """
ALTER TABLE alerts
ADD COLUMN IF NOT EXISTS analyst_decision VARCHAR,
ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMPTZ;
"""

with engine.connect() as conn:
    conn.execute(text(SQL))
    conn.commit()

print("Analyst columns added")
