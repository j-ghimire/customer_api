from pydantic import BaseModel, ConfigDict
from typing import Optional

# Employee schemas
class EmployeeBase(BaseModel):
    employeeNumber: int
    lastName: str
    firstName: str
    extension: str
    email: str
    officeCode: str
    reportsTo: Optional[int] = None
    jobTitle: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    extension: Optional[str] = None
    email: Optional[str] = None
    officeCode: Optional[str] = None
    reportsTo: Optional[int] = None
    jobTitle: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class EmployeeOut(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)