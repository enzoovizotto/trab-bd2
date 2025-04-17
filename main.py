import sys
import os

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from views.order_view import OrderView

def main():
    view = OrderView()
    view.display_menu()

if __name__ == "__main__":
    main()
