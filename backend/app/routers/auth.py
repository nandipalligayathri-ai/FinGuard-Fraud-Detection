from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..security import hash_password, verify_password, create_access_token
from ..audit import record

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.TokenResponse)
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(409, "Username already exists")
    user = models.User(username=payload.username, password_hash=hash_password(payload.password))
    db.add(user); db.commit()
    record(db, payload.username, "REGISTER", "New local demo user registered")
    return {"access_token": create_access_token(payload.username)}

@router.post("/login", response_model=schemas.TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Incorrect username or password")
    record(db, user.username, "LOGIN", "Successful login")
    return {"access_token": create_access_token(user.username)}
