from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models
from ..security import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
def summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    total = db.query(models.Transaction).count()
    alert_count = db.query(models.Alert).count()
    pending = db.query(models.Alert).filter(models.Alert.review_status == "PENDING").count()
    amount = db.query(func.coalesce(func.sum(models.Transaction.amount), 0)).scalar()
    distribution = db.query(models.Alert.risk_score, func.count(models.Alert.alert_id)).group_by(models.Alert.risk_score).all()
    return {
        "total_transactions": total,
        "total_alerts": alert_count,
        "pending_alerts": pending,
        "total_amount": round(float(amount), 2),
        "risk_distribution": [{"risk_score": int(score), "count": int(count)} for score, count in distribution]
    }
