from typing import List
from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..crud import orders as crud
from ..schemas import orders as schemas
from ..model import Order

router = APIRouter()

@router.get("/orders", response_model=List[schemas.OrderOut])
def list_orders(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        return crud.get_orders(db, skip=skip, limit=limit)
    finally:
        db.close()

@router.get("/orders/{ordernumber}", response_model=schemas.OrderOut)
def get_order(ordernumber: int):
    db = SessionLocal()
    try:
        order = crud.get_order_by_id(db, ordernumber)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    finally:
        db.close()

@router.put("/orders/{ordernumber}", response_model=schemas.OrderOut)
def update_order(ordernumber: int, updates: schemas.OrderUpdate):
    db = SessionLocal()
    try:
        db_order = crud.update_order(db, ordernumber, updates.model_dump(exclude_unset=True))
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return db_order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()