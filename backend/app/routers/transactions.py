from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv, io
from ..database import get_db
from .. import models, schemas
from ..security import get_current_user
from ..services.transaction_service import create_transaction
from ..audit import record

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])

@router.get("/", response_model=List[schemas.TransactionOut])
def list_transactions(limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Transaction).order_by(models.Transaction.transaction_datetime.desc()).limit(min(limit, 500)).all()

@router.post("/", response_model=schemas.TransactionOut)
def add_transaction(payload: schemas.TransactionCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        tx = create_transaction(db, payload)
    except ValueError as exc:
        raise HTTPException(404, str(exc))
    record(db, user.username, "CREATE_TRANSACTION", f"transaction_id={tx.transaction_id}")
    return tx

@router.post("/import")
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Upload a CSV file")
    content = (await file.read()).decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))
    created, errors = 0, []
    for line_no, row in enumerate(reader, start=2):
        try:
            payload = schemas.TransactionCreate(
                account_id=int(row["account_id"]),
                transaction_datetime=row["transaction_datetime"],
                amount=float(row["amount"]),
                transaction_type=row["transaction_type"],
                channel=row["channel"],
                region=row.get("region") or None
            )
            create_transaction(db, payload)
            created += 1
        except Exception as exc:
            db.rollback()
            errors.append({"line": line_no, "error": str(exc)})
    record(db, user.username, "IMPORT_TRANSACTIONS", f"created={created}, errors={len(errors)}")
    return {"created": created, "errors": errors}
