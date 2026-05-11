from typing import List
from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..crud import customers as crud
from ..schemas import customers as schemas
from ..model import Customer
from ..logger import logger

router = APIRouter()

@router.get("/customers", response_model=List[schemas.CustomerOut])
def list_customers(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        logger.info(f"API request to list customers - skip: {skip}, limit: {limit}")
        customers = crud.get_customers(db, skip=skip, limit=limit)
        logger.info(f"Successfully retrieved {len(customers)} customers")
        return customers
    except Exception as e:
        logger.error(f"Error listing customers: {e}")
        raise
    finally:
        db.close()

@router.post("/customers", response_model=schemas.CustomerOut)
def create_customer(customer: schemas.CustomerCreate):
    db = SessionLocal()
    try:
        logger.info(f"API request to create customer: {customer}")
        db_customer = crud.create_customer(db, customer.model_dump())
        logger.info(f"Customer created successfully with ID: {db_customer.customerNumber}")
        return db_customer
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        raise
    finally:
        db.close()

@router.get("/customers/{customer_id}", response_model=schemas.CustomerDetailComplete)
def get_customer(customer_id: int):
    db = SessionLocal()
    try:
        logger.info(f"API request to get complete customer details: {customer_id}")
        customer = crud.get_customer_complete(db, customer_id)
        if not customer:
            logger.error(f"Customer not found for ID: {customer_id}")
            raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found")
        logger.info(f"Successfully retrieved complete customer data: {customer_id}")
        return customer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting customer {customer_id}: {e}")
        raise
    finally:
        db.close()

@router.put("/customers/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(customer_id: int, updates: schemas.CustomerUpdate):
    db = SessionLocal()
    try:
        logger.info(f"API request to update customer {customer_id} with: {updates}")
        db_customer = crud.update_customer(db, customer_id, updates.model_dump(exclude_unset=True))
        if not db_customer:
            logger.error(f"Customer not found for update: {customer_id}")
            raise HTTPException(status_code=404, detail="Customer not found")
        logger.info(f"Customer updated successfully: {customer_id}")
        return db_customer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating customer {customer_id}: {e}")
        raise
    finally:
        db.close()

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    db = SessionLocal()
    try:
        logger.info(f"API request to delete customer: {customer_id}")
        crud.delete_customer(db, customer_id)
        logger.info(f"Customer deleted successfully: {customer_id}")
        return {"message": "Customer deleted"}
    except Exception as e:
        logger.error(f"Error deleting customer {customer_id}: {e}")
        raise
    finally:
        db.close()