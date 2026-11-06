from sqlalchemy.orm import Session
from .. import models, schemas
from .risk_engine import create_alert_if_needed

def create_transaction(db: Session, payload: schemas.TransactionCreate):
    account = db.query(models.Account).filter(models.Account.account_id == payload.account_id).first()
    if not account:
        raise ValueError("Account does not exist")
    tx = models.Transaction(**payload.model_dump())
    db.add(tx)
    db.commit()
    db.refresh(tx)
    create_alert_if_needed(db, tx)
    return tx
