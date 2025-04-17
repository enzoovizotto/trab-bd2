from dao.sqlalchemy_dao import SQLAlchemyDAO
from datetime import datetime

class SQLAlchemyController:
    def __init__(self):
        self.dao = SQLAlchemyDAO()

    def create_order(self, customer_id, employee_id, order_items):
        return self.dao.create_order(customer_id, employee_id, order_items)

    def get_order_details(self, order_id):
        return self.dao.get_order_details(order_id)

    def get_employee_ranking(self, start_date, end_date):
        return self.dao.get_employee_ranking(start_date, end_date)
