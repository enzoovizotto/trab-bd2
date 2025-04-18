from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os
from dotenv import load_dotenv
from models.sqlalchemy_models import Base, Order, OrderDetail, Customer, Employee, Product

load_dotenv()

class SQLAlchemyDAO:
    def __init__(self):
        # Create database connection
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_order(self, customer_id, employee_id, order_items):
        try:
            # Create new order
            new_order = Order(
                customerid=customer_id,
                employeeid=employee_id,
                orderdate=datetime.now()
            )
            self.session.add(new_order)
            self.session.flush()  # To get the orderid

            # Create order details
            for item in order_items:
                order_detail = OrderDetail(
                    orderid=new_order.orderid,
                    productid=item['productid'],
                    unitprice=item['unitprice'],
                    quantity=item['quantity'],
                    discount=item.get('discount', 0)
                )
                self.session.add(order_detail)

            self.session.commit()
            return new_order.orderid

        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_order_details(self, order_id):
        try:
            order = self.session.query(Order)\
                .filter(Order.orderid == order_id)\
                .first()

            if not order:
                return None

            result = []
            for detail in order.order_details:
                result.append({
                    'orderid': order.orderid,
                    'orderdate': order.orderdate,
                    'customername': order.customer.companyname,
                    'employeename': f"{order.employee.firstname} {order.employee.lastname}",
                    'productname': detail.product.productname,
                    'quantity': detail.quantity,
                    'unitprice': detail.unitprice
                })

            return result

        except SQLAlchemyError as e:
            raise e

    def get_employee_ranking(self, start_date, end_date):
        try:
            ranking = self.session.query(
                Employee,
                func.count(Order.orderid).label('totalorders'),
                func.sum(
                    OrderDetail.unitprice * OrderDetail.quantity * 
                    (1 - OrderDetail.discount)
                ).label('totalsales')
            ).join(Order, Employee.employeeid == Order.employeeid)\
             .join(OrderDetail, Order.orderid == OrderDetail.orderid)\
             .filter(Order.orderdate.between(start_date, end_date))\
             .group_by(Employee.employeeid)\
             .order_by(func.sum(
                 OrderDetail.unitprice * OrderDetail.quantity * 
                 (1 - OrderDetail.discount)
             ).desc())\
             .all()

            return [
                {
                    'employeename': f"{emp.firstname} {emp.lastname}",
                    'totalorders': total_orders,
                    'totalsales': float(total_sales or 0)
                }
                for emp, total_orders, total_sales in ranking
            ]

        except SQLAlchemyError as e:
            raise e
