from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..model import Employee
from ..logger import logger

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    try:
        logger.info(f"Fetching employees with skip={skip}, limit={limit}")
        result = db.query(Employee).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(result)} employees")
        return result
    except Exception as e:
        logger.error(f"Error fetching employees: {e}")
        raise

def get_employee_by_id(db: Session, employeeNumber: int):
    try:
        logger.info(f"Fetching employee by ID: {employeeNumber}")
        result = db.query(Employee).filter(Employee.employeeNumber == employeeNumber).first()
        if result:
            logger.info(f"Employee found: {employeeNumber}")
        else:
            logger.warning(f"Employee not found: {employeeNumber}")
        return result
    except Exception as e:
        logger.error(f"Error fetching employee {employeeNumber}: {e}")
        raise

def create_employee(db: Session, employee: Employee):
    try:
        logger.info(f"Creating employee: {employee.employeeNumber}")
        db.add(employee)
        db.commit()
        db.refresh(employee)
        logger.info(f"Employee created: {employee.employeeNumber}")
        return employee
    except Exception as e:
        logger.error(f"Error creating employee: {e}")
        db.rollback()
        raise

def update_employee(db: Session, employeeNumber: int, updates):
    try:
        logger.info(f"Updating employee: {employeeNumber} with updates: {updates}")
        db.query(Employee).filter(Employee.employeeNumber == employeeNumber).update(updates)
        db.commit()
        result = get_employee_by_id(db, employeeNumber)
        logger.info(f"Employee updated: {employeeNumber}")
        return result
    except IntegrityError as e:
        logger.error(f"Foreign key error updating employee {employeeNumber}: {e}")
        db.rollback()
        if "reportsTo" in str(e):
            raise ValueError(f"Invalid reportsTo value: Employee manager does not exist")
        elif "officeCode" in str(e):
            raise ValueError(f"Invalid officeCode: Office does not exist")
        else:
            raise ValueError(f"Invalid data: {str(e)}")
    except Exception as e:
        logger.error(f"Error updating employee {employeeNumber}: {e}")
        db.rollback()
        raise

def delete_employee(db: Session, employeeNumber: int):
    try:
        logger.info(f"Deleting employee: {employeeNumber}")
        db.query(Employee).filter(Employee.employeeNumber == employeeNumber).delete()
        db.commit()
        logger.info(f"Employee deleted: {employeeNumber}")
    except Exception as e:
        logger.error(f"Error deleting employee {employeeNumber}: {e}")
        db.rollback()
        raise