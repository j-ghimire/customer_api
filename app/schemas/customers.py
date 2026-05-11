from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

# Customer schemas
class CustomerBase(BaseModel):
    customerNumber:int
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[float] = None

class CustomerCreate(BaseModel):
    customerNumber: int
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[float] = None

class CustomerUpdate(BaseModel):
    customerName: Optional[str] = None
    contactLastName: Optional[str] = None
    contactFirstName: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

class CustomerOut(CustomerBase):
    customerNumber: int
    model_config = ConfigDict(from_attributes=True)

# Additional schemas for relationships
class OrderWithDetails(BaseModel):
    orderNumber: int
    orderDate: Optional[date] = None
    requiredDate: Optional[date] = None
    shippedDate: Optional[date] = None
    status: Optional[str] = None
    comments: Optional[str] = None
    customerNumber: int
    orderdetails: List['OrderDetailOut'] = []

class CustomerDetailComplete(CustomerOut):
    orders: List[OrderWithDetails] = []
    payments: List['PaymentOut'] = []

# Forward references
from .orderdetails import OrderDetailOut
from .payments import PaymentOut

CustomerDetailComplete.model_rebuild()