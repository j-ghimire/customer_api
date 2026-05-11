from typing import List
from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..crud import employees as crud
from ..schemas import employees as schemas
from ..model import Employee

router = APIRouter()

@router.get("/employees", response_model=List[schemas.EmployeeOut])
def list_employees(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        return crud.get_employees(db, skip=skip, limit=limit)
    finally:
        db.close()

@router.get("/employees/{employeeNumber}", response_model=schemas.EmployeeOut)
def get_employee(employeeNumber: int):
    db = SessionLocal()
    try:
        employee = crud.get_employee_by_id(db, employeeNumber)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    finally:
        db.close()

@router.put("/employees/{employeeNumber}", response_model=schemas.EmployeeOut)
def update_employee(employeeNumber: int, updates: schemas.EmployeeUpdate):
    db = SessionLocal()
    try:
        db_employee = crud.update_employee(db, employeeNumber, updates.model_dump(exclude_unset=True))
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return db_employee
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@router.delete("/employees/{employeeNumber}")
def delete_employee(employeeNumber: int):
    db = SessionLocal()
    try:
        crud.delete_employee(db, employeeNumber)
        return {"message": "Employee deleted"}
    finally:
        db.close()