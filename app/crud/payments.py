from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..model import Payment
from ..logger import logger

def get_payments(db: Session, skip: int = 0, limit: int = 100):
    try:
        logger.info(f"Fetching payments with skip={skip}, limit={limit}")
        result = db.query(Payment).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(result)} payments")
        return result
    except Exception as e:
        logger.error(f"Error fetching payments: {e}")
        raise

def get_payment_by_id(db: Session, customerNumber: int, checkNumber: str):
    try:
        logger.info(f"Fetching payment by ID: customerNumber={customerNumber}, checkNumber={checkNumber}")
        result = db.query(Payment).filter(Payment.customerNumber == customerNumber, Payment.checkNumber == checkNumber).first()
        if result:
            logger.info(f"Payment found: customerNumber={customerNumber}, checkNumber={checkNumber}")
        else:
            logger.warning(f"Payment not found: customerNumber={customerNumber}, checkNumber={checkNumber}")
        return result
    except Exception as e:
        logger.error(f"Error fetching payment customerNumber={customerNumber}, checkNumber={checkNumber}: {e}")
        raise

def create_payment(db: Session, payment_data):
    try:
        logger.info(f"Creating payment: customerNumber={payment_data.get('customerNumber')}, checkNumber={payment_data.get('checkNumber')}")
        payment = Payment(**payment_data)
        db.add(payment)
        db.commit()
        db.refresh(payment)
        logger.info(f"Payment created: customerNumber={payment.customerNumber}, checkNumber={payment.checkNumber}")
        return payment
    except Exception as e:
        logger.error(f"Error creating payment: {e}")
        db.rollback()
        raise

def update_payment(db: Session, customerNumber: int, checkNumber: str, updates):
    try:
        logger.info(f"Updating payment: customerNumber={customerNumber}, checkNumber={checkNumber} with updates: {updates}")
        db.query(Payment).filter(Payment.customerNumber == customerNumber, Payment.checkNumber == checkNumber).update(updates)
        db.commit()
        result = get_payment_by_id(db, customerNumber, checkNumber)
        logger.info(f"Payment updated: customerNumber={customerNumber}, checkNumber={checkNumber}")
        return result
    except Exception as e:
        logger.error(f"Error updating payment customerNumber={customerNumber}, checkNumber={checkNumber}: {e}")
        db.rollback()
        raise

def delete_payment(db: Session, customerNumber: int, checkNumber: str):
    try:
        logger.info(f"Deleting payment: customerNumber={customerNumber}, checkNumber={checkNumber}")
        rows = db.query(Payment).filter(Payment.customerNumber == customerNumber, Payment.checkNumber == checkNumber).delete()
        if rows == 0:
            db.rollback()
            return None
        db.commit()
        logger.info(f"Payment deleted: customerNumber={customerNumber}, checkNumber={checkNumber}")
        return True
    except IntegrityError as e:
        logger.error(f"Foreign key error deleting payment customerNumber={customerNumber}, checkNumber={checkNumber}: {e}")
        db.rollback()
        raise ValueError(
            f"Cannot delete payment for customer '{customerNumber}' with check number '{checkNumber}' because it is referenced by other records"
        )
    except Exception as e:
        logger.error(f"Error deleting payment customerNumber={customerNumber}, checkNumber={checkNumber}: {e}")
        db.rollback()
        raise