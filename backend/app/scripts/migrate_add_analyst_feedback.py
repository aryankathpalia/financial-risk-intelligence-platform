# scripts/migrate_add_analyst_feedback.py
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)
