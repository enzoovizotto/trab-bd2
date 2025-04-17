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
                customer_id=customer_id,
                employee_id=employee_id,
                order_date=datetime.now()
            )
            self.session.add(new_order)
            self.session.flush()  # To get the order_id

            # Create order details
            for item in order_items:
                order_detail = OrderDetail(
                    order_id=new_order.order_id,
                    product_id=item['productid'],
                    unit_price=item['unitprice'],
                    quantity=item['quantity'],
                    discount=item.get('discount', 0)
                )
                self.session.add(order_detail)

            self.session.commit()
            return new_order.order_id

        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_order_details(self, order_id):
        try:
            order = self.session.query(Order)\
                .filter(Order.order_id == order_id)\
                .first()

            if not order:
                return None

            result = []
            for detail in order.order_details:
                result.append({
                    'orderid': order.order_id,
                    'orderdate': order.order_date,
                    'customername': order.customer.company_name,
                    'employeename': f"{order.employee.first_name} {order.employee.last_name}",
                    'productname': detail.product.product_name,
                    'quantity': detail.quantity,
                    'unitprice': detail.unit_price
                })

            return result

        except SQLAlchemyError as e:
            raise e

    def get_employee_ranking(self, start_date, end_date):
        try:
            ranking = self.session.query(
                Employee,
                func.count(Order.order_id).label('totalorders'),
                func.sum(
                    OrderDetail.unit_price * OrderDetail.quantity * 
                    (1 - OrderDetail.discount)
                ).label('totalsales')
            ).join(Order, Employee.employee_id == Order.employee_id)\
             .join(OrderDetail, Order.order_id == OrderDetail.order_id)\
             .filter(Order.order_date.between(start_date, end_date))\
             .group_by(Employee.employee_id)\
             .order_by(func.sum(
                 OrderDetail.unit_price * OrderDetail.quantity * 
                 (1 - OrderDetail.discount)
             ).desc())\
             .all()

            return [
                {
                    'employeename': f"{emp.first_name} {emp.last_name}",
                    'totalorders': total_orders,
                    'totalsales': float(total_sales or 0)
                }
                for emp, total_orders, total_sales in ranking
            ]

        except SQLAlchemyError as e:
            raise e
