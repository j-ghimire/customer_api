from pydantic import BaseModel, ConfigDict
from typing import Optional

# Product schemas
class ProductBase(BaseModel):
    productCode: str
    productName: str
    productLine: str
    productScale: str
    productVendor: str
    productDescription: str
    quantityInStock: int
    buyPrice: float
    MSRP: float

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    productName: Optional[str] = None
    productLine: Optional[str] = None
    productScale: Optional[str] = None
    productVendor: Optional[str] = None
    productDescription: Optional[str] = None
    quantityInStock: Optional[int] = None
    buyPrice: Optional[float] = None
    MSRP: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)