from sqlalchemy.orm import Session
from ..model import OrderDetail
from ..logger import logger

def get_orderdetails(db: Session, skip: int = 0, limit: int = 100):
    try:
        logger.info(f"Fetching orderdetails with skip={skip}, limit={limit}")
        result = db.query(OrderDetail).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(result)} orderdetails")
        return result
    except Exception as e:
        logger.error(f"Error fetching orderdetails: {e}")
        raise

def get_orderdetail_by_id(db: Session, ordernumber: int, productcode: str):
    try:
        logger.info(f"Fetching orderdetail by ID: ordernumber={ordernumber}, productcode={productcode}")
        result = db.query(OrderDetail).filter(OrderDetail.orderNumber == ordernumber, OrderDetail.productCode == productcode).first()
        if result:
            logger.info(f"Orderdetail found: ordernumber={ordernumber}, productcode={productcode}")
        else:
            logger.warning(f"Orderdetail not found: ordernumber={ordernumber}, productcode={productcode}")
        return result
    except Exception as e:
        logger.error(f"Error fetching orderdetail ordernumber={ordernumber}, productcode={productcode}: {e}")
        raise

def create_orderdetail(db: Session, orderdetail: OrderDetail):
    try:
        logger.info(f"Creating orderdetail: ordernumber={orderdetail.orderNumber}, productcode={orderdetail.productCode}")
        db.add(orderdetail)
        db.commit()
        db.refresh(orderdetail)
        logger.info(f"Orderdetail created: ordernumber={orderdetail.orderNumber}, productcode={orderdetail.productCode}")
        return orderdetail
    except Exception as e:
        logger.error(f"Error creating orderdetail: {e}")
        db.rollback()
        raise

def update_orderdetail(db: Session, ordernumber: int, productcode: str, updates):
    try:
        logger.info(f"Updating orderdetail: ordernumber={ordernumber}, productcode={productcode} with updates: {updates}")
        db.query(OrderDetail).filter(OrderDetail.orderNumber == ordernumber, OrderDetail.productCode == productcode).update(updates)
        db.commit()
        result = get_orderdetail_by_id(db, ordernumber, productcode)
        logger.info(f"Orderdetail updated: ordernumber={ordernumber}, productcode={productcode}")
        return result
    except Exception as e:
        logger.error(f"Error updating orderdetail ordernumber={ordernumber}, productcode={productcode}: {e}")
        db.rollback()
        raise

def delete_orderdetail(db: Session, ordernumber: int, productcode: str):
    try:
        logger.info(f"Deleting orderdetail: ordernumber={ordernumber}, productcode={productcode}")
        db.query(OrderDetail).filter(OrderDetail.orderNumber == ordernumber, OrderDetail.productCode == productcode).delete()
        db.commit()
        logger.info(f"Orderdetail deleted: ordernumber={ordernumber}, productcode={productcode}")
    except Exception as e:
        logger.error(f"Error deleting orderdetail ordernumber={ordernumber}, productcode={productcode}: {e}")
        db.rollback()
        raise