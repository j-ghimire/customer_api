from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..model import Office
from ..logger import logger

def get_offices(db: Session, skip: int = 0, limit: int = 100):
    try:
        logger.info(f"Fetching offices with skip={skip}, limit={limit}")
        result = db.query(Office).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(result)} offices")
        return result
    except Exception as e:
        logger.error(f"Error fetching offices: {e}")
        raise

def get_office_by_id(db: Session, officeCode: str):
    try:
        logger.info(f"Fetching office by ID: {officeCode}")
        result = db.query(Office).filter(Office.officeCode == officeCode).first()
        if result:
            logger.info(f"Office found: {officeCode}")
        else:
            logger.warning(f"Office not found: {officeCode}")
        return result
    except Exception as e:
        logger.error(f"Error fetching office {officeCode}: {e}")
        raise

def create_office(db: Session, office: Office):
    try:
        logger.info(f"Creating office: {office.officeCode}")
        db.add(office)
        db.commit()
        db.refresh(office)
        logger.info(f"Office created: {office.officeCode}")
        return office
    except Exception as e:
        logger.error(f"Error creating office: {e}")
        db.rollback()
        raise

def update_office(db: Session, officeCode: str, updates):
    try:
        logger.info(f"Updating office: {officeCode} with updates: {updates}")
        db.query(Office).filter(Office.officeCode == officeCode).update(updates)
        db.commit()
        result = get_office_by_id(db, officeCode)
        logger.info(f"Office updated: {officeCode}")
        return result
    except Exception as e:
        logger.error(f"Error updating office {officeCode}: {e}")
        db.rollback()
        raise

def delete_office(db: Session, officeCode: str):
    try:
        logger.info(f"Deleting office: {officeCode}")
        rows = db.query(Office).filter(Office.officeCode == officeCode).delete()
        if rows == 0:
            db.rollback()
            return None
        db.commit()
        logger.info(f"Office deleted: {officeCode}")
        return True
    except IntegrityError as e:
        logger.error(f"Foreign key error deleting office {officeCode}: {e}")
        db.rollback()
        raise ValueError(
            f"Cannot delete office '{officeCode}' because it is referenced by existing employees"
        )
    except Exception as e:
        logger.error(f"Error deleting office {officeCode}: {e}")
        db.rollback()
        raise