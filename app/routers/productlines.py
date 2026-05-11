from typing import List
from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..crud import productlines as crud
from ..schemas import productlines as schemas
from ..model import ProductLine

router = APIRouter()

@router.get("/productlines", response_model=List[schemas.ProductLineOut])
def list_productlines(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        return crud.get_productlines(db, skip=skip, limit=limit)
    finally:
        db.close()

@router.get("/productlines/{productline}", response_model=schemas.ProductLineOut)
def get_productline(productline: str):
    db = SessionLocal()
    try:
        productline_obj = crud.get_productline_by_id(db, productline)
        if not productline_obj:
            raise HTTPException(status_code=404, detail="ProductLine not found")
        return productline_obj
    finally:
        db.close()

@router.put("/productlines/{productline}", response_model=schemas.ProductLineOut)
def update_productline(productline: str, updates: schemas.ProductLineUpdate):
    db = SessionLocal()
    try:
        db_productline = crud.update_productline(db, productline, updates.model_dump(exclude_unset=True))
        if not db_productline:
            raise HTTPException(status_code=404, detail="ProductLine not found")
        return db_productline
    finally:
        db.close()