from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class TransactionCreate(BaseModel):
    account_id: int
    transaction_datetime: datetime
    amount: float = Field(gt=0)
    transaction_type: str = Field(min_length=2, max_length=30)
    channel: str = Field(min_length=2, max_length=30)
    region: Optional[str] = None

class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transaction_id: int
    account_id: int
    transaction_datetime: datetime
    amount: float
    transaction_type: str
    channel: str
    region: Optional[str]

class AlertStatusUpdate(BaseModel):
    review_status: str

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=8)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
