class Order:
    def __init__(self, order_id=None, customer_id=None, employee_id=None, order_date=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.employee_id = employee_id
        self.order_date = order_date

class OrderDetail:
    def __init__(self, order_id=None, product_id=None, unit_price=None, quantity=None, discount=None):
        self.order_id = order_id
        self.product_id = product_id
        self.unit_price = unit_price
        self.quantity = quantity
        self.discount = discount
