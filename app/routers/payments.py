from typing import List
from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..crud import payments as crud
from ..schemas import payments as schemas
from ..model import Payment

router = APIRouter()

@router.get("/payments", response_model=List[schemas.PaymentOut])
def list_payments(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        return crud.get_payments(db, skip=skip, limit=limit)
    finally:
        db.close()

@router.post("/payments", response_model=schemas.PaymentOut)
def create_payment(payment: schemas.PaymentCreate):
    db = SessionLocal()
    try:
        db_payment = crud.create_payment(db, payment.model_dump())
        return db_payment
    finally:
        db.close()

@router.get("/payments/{customerNumber}/{checkNumber}", response_model=schemas.PaymentOut)
def get_payment(customerNumber: int, checkNumber: str):
    db = SessionLocal()
    try:
        payment = crud.get_payment_by_id(db, customerNumber, checkNumber)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
    finally:
        db.close()

@router.put("/payments/{customerNumber}/{checkNumber}", response_model=schemas.PaymentOut)
def update_payment(customerNumber: int, checkNumber: str, updates: schemas.PaymentUpdate):
    db = SessionLocal()
    try:
        db_payment = crud.update_payment(db, customerNumber, checkNumber, updates.model_dump(exclude_unset=True))
        if not db_payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return db_payment
    finally:
        db.close()

@router.delete("/payments/{customerNumber}/{checkNumber}")
def delete_payment(customerNumber: int, checkNumber: str):
    db = SessionLocal()
    try:
        result = crud.delete_payment(db, customerNumber, checkNumber)
        if result is None:
            raise HTTPException(status_code=404, detail="Payment not found")
        return {"message": "Payment deleted"}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    finally:
        db.close()

