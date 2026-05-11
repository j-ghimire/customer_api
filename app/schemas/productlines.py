from pydantic import BaseModel, ConfigDict
from typing import Optional

# ProductLine schemas
class ProductLineBase(BaseModel):
    productLine: str
    textDescription: Optional[str] = None
    htmlDescription: Optional[str] = None
    image: Optional[str | bytes] = None
    model_config = ConfigDict(from_attributes=True)

class ProductLineCreate(ProductLineBase):
    pass

class ProductLineUpdate(BaseModel):
    textDescription: Optional[str] = None
    htmlDescription: Optional[str] = None
    image: Optional[str | bytes] = None
    model_config = ConfigDict(from_attributes=True)

class ProductLineOut(ProductLineBase):
    model_config = ConfigDict(from_attributes=True)