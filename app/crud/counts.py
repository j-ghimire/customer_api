from sqlalchemy.orm import Session
from sqlalchemy import func
from ..model import Customer, Order, Product, Employee, Office, Payment, OrderDetail, ProductLine
from ..logger import logger

def _safe_scalar_count(value):
    return 0 if value is None else value

def count_customers(db: Session):
    logger.info("Counting customers")
    count = _safe_scalar_count(db.query(func.count(Customer.customerNumber)).scalar())
    logger.info("Count customers query completed")
    return count

def count_orders(db: Session):
    count = _safe_scalar_count(db.query(func.count(Order.orderNumber)).scalar())
    logger.info("Count orders query completed")
    return count

def count_products(db: Session):
    count = _safe_scalar_count(db.query(func.count(Product.productCode)).scalar())
    logger.info("Count products query completed")
    return count

def count_employees(db: Session):
    count = _safe_scalar_count(db.query(func.count(Employee.employeeNumber)).scalar())
    logger.info("Count employees query completed")
    return count

def count_offices(db: Session):
    count = _safe_scalar_count(db.query(func.count(Office.officeCode)).scalar())
    logger.info("Count offices query completed")
    return count

def count_payments(db: Session):
    count = _safe_scalar_count(db.query(func.count()).select_from(Payment).scalar())
    logger.info("Count payments query completed")
    return count

def count_orderdetails(db: Session):
    count = _safe_scalar_count(db.query(func.count()).select_from(OrderDetail).scalar())
    logger.info("Count orderdetails query completed")
    return count

def count_productlines(db: Session):
    count = _safe_scalar_count(db.query(func.count(ProductLine.productLine)).scalar())
    logger.info("Count productlines query completed")
    return count