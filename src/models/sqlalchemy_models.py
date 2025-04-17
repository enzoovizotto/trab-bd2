from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(String(5), primary_key=True)
    company_name = Column(String(40), nullable=False)
    orders = relationship('Order', back_populates='customer')

class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String(10), nullable=False)
    last_name = Column(String(20), nullable=False)
    orders = relationship('Order', back_populates='employee')

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(40), nullable=False)
    unit_price = Column(DECIMAL(10, 2))
    order_details = relationship('OrderDetail', back_populates='product')

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(String(5), ForeignKey('customers.customerid'))
    employee_id = Column(Integer, ForeignKey('employees.employeeid'))
    order_date = Column(DateTime)
    
    customer = relationship('Customer', back_populates='orders')
    employee = relationship('Employee', back_populates='orders')
    order_details = relationship('OrderDetail', back_populates='order')

class OrderDetail(Base):
    __tablename__ = 'order_details'

    order_id = Column(Integer, ForeignKey('orders.orderid'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.productid'), primary_key=True)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    discount = Column(DECIMAL(4, 2), nullable=False)

    order = relationship('Order', back_populates='order_details')
    product = relationship('Product', back_populates='order_details')
