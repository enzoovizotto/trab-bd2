from .database import Database
from datetime import datetime

class OrderDAO:
    def __init__(self):
        self.db = Database()

    def create_order(self, order, order_details, unsafe=False):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            # Versão vulnerável a SQL injection (quando unsafe=True)
            if unsafe:                
                query = f"""
                    INSERT INTO northwind.orders (customerid, employeeid, orderdate)
                    VALUES ({order.customer_id}, {order.employee_id}, '{order.order_date}')
                    RETURNING orderid
                """
            else:
                # Versão segura usando parâmetros
                query = """
                    INSERT INTO northwind.orders (customerid, employeeid, orderdate)
                    VALUES (%s, %s, %s)
                    RETURNING orderid
                """
                
            if unsafe:
                cursor.execute(query)
            else:
                cursor.execute(query, (order.customer_id, order.employee_id, order.order_date))
            
            order_id = cursor.fetchone()[0]

            # Inserir detalhes do pedido
            for detail in order_details:
                if unsafe:
                    detail_query = f"""
                        INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity, discount)
                        VALUES ({order_id}, '{detail.product_id}', '{detail.unit_price}', '{detail.quantity}', '{detail.discount}')
                    """
                    cursor.execute(detail_query)
                else:
                    detail_query = """
                        INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity, discount)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(detail_query, (order_id, detail.product_id, detail.unit_price, detail.quantity, detail.discount))

            conn.commit()
            return order_id

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.disconnect()

    def get_order_details(self, orderid):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            query = """
                SELECT o.orderid, o.orderdate, 
                       c.companyname as customername,
                       e.firstname || ' ' || e.lastname as employeename,
                       p.productname, od.quantity, od.unitprice
                FROM northwind.orders o
                JOIN northwind.customers c ON o.customerid = c.customerid
                JOIN northwind.employees e ON o.employeeid = e.employeeid
                JOIN northwind.order_details od ON o.orderid = od.orderid
                JOIN northwind.products p ON od.productid = p.productid
                WHERE o.orderid = %s
            """
            cursor.execute(query, (orderid,))
            return cursor.fetchall()
        finally:
            cursor.close()
            self.db.disconnect()

    def get_employee_ranking(self, start_date, end_date):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            query = """
                SELECT 
                    e.firstname || ' ' || e.lastname as employeename,
                    COUNT(DISTINCT o.orderid) as totalorders,
                    SUM(od.unitprice * od.quantity * (1 - od.discount)) as totalsales
                FROM northwind.employees e
                LEFT JOIN northwind.orders o ON e.employeeid = o.employeeid
                LEFT JOIN northwind.order_details od ON o.orderid = od.orderid
                WHERE o.orderdate BETWEEN %s AND %s
                GROUP BY e.employeeid, e.firstname, e.lastname
                ORDER BY totalsales DESC
            """
            cursor.execute(query, (start_date, end_date))
            return cursor.fetchall()
        finally:
            cursor.close()
            self.db.disconnect()