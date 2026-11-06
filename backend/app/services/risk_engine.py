from datetime import timedelta
from sqlalchemy.orm import Session
from .. import models

# Documented, configurable weights. Scores are capped at 100.
RULE_WEIGHTS = {
    "UNUSUAL_AMOUNT": 40,
    "HIGH_FREQUENCY": 35,
    "REGION_CHANGE": 25,
}
AMOUNT_THRESHOLD = 50000.0
FREQUENCY_LIMIT = 5
FREQUENCY_WINDOW_MINUTES = 10

def assess_transaction(db: Session, tx: models.Transaction):
    reasons = []
    triggered_rules = []
    score = 0
    if tx.amount > AMOUNT_THRESHOLD:
        score += RULE_WEIGHTS["UNUSUAL_AMOUNT"]
        triggered_rules.append("UNUSUAL_AMOUNT")
        reasons.append(f"Amount {tx.amount:.2f} exceeds configured threshold {AMOUNT_THRESHOLD:.2f}")
    window_start = tx.transaction_datetime - timedelta(minutes=FREQUENCY_WINDOW_MINUTES)
    recent_count = db.query(models.Transaction).filter(
        models.Transaction.account_id == tx.account_id,
        models.Transaction.transaction_datetime >= window_start,
        models.Transaction.transaction_datetime <= tx.transaction_datetime,
        models.Transaction.transaction_id != tx.transaction_id
    ).count()
    if recent_count >= FREQUENCY_LIMIT:
        score += RULE_WEIGHTS["HIGH_FREQUENCY"]
        triggered_rules.append("HIGH_FREQUENCY")
        reasons.append(f"At least {FREQUENCY_LIMIT} other transactions occurred within {FREQUENCY_WINDOW_MINUTES} minutes")
    if tx.region:
        previous = db.query(models.Transaction).filter(
            models.Transaction.account_id == tx.account_id,
            models.Transaction.transaction_datetime < tx.transaction_datetime,
            models.Transaction.region.isnot(None)
        ).order_by(models.Transaction.transaction_datetime.desc()).first()
        if previous and previous.region.lower() != tx.region.lower():
            score += RULE_WEIGHTS["REGION_CHANGE"]
            triggered_rules.append("REGION_CHANGE")
            reasons.append(f"Region changed from {previous.region} to {tx.region}")
    score = min(score, 100)
    return score, reasons, triggered_rules

def create_alert_if_needed(db: Session, tx: models.Transaction):
    score, reasons, triggered_rules = assess_transaction(db, tx)
    if score <= 0:
        return None
    alert = models.Alert(
        transaction_id=tx.transaction_id,
        rule_name=",".join(triggered_rules),
        risk_score=score,
        review_status="PENDING",
        reason="; ".join(reasons)
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert
