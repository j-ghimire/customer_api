from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..model import Order
from ..logger import logger

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    try:
        logger.info(f"Fetching orders with skip={skip}, limit={limit}")
        result = db.query(Order).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(result)} orders")
        return result
    except Exception as e:
        logger.error(f"Error fetching orders: {e}")
        raise

def get_order_by_id(db: Session, ordernumber: int):
    try:
        logger.info(f"Fetching order by ID: {ordernumber}")
        result = db.query(Order).filter(Order.orderNumber == ordernumber).first()
        if result:
            logger.info(f"Order found: {ordernumber}")
        else:
            logger.warning(f"Order not found: {ordernumber}")
        return result
    except Exception as e:
        logger.error(f"Error fetching order {ordernumber}: {e}")
        raise

def create_order(db: Session, order: Order):
    try:
        logger.info(f"Creating order: {order.orderNumber}")
        db.add(order)
        db.commit()
        db.refresh(order)
        logger.info(f"Order created: {order.orderNumber}")
        return order
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        db.rollback()
        raise

def update_order(db: Session, ordernumber: int, updates):
    try:
        logger.info(f"Updating order: {ordernumber} with updates: {updates}")
        db.query(Order).filter(Order.orderNumber == ordernumber).update(updates)
        db.commit()
        result = get_order_by_id(db, ordernumber)
        logger.info(f"Order updated: {ordernumber}")
        return result
    except IntegrityError as e:
        logger.error(f"Foreign key error updating order {ordernumber}: {e}")
        db.rollback()
        if "customerNumber" in str(e):
            raise ValueError("Invalid customerNumber: customer does not exist")
        raise ValueError(f"Invalid data: {str(e)}")
    except Exception as e:
        logger.error(f"Error updating order {ordernumber}: {e}")
        db.rollback()
        raise

def delete_order(db: Session, ordernumber: int):
    try:
        logger.info(f"Deleting order: {ordernumber}")
        rows = db.query(Order).filter(Order.orderNumber == ordernumber).delete()
        if rows == 0:
            db.rollback()
            return None
        db.commit()
        logger.info(f"Order deleted: {ordernumber}")
        return True
    except IntegrityError as e:
        logger.error(f"Foreign key error deleting order {ordernumber}: {e}")
        db.rollback()
        raise ValueError(
            f"Cannot delete order '{ordernumber}' because it is referenced by existing orderdetails"
        )
    except Exception as e:
        logger.error(f"Error deleting order {ordernumber}: {e}")
        db.rollback()
        raise