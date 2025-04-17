from datetime import datetime
from models.order import Order, OrderDetail
from dao.order_dao import OrderDAO

class OrderController:
    def __init__(self):
        self.order_dao = OrderDAO()

    def create_order(self, customer_id, employee_id, order_items, unsafe=False):
        # Criar objeto Order
        order = Order(
            customer_id=customer_id,
            employee_id=employee_id,
            order_date=datetime.now()
        )

        # Criar lista de OrderDetail
        order_details = []
        for item in order_items:
            detail = OrderDetail(
                product_id=item['productid'],
                unit_price=item['unitprice'],
                quantity=item['quantity'],
                discount=item.get('discount', 0)
            )
            order_details.append(detail)

        # Usar o DAO para criar o pedido
        return self.order_dao.create_order(order, order_details, unsafe)

    def get_order_details(self, order_id):
        return self.order_dao.get_order_details(order_id)

    def get_employee_ranking(self, start_date, end_date):
        return self.order_dao.get_employee_ranking(start_date, end_date)
