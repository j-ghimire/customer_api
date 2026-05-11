from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

# Order schemas
class OrderBase(BaseModel):
    orderNumber: int
    orderDate: Optional[date] = None
    requiredDate: Optional[date] = None
    shippedDate: Optional[date] = None
    status: Optional[str] = None
    comments: Optional[str] = None
    customerNumber: int

class OrderCreate(BaseModel):
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: str
    comments: Optional[str] = None
    customerNumber: int

class OrderUpdate(BaseModel):
    orderDate: Optional[date] = None
    requiredDate: Optional[date] = None
    shippedDate: Optional[date] = None
    status: Optional[str] = None
    comments: Optional[str] = None
    customerNumber: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class OrderOut(OrderBase):
    model_config = ConfigDict(from_attributes=True)

class OrderWithDetails(OrderOut):
    orderdetails: List['OrderDetailOut'] = []

# Forward reference
from .orderdetails import OrderDetailOut

OrderWithDetails.model_rebuild()