from app.db.models.alert import Alert

def create_alert_if_needed(db, transaction_id, score):
    if score["decision"] != "REVIEW":
        return None

    existing = (
        db.query(Alert)
        .filter(
            Alert.transaction_id == transaction_id,
            Alert.status == "pending"
        )
        .first()
    )

    if existing:
        return existing

    alert = Alert(
        transaction_id=transaction_id,
        risk_score=score["fraud_prob"],
        severity="medium",
        status="pending",
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert
