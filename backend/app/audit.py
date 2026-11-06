from sqlalchemy.orm import Session
from .models import AuditLog

def record(db: Session, username: str, action: str, details: str = ""):
    db.add(AuditLog(username=username, action=action, details=details))
    db.commit()
