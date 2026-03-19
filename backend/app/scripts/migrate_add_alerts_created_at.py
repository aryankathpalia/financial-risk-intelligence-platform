from app.db.session import engine
from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text(
        "ALTER TABLE alerts ADD COLUMN IF NOT EXISTS analyst_decision VARCHAR;"
    ))
    conn.execute(text(
        "ALTER TABLE alerts ADD COLUMN IF NOT EXISTS analyst_reason VARCHAR;"
    ))
    conn.execute(text(
        "ALTER TABLE alerts ADD COLUMN IF NOT EXISTS resolved_at TIMESTAMPTZ;"
    ))

print("Analyst feedback columns ensured")
