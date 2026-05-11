from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..model import ProductLine
from ..logger import logger

def get_productlines(db: Session, skip: int = 0, limit: int = 100):
    try:
        logger.info(f"Fetching productlines with skip={skip}, limit={limit}")
        result = db.query(ProductLine).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(result)} productlines")
        return result
    except Exception as e:
        logger.error(f"Error fetching productlines: {e}")
        raise

def get_productline_by_id(db: Session, productline: str):
    try:
        logger.info(f"Fetching productline by ID: {productline}")
        result = db.query(ProductLine).filter(ProductLine.productLine == productline).first()
        if result:
            logger.info(f"Productline found: {productline}")
        else:
            logger.warning(f"Productline not found: {productline}")
        return result
    except Exception as e:
        logger.error(f"Error fetching productline {productline}: {e}")
        raise

def create_productline(db: Session, productline: ProductLine):
    try:
        logger.info(f"Creating productline: {productline.productLine}")
        db.add(productline)
        db.commit()
        db.refresh(productline)
        logger.info(f"Productline created: {productline.productLine}")
        return productline
    except Exception as e:
        logger.error(f"Error creating productline: {e}")
        db.rollback()
        raise

def update_productline(db: Session, productline: str, updates):
    try:
        logger.info(f"Updating productline: {productline} with updates: {updates}")
        if "image" in updates and isinstance(updates["image"], str):
            updates["image"] = updates["image"].encode("utf-8")
        db.query(ProductLine).filter(ProductLine.productLine == productline).update(updates)
        db.commit()
        result = get_productline_by_id(db, productline)
        logger.info(f"Productline updated: {productline}")
        return result
    except Exception as e:
        logger.error(f"Error updating productline {productline}: {e}")
        db.rollback()
        raise

def delete_productline(db: Session, productline: str):
    try:
        logger.info(f"Deleting productline: {productline}")
        rows = db.query(ProductLine).filter(ProductLine.productLine == productline).delete()
        if rows == 0:
            db.rollback()
            return None
        db.commit()
        logger.info(f"Productline deleted: {productline}")
        return True
    except IntegrityError as e:
        logger.error(f"Foreign key error deleting productline {productline}: {e}")
        db.rollback()
        raise ValueError(
            f"Cannot delete productline '{productline}' because it is referenced by existing products"
        )
    except Exception as e:
        logger.error(f"Error deleting productline {productline}: {e}")
        db.rollback()
        raise
