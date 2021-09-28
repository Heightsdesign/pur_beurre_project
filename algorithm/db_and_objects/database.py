"""Creating Database and Tables"""

from connexion.mysql_connector import dbcursor
from db_and_objects.product import ProductManager


class Table:
    """Creates Table objects"""

    def __init__(self, name, attrs):

        self.name = name
        self.attrs = attrs

    def create_table(self):
        # creates a table takes the name and attributes as arguments

        dbcursor.execute("CREATE TABLE IF NOT EXISTS {}({})".format(self.name, self.attrs))


class Database:
    """Creates the database and works with the
    table class object to create the table within it"""

    def __init__(self, products):

        self.products = products

        # creates the database
        dbcursor.execute("SELECT 'CREATE DATABASE pur_beurre'")
        #dbcursor.execute("WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pur_beurre')")

    def main_database(self):
        # Main function to execute, to create database and tables

        products_table_attrs = "id BIGINT  NOT NULL, name VARCHAR(255) NOT NULL, nutriscore VARCHAR(1) NOT NULL, ingredients TEXT, url VARCHAR(255) NOT NULL, PRIMARY KEY(id) "

        products_table = Table("Products", products_table_attrs)

        product_categories_table_attrs = "id INT PRIMARY KEY AUTO_INCREMENT, idproduct BIGINT  NOT NULL, idcategory INT NOT NULL, FOREIGN KEY (idproduct) REFERENCES Products (id), FOREIGN KEY (idcategory) REFERENCES Categories (id) "

        product_categories_table = Table(
            "Product_Categories", product_categories_table_attrs
        )

        categories_table_attrs = "id INT NOT NULL AUTO_INCREMENT, name VARCHAR(100) NOT NULL UNIQUE, PRIMARY KEY(id)"
        categories_table = Table("Categories", categories_table_attrs)

        stores_table_attrs = "id INT NOT NULL AUTO_INCREMENT, name VARCHAR(100) NOT NULL UNIQUE, PRIMARY KEY(id) "
        stores_table = Table("Stores", stores_table_attrs)

        product_stores_table_attrs = "id INT PRIMARY KEY AUTO_INCREMENT, idproduct BIGINT NOT NULL, idstore INT, FOREIGN KEY (idproduct) REFERENCES Products (id), FOREIGN KEY (idstore) REFERENCES Stores (id) "
        product_stores_table = Table(
            "Product_Stores", product_stores_table_attrs
            )

        favorites_table_attrs = "id SMALLINT PRIMARY KEY AUTO_INCREMENT, id_product BIGINT NOT NULL, FOREIGN KEY (id_product) REFERENCES Products (id) "
        favorites_table = Table("Favorites", favorites_table_attrs)

        products_table.create_table()
        categories_table.create_table()
        product_categories_table.create_table()
        stores_table.create_table()
        product_stores_table.create_table()
        favorites_table.create_table()

    def delete_doubles(self):
        # This method deletes the doubles which
        # can occur in the product_categories table

        dbcursor.execute("USE pur_beurre;")
        dbcursor.execute(
            "DELETE product_categories FROM product_categories "
            "LEFT OUTER JOIN ( "
            "SELECT MIN(id) as id, idproduct, idcategory "
            "FROM product_categories "
            "GROUP BY idproduct, idcategory "
            ") as t1 "
            "ON product_categories.id = t1.id "
            "WHERE t1.id IS NULL "
        )

    def database_constructor(self):
        # Builds the database

        #self.main_database()
        product_manager = ProductManager(self.products)
        product_manager.save()
        self.delete_doubles()
        return product_manager
