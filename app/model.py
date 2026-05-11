from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Text, Numeric, SmallInteger, LargeBinary
from .database import Base

class ProductLine(Base):
    __tablename__ = "productlines"
    productLine = Column(String(50), primary_key=True)
    textDescription = Column(String(4000))
    htmlDescription = Column(Text)
    image = Column(LargeBinary)

class Product(Base):
    __tablename__ = "products"
    productCode = Column(String(15), primary_key=True)
    productName = Column(String(70))
    productLine = Column(String(50), ForeignKey("productlines.productLine"))
    productScale = Column(String(10))
    productVendor = Column(String(50))
    productDescription = Column(Text)
    quantityInStock = Column(Integer)
    buyPrice = Column(Numeric(10, 2))
    MSRP = Column(Numeric(10, 2))

class Office(Base):
    __tablename__ = "offices"
    officeCode = Column(String(10), primary_key=True)
    city = Column(String(50))
    phone = Column(String(50))
    addressLine1 = Column(String(50))
    addressLine2 = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    postalCode = Column(String(15))
    territory = Column(String(10))

class Employee(Base):
    __tablename__ = "employees"
    employeeNumber = Column(Integer, primary_key=True)
    lastName = Column(String(50))
    firstName = Column(String(50))
    extension = Column(String(10))
    email = Column(String(100))
    officeCode = Column(String(10), ForeignKey("offices.officeCode"))
    reportsTo = Column(Integer, ForeignKey("employees.employeeNumber"))
    jobTitle = Column(String(50))

class Customer(Base):
    __tablename__ = "customers"
    customerNumber = Column(Integer, primary_key=True, index=True)
    customerName = Column(String(50))
    contactLastName = Column(String(50))
    contactFirstName = Column(String(50))
    phone = Column(String(50))
    addressLine1 = Column(String(50))
    addressLine2 = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    postalCode = Column(String(15))
    country = Column(String(50))
    salesRepEmployeeNumber = Column(Integer, ForeignKey("employees.employeeNumber"))
    creditLimit = Column(Numeric(10, 2))

class Payment(Base):
    __tablename__ = "payments"
    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"), primary_key=True)
    checkNumber = Column(String(50), primary_key=True)
    paymentDate = Column(Date)
    amount = Column(Numeric(10, 2))

class Order(Base):
    __tablename__ = "orders"
    orderNumber = Column(Integer, primary_key=True)
    orderDate = Column(Date)
    requiredDate = Column(Date)
    shippedDate = Column(Date)
    status = Column(String(15))
    comments = Column(Text)
    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"))

class OrderDetail(Base):
    __tablename__ = "orderdetails"
    orderNumber = Column(Integer, ForeignKey("orders.orderNumber"), primary_key=True)
    productCode = Column(String(15), ForeignKey("products.productCode"), primary_key=True)
    quantityOrdered = Column(Integer)
    priceEach = Column(Numeric(10, 2))
    orderLineNumber = Column(SmallInteger)