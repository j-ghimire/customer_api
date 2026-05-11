from typing import List
from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..crud import products as crud
from ..schemas import products as schemas
from ..model import Product

router = APIRouter()

@router.get("/products", response_model=List[schemas.ProductOut])
def list_products(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        return crud.get_products(db, skip=skip, limit=limit)
    finally:
        db.close()

@router.get("/products/{productcode}", response_model=schemas.ProductOut)
def get_product(productcode: str):
    db = SessionLocal()
    try:
        product = crud.get_product_by_id(db, productcode)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    finally:
        db.close()

@router.put("/products/{productcode}", response_model=schemas.ProductOut)
def update_product(productcode: str, updates: schemas.ProductUpdate):
    db = SessionLocal()
    try:
        db_product = crud.update_product(db, productcode, updates.model_dump(exclude_unset=True))
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return db_product
    except crud.ProductLineNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()