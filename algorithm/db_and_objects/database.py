"""Creating Database and Tables"""

from db_and_objects.product import ProductManager


class Database:
    """Creates the database and works with the
    table class object to create the table within it"""

    def __init__(self, products):

        self.products = products

    def database_constructor(self):
        # inserts data in the database

        product_manager = ProductManager(self.products)
        product_manager.save_product()
        return product_manager
