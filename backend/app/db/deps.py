from app.db.database import SessionLocal

from sqlalchemy import text

def get_db():
    db = SessionLocal()
    db.execute(text("SET search_path TO railway, public"))
    try:
        yield db
    finally:
        db.close()
