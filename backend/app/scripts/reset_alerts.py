from app.db.database import engine
from app.db.models.alert import Alert

print("Dropping alerts table...")
Alert.__table__.drop(engine, checkfirst=True)

print("Recreating alerts table...")
Alert.__table__.create(engine)

print("Alerts table reset complete")
