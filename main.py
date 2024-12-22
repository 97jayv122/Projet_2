from controller import Controller
from models import Category
from view import View

def main():
    category = Category()
    view = View()
    etl = Controller(category, view)
    etl.run()   

main()