from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

# Payment schemas
class PaymentBase(BaseModel):
    customerNumber: int
    checkNumber: str
    paymentDate: Optional[date] = None
    amount: float

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    paymentDate: Optional[date] = None
    amount: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

class PaymentOut(PaymentBase):
    model_config = ConfigDict(from_attributes=True)