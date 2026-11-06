from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas
from ..security import get_current_user
from ..audit import record

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

@router.get("/")
def list_alerts(status: str = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(models.Alert).order_by(models.Alert.created_at.desc())
    if status:
        query = query.filter(models.Alert.review_status == status.upper())
    return [{
        "alert_id": a.alert_id, "transaction_id": a.transaction_id,
        "rule_name": a.rule_name, "risk_score": a.risk_score,
        "review_status": a.review_status, "reason": a.reason,
        "created_at": a.created_at.isoformat() if a.created_at else None
    } for a in query.limit(500).all()]

@router.patch("/{alert_id}")
def update_alert(alert_id: int, payload: schemas.AlertStatusUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    allowed = {"PENDING", "UNDER_REVIEW", "CLEARED", "CLOSED"}
    status = payload.review_status.upper()
    if status not in allowed:
        raise HTTPException(400, f"Status must be one of {sorted(allowed)}")
    alert = db.query(models.Alert).filter(models.Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(404, "Alert not found")
    alert.review_status = status
    alert.reviewed_at = datetime.utcnow()
    db.commit()
    record(db, user.username, "UPDATE_ALERT", f"alert_id={alert_id}, status={status}")
    return {"message": "Review status updated", "alert_id": alert_id, "review_status": status}
