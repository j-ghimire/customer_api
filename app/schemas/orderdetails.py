from pydantic import BaseModel, ConfigDict
from typing import Optional

# OrderDetail schemas
class OrderDetailBase(BaseModel):
    orderNumber: int
    productCode: str
    quantityOrdered: int
    priceEach: float
    orderLineNumber: int

class OrderDetailCreate(BaseModel):
    orderNumber: int
    productCode: str
    quantityOrdered: int
    priceEach: float
    orderLineNumber: int

class OrderDetailUpdate(BaseModel):
    quantityOrdered: Optional[int] = None
    priceEach: Optional[float] = None
    orderLineNumber: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class OrderDetailOut(OrderDetailBase):
    model_config = ConfigDict(from_attributes=True)