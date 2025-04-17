from controllers.order_controller import OrderController
from controllers.sqlalchemy_controller import SQLAlchemyController
from datetime import datetime

class OrderView:
    def __init__(self):
        self.psycopg_controller = OrderController()
        self.sqlalchemy_controller = SQLAlchemyController()
        self.current_controller = self.psycopg_controller  # Default to psycopg2

    def display_menu(self):
        while True:
            impl = "SQLAlchemy" if self.current_controller == self.sqlalchemy_controller else "Psycopg2"
            print(f"\n=== Sistema de Pedidos Northwind ({impl}) ===")
            print("1. Criar novo pedido")
            print("2. Criar novo pedido (versão insegura - SQL Injection)")
            print("3. Ver detalhes de um pedido")
            print("4. Ver ranking de funcionários")
            print("5. Trocar implementação (Psycopg2/SQLAlchemy)")
            print("6. Sair")

            choice = input("\nEscolha uma opção: ")
            if choice == "1":
                self.create_order(unsafe=False)
            elif choice == "2":
                if self.current_controller == self.sqlalchemy_controller:
                    print("SQL Injection não está disponível na implementação SQLAlchemy")
                else:
                    self.create_order(unsafe=True)
            elif choice == "3":
                self.show_order_details()
            elif choice == "4":
                self.show_employee_ranking()
            elif choice == "5":
                if self.current_controller == self.psycopg_controller:
                    self.current_controller = self.sqlalchemy_controller
                    print("\nMudando para implementação SQLAlchemy")
                else:
                    self.current_controller = self.psycopg_controller
                    print("\nMudando para implementação Psycopg2")
            elif choice == "6":
                break
            else:
                print("Opção inválida!")

    def create_order(self, unsafe=False):
        print("\n=== Criar Novo Pedido ===")
        customer_id = input("ID do Cliente: ")
        employee_id = input("ID do Funcionário: ")

        order_items = []
        while True:
            print("\n--- Adicionar Item ao Pedido ---")
            product_id = input("ID do Produto (ou deixe vazio para finalizar): ")
            if not product_id:
                break

            quantity = float(input("Quantidade: "))
            unit_price = float(input("Preço Unitário: "))
            discount = float(input("Desconto (0-1): ") or "0")

            order_items.append({
                'productid': product_id,
                'quantity': quantity,
                'unitprice': unit_price,
                'discount': discount
            })

        try:
            if self.current_controller == self.sqlalchemy_controller:
                order_id = self.current_controller.create_order(
                    customer_id=customer_id,
                    employee_id=employee_id,
                    order_items=order_items
                )
            else:
                order_id = self.current_controller.create_order(
                    customer_id=customer_id,
                    employee_id=employee_id,
                    order_items=order_items,
                    unsafe=unsafe
                )
            print(f"\nPedido criado com sucesso! ID do pedido: {order_id}")
        except Exception as e:
            print(f"\nErro ao criar pedido: {str(e)}")

    def show_order_details(self):
        order_id = input("\nDigite o ID do pedido: ")
        try:
            details = self.current_controller.get_order_details(order_id)
            if not details:
                print("Pedido não encontrado!")
                return

            print("\n=== Detalhes do Pedido ===")
            if self.current_controller == self.sqlalchemy_controller:
                print(f"Número do pedido: {details[0]['orderid']}")
                print(f"Data do pedido: {details[0]['orderdate']}")
                print(f"Cliente: {details[0]['customername']}")
                print(f"Vendedor: {details[0]['employeename']}")
                print("\nItens do pedido:")
                print("-" * 50)
                print("Produto | Quantidade | Preço Unitário")
                print("-" * 50)

                for detail in details:
                    print(f"{detail['productname']} | {detail['quantity']} | ${float(detail['unitprice']):.2f}")
            else:
                print(f"Número do pedido: {details[0][0]}")
                print(f"Data do pedido: {details[0][1]}")
                print(f"Cliente: {details[0][2]}")
                print(f"Vendedor: {details[0][3]}")
                print("\nItens do pedido:")
                print("-" * 50)
                print("Produto | Quantidade | Preço Unitário")
                print("-" * 50)

                for detail in details:
                    print(f"{detail[4]} | {detail[5]} | ${detail[6]:.2f}")

        except Exception as e:
            print(f"Erro ao buscar detalhes do pedido: {str(e)}")

    def show_employee_ranking(self):
        print("\n=== Ranking de Funcionários ===")
        start_date = input("Data inicial (YYYY-MM-DD): ")
        end_date = input("Data final (YYYY-MM-DD): ")

        try:
            ranking = self.current_controller.get_employee_ranking(start_date, end_date)

            print("\nRanking por vendas:")
            print("-" * 70)
            print("Funcionário | Total de Pedidos | Total de Vendas")
            print("-" * 70)

            if self.current_controller == self.sqlalchemy_controller:
                for employee in ranking:
                    print(f"{employee['employeename']} | {employee['totalorders']} | ${employee['totalsales']:.2f}")
            else:
                for employee in ranking:
                    print(f"{employee[0]} | {employee[1]} | ${employee[2]:.2f}")

        except Exception as e:
            print(f"Erro ao buscar ranking: {str(e)}")
