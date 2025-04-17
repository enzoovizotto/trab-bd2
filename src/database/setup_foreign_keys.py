from dao.database import Database

def check_foreign_key_exists(cursor, table_name, column_name, ref_table):
    cursor.execute("""
        SELECT COUNT(1) 
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name
          AND tc.table_schema = kcu.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
          AND tc.table_name = %s
          AND kcu.column_name = %s
          AND kcu.referenced_table_name = %s;
    """, (table_name, column_name, ref_table))
    return cursor.fetchone()[0] > 0

def create_foreign_keys():
    db = Database()
    conn = db.connect()
    cursor = conn.cursor()
    
    try:
        # Check Orders foreign keys
        if not check_foreign_key_exists(cursor, 'orders', 'customer_id', 'customers'):
            print("Criando FK para customer_id em orders...")
            cursor.execute("""
                ALTER TABLE orders
                ADD CONSTRAINT fk_orders_customers
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id);
            """)
            
        if not check_foreign_key_exists(cursor, 'orders', 'employee_id', 'employees'):
            print("Criando FK para employee_id em orders...")
            cursor.execute("""
                ALTER TABLE orders
                ADD CONSTRAINT fk_orders_employees
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id);
            """)
            
        # Check Order_Details foreign keys
        if not check_foreign_key_exists(cursor, 'order_details', 'order_id', 'orders'):
            print("Criando FK para order_id em order_details...")
            cursor.execute("""
                ALTER TABLE order_details
                ADD CONSTRAINT fk_orderdetails_orders
                FOREIGN KEY (order_id) REFERENCES orders(order_id);
            """)
            
        if not check_foreign_key_exists(cursor, 'order_details', 'product_id', 'products'):
            print("Criando FK para product_id em order_details...")
            cursor.execute("""
                ALTER TABLE order_details
                ADD CONSTRAINT fk_orderdetails_products
                FOREIGN KEY (product_id) REFERENCES products(product_id);
            """)
            
        conn.commit()
        print("Verificação e criação das chaves estrangeiras concluída com sucesso!")
        
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar chaves estrangeiras: {str(e)}")
        raise
    finally:
        cursor.close()
        db.disconnect()

if __name__ == "__main__":
    create_foreign_keys()
