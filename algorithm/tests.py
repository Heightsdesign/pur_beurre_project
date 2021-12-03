import sys
from algorithm.db_and_objects.product import (
    Product,
    ProductParser,
    ProductManager,
)
from django.test import TestCase
from unittest import mock
from substitutes.models import Product as DbProduct
import requests


class ProductParserTestCase(TestCase):
    """Tests the product parser class and its methods"""

    def new_init(self):
        """Mocks the data retreived by api file"""
        self.data = [
            {
                "products": {
                    "code": 1564647,
                    "product_name_fr": "Nutella",
                    "nutrition_grade_fr": "e",
                    "url": "https://www.openfoodfacts.com/Nutella",
                    "categories": "snacks, snacks_sucrés",
                }
            }
        ]

    def test_product_parser_is_valid(self):
        # Mocks a product supposed to be valid to the method "is_valid"
        product_true = {
            "code": 1564647,
            "product_name_fr": "Nutella",
            "nutrition_grade_fr": "e",
            "url": "https://www.openfoodfacts.com/Nutella",
            "categories": "snacks, snacks_sucrés",
        }

        # Replaces the self.data in product parser with mocked data in new_init
        with mock.patch(
                "db_and_objects.product.ProductParser.__init__",
                self.new_init
        ):
            # Tests method is_valid with a valid product
            assert ProductParser().is_valid(product_true)

        # Mocks a which is not supposed to be valid to the method "is_valid"
        product_false = {
            "code": 1564647,
            "nutrition_grade_fr": "e",
            "url": "https://www.openfoodfacts.com/Nutella",
            "categories": ["snacks", "snacks_sucrés"],
        }
        # Replaces the self.data in product parser with mocked data in new_init
        with mock.patch(
                "product.ProductParser.__init__",
                self.new_init
        ):
            # Tests method is_valid with a none valid product
            assert not ProductParser().is_valid(product_false)

    def test_parser(self):
        with mock.patch(
                "product.ProductParser.__init__",
                self.new_init
        ):
            ProductParser.data = [
                {
                    "products": [
                        {
                            "code": 1564647,
                            "product_name_fr": "Nutella",
                            "nutrition_grade_fr": "e",
                            "url": "https://www.openfoodfacts.com/Nutella",
                            "categories": "snacks, snacks_sucrés",
                        }
                    ]
                }
            ]
            # Test if the parser method add the data to an object list
            assert len(ProductParser().parser()) == 1
            assert ProductParser().parser()[0].id == 1564647
            assert ProductParser().parser()[0].name == "Nutella"
            assert ProductParser().parser()[0].nutriscore == "e"


class ProductManagerTestCase(TestCase):

    def test_product_manager(self):

        # Mocks a product object
        product = Product(
            1564647,
            "Nütella",
            "e",
            {"noisette": 90},
            "leclerc",
            "https://www.openfoodfacts.com/Nutella",
            "snacks,snacks_sucrés",
            "https://www.openfoodfacts.com/img/Nutella",
        )

        # Mocks the product object list
        products = [product]
        # Gets all products from database
        all_products = DbProduct.objects.all()
        # Gets count of all products from the database
        initial_count = all_products.count()
        # Executes the class method "save_products"
        ProductManager(products).save_products()
        # Gets the new count of all products from database
        new_count = all_products.count()

        # Checks if the product was added to the database
        assert new_count == initial_count + 1
        # Checks if ü was replaced by u
        assert all_products[0].name == "Nutella"


class ApiTestCase(TestCase):

    def setUp(self):

        self.url = "https://fr.openfoodfacts.org/cgi/search.pl"
        self.params = {
            "action": "process",
            "sort_by": "unique_scans_n",
            "page": 1,
            "page_size": 10,
            "json": 1,
            }

    def test_api_response(self):

        response = requests.get(self.url, self.params)
        assert response.status_code == 200
