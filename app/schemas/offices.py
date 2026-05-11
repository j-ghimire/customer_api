from pydantic import BaseModel, ConfigDict
from typing import Optional

# Office schemas
class OfficeBase(BaseModel):
    officeCode: str
    city: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    state: Optional[str] = None
    country: str
    postalCode: str
    territory: str

class OfficeCreate(OfficeBase):
    pass

class OfficeUpdate(BaseModel):
    city: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[str] = None
    territory: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OfficeOut(OfficeBase):
    model_config = ConfigDict(from_attributes=True)