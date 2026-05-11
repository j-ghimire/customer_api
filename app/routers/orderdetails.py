from typing import List
from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..crud import orderdetails as crud
from ..schemas import orderdetails as schemas
from ..model import OrderDetail

router = APIRouter()

@router.get("/orderdetails", response_model=List[schemas.OrderDetailOut])
def list_orderdetails(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        return crud.get_orderdetails(db, skip=skip, limit=limit)
    finally:
        db.close()

@router.get("/orderdetails/{ordernumber}/{productcode}", response_model=schemas.OrderDetailOut)
def get_orderdetail(ordernumber: int, productcode: str):
    db = SessionLocal()
    try:
        orderdetail = crud.get_orderdetail_by_id(db, ordernumber, productcode)
        if not orderdetail:
            raise HTTPException(status_code=404, detail="OrderDetail not found")
        return orderdetail
    finally:
        db.close()

@router.put("/orderdetails/{ordernumber}/{productcode}", response_model=schemas.OrderDetailOut)
def update_orderdetail(ordernumber: int, productcode: str, updates: schemas.OrderDetailUpdate):
    db = SessionLocal()
    try:
        db_orderdetail = crud.update_orderdetail(db, ordernumber, productcode, updates.model_dump(exclude_unset=True))
        if not db_orderdetail:
            raise HTTPException(status_code=404, detail="OrderDetail not found")
        return db_orderdetail
    finally:
        db.close()

@router.delete("/orderdetails/{ordernumber}/{productcode}")
def delete_orderdetail(ordernumber: int, productcode: str):
    db = SessionLocal()
    try:
        crud.delete_orderdetail(db, ordernumber, productcode)
        return {"message": "OrderDetail deleted"}
    finally:
        db.close()