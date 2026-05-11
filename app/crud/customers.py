from sqlalchemy.orm import Session
from ..model import Customer, Order, OrderDetail, Payment, Employee
from ..logger import logger

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()

def get_customer_by_id(db: Session, customer_id: int):
    logger.info(f"Fetching customer with ID: {customer_id}")
    customer = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if customer:
        logger.info(f"Customer found: {customer_id}")
    else:
        logger.warning(f"Customer not found: {customer_id}")
    return customer

def create_customer(db: Session, customer_data):
    try:
        logger.info(f"Creating customer: {customer_data}")
        
        # Validate salesRepEmployeeNumber
        sales_rep = customer_data.get('salesRepEmployeeNumber')
        if sales_rep and (sales_rep == 0 or not db.query(Employee).filter(Employee.employeeNumber == sales_rep).first()):
            customer_data['salesRepEmployeeNumber'] = None
        
        customer = Customer(**customer_data)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        logger.info(f"Customer created with ID: {customer.customerNumber}")
        return customer
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        db.rollback()
        raise

def update_customer(db: Session, customer_id: int, updates):
    # Validate salesRepEmployeeNumber
    if 'salesRepEmployeeNumber' in updates:
        emp_num = updates['salesRepEmployeeNumber']
        if emp_num == 0 or not db.query(Employee).filter(Employee.employeeNumber == emp_num).first():
            updates['salesRepEmployeeNumber'] = None
    db.query(Customer).filter(Customer.customerNumber == customer_id).update(updates)
    db.commit()
    return get_customer_by_id(db, customer_id)

def delete_customer(db: Session, customer_id: int):
    db.query(Customer).filter(Customer.customerNumber == customer_id).delete()
    db.commit()

def get_customer_complete(db: Session, customer_id: int):
    """Fetch complete customer information including orders, order details, and payments"""
    logger.info(f"Fetching complete customer data for ID: {customer_id}")
    
    # Get customer
    customer = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if not customer:
        logger.warning(f"Customer not found: {customer_id}")
        return None
    
    # Get all orders for the customer
    orders = db.query(Order).filter(Order.customerNumber == customer_id).all()
    logger.info(f"Found {len(orders)} orders for customer {customer_id}")
    
    # Get order details for each order
    for order in orders:
        order_details = db.query(OrderDetail).filter(OrderDetail.orderNumber == order.orderNumber).all()
        order.orderdetails = order_details
        logger.info(f"Found {len(order_details)} details for order {order.orderNumber}")
    
    customer.orders = orders
    
    # Get all payments for the customer
    payments = db.query(Payment).filter(Payment.customerNumber == customer_id).all()
    logger.info(f"Found {len(payments)} payments for customer {customer_id}")
    customer.payments = payments
    
    logger.info(f"Complete customer data retrieved for ID: {customer_id}")
    return customer