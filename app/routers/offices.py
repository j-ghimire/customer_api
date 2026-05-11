from typing import List
from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..crud import offices as crud
from ..schemas import offices as schemas
from ..model import Office

router = APIRouter()

@router.get("/offices", response_model=List[schemas.OfficeOut])
def list_offices(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        return crud.get_offices(db, skip=skip, limit=limit)
    finally:
        db.close()

@router.get("/offices/{officeCode}", response_model=schemas.OfficeOut)
def get_office(officeCode: str):
    db = SessionLocal()
    try:
        office = crud.get_office_by_id(db, officeCode)
        if not office:
            raise HTTPException(status_code=404, detail="Office not found")
        return office
    finally:
        db.close()

@router.put("/offices/{officeCode}", response_model=schemas.OfficeOut)
def update_office(officeCode: str, updates: schemas.OfficeUpdate):
    db = SessionLocal()
    try:
        db_office = crud.update_office(db, officeCode, updates.model_dump(exclude_unset=True))
        if not db_office:
            raise HTTPException(status_code=404, detail="Office not found")
        return db_office
    finally:
        db.close()