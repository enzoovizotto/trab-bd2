from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = {'schema': 'northwind'}

    customerid = Column(String(5), primary_key=True)
    companyname = Column(String(40), nullable=False)
    orders = relationship('Order', back_populates='customer')

class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'northwind'}

    employeeid = Column(Integer, primary_key=True)
    firstname = Column(String(10), nullable=False)
    lastname = Column(String(20), nullable=False)
    orders = relationship('Order', back_populates='employee')

class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'northwind'}

    productid = Column(Integer, primary_key=True)
    productname = Column(String(40), nullable=False)
    unitprice = Column(DECIMAL(10, 2))
    order_details = relationship('OrderDetail', back_populates='product')

class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'northwind'}

    orderid = Column(Integer, primary_key=True)
    customerid = Column(String(5), ForeignKey('northwind.customers.customerid'))
    employeeid = Column(Integer, ForeignKey('northwind.employees.employeeid'))
    orderdate = Column(DateTime)
    
    customer = relationship('Customer', back_populates='orders')
    employee = relationship('Employee', back_populates='orders')
    order_details = relationship('OrderDetail', back_populates='order')

class OrderDetail(Base):
    __tablename__ = 'order_details'
    __table_args__ = {'schema': 'northwind'}

    orderid = Column(Integer, ForeignKey('northwind.orders.orderid'), primary_key=True)
    productid = Column(Integer, ForeignKey('northwind.products.productid'), primary_key=True)
    unitprice = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    discount = Column(DECIMAL(4, 2), nullable=False)

    order = relationship('Order', back_populates='order_details')
    product = relationship('Product', back_populates='order_details')
