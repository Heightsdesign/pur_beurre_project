# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file uses the data collected from the api file
and creates and object Product from it
and adds the object in a list"""

import sys
import os
sys.path.append('D:\Openclassrooms\P8\pur_beurre_project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pur_beurre.settings'
import django
django.setup()
sys.path.append("D:/Openclassrooms/P8/pur_beurre_project/algorithm")
from substitutes.models import Product as DbProduct
from substitutes.models import Categories as DbCategories
from substitutes.models import Nutriments as DbNutriments
from algorithm.db_and_objects.api import ProductDownloader
import algorithm.db_and_objects.constants as constants


class Product:
    """Creating Product object"""

    def __init__(
        self,
        id,
        name,
        nutriscore,
        nutriments,
        stores,
        url,
        categories, img_url
    ):

        # initializes the object with attributes passed as arguments
        self.id = id
        self.name = name
        self.nutriscore = nutriscore
        self.nutriments = nutriments
        self.stores = stores
        self.url = url
        self.categories = categories
        self.img_url = img_url


class ProductParser:
    """Iterates through the data and "
    creates objects from of it and adds them to a list"""

    def __init__(self):
        # initializes object ProductParser,
        # the parameters passed as an argument are determined
        # in the ProductDownloader class
        self.data = ProductDownloader().response()

    def is_valid(self, prod):
        # verifies if products attributes are valid

        self.prod = prod

        # keys = attributes considered necessary to add a product to our list
        keys = ("code", "product_name_fr", "nutrition_grade_fr", "categories")
        for key in keys:
            # checking if the attributes or their value exists
            if key not in prod or not prod[key]:
                return False
        return True

    def parser(self):
        # Iterates through data,
        # creates object from it and adds them to a list

        obj_list = []
        for page in self.data:
            products = page["products"]
            for prod in products:
                # print(type(prod["nutriments"]), prod["nutriments"])
                if self.is_valid(prod):
                    product = Product(
                        prod["code"],
                        prod["product_name_fr"],
                        prod["nutrition_grade_fr"],
                        prod.get("nutriments", ""),
                        prod.get("stores", ""),
                        prod["url"],
                        prod["categories"],
                        prod.get("image_url", ""),
                    )

                    obj_list.append(product)
        return obj_list


class ProductManager:
    """Methods to execute with product objects"""

    def __init__(self, products):

        self.product_list = products

    def win1252_parser(self, word):

        for letter in word:
            if letter not in constants.win_1252_charlist2:
                word = word.replace(str(letter), "")

        return word

    def save_products(self):
        # Inserts products in database

        for product in self.product_list:

            # Replaces unwanted characters
            product_name = (
                product.name.replace("é", "e")
                .replace("è", "e")
                .replace("à", "a")
                .replace("î", "i")
                .replace("â", "a")
                .replace("ü", "u")
                .replace("ß", " ")
                .replace("ô", "o")
                .replace("ê", "e")
                .replace("ë", "e")
                .replace("ï", "i")
                .replace("û", "u")
                .replace("œ", "oe")
                .replace("Ê", "E")
                .replace("É", "E")
                .replace("ã", "")
                .replace("Î", "I")
                .replace("ó", "o")
                .replace("Œ", "OE")
                .replace("Â", "A")
                .replace("ú", "u")
                .replace("ö", "o")
                .replace("ä", "a")
            )

            # Parses the product name
            product_name = self.win1252_parser(product_name)
            product_nutriscore = product.nutriscore
            product_nutriments = product.nutriments
            product_url = product.url
            product_img_url = product.img_url
            product_categories = product.categories

            product = DbProduct(
                name=product_name,
                nutriscore=product_nutriscore,
                url=product_url,
                imgurl=product_img_url,
            )

            product.save()

            product_categories = product_categories.split(",")

            for category in product_categories:

                # Replaces unwanted characters
                category = (
                    category.replace("'", " ")
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("à", "a")
                    .replace("î", "i")
                    .replace("â", "a")
                    .replace("ü", "u")
                    .replace("ß", " ")
                    .replace("ô", "o")
                    .replace("ê", "e")
                    .replace("ë", "e")
                    .replace("ï", "i")
                    .replace("û", "u")
                    .replace("œ", "oe")
                    .replace("Ê", "E")
                    .replace("🍓", " ")
                    .replace("É", "E")
                    .replace("ã", "")
                    .replace("Î", "I")
                    .replace("ó", "o")
                    .replace("Œ", "OE")
                    .replace("Â", "A")
                    .replace("ú", "u")
                    .replace("ö", "o")
                    .replace("ä", "a")
                )
                category = self.win1252_parser(category)

                cat = DbCategories.objects.create(name=category)
                product.categories.add(cat)

            for nutriment_name, nutriment_value in product_nutriments.items():
                if type(nutriment_value) != type(1):
                    nutriment_value = 0
                    nut = DbNutriments.objects.create(
                        name=nutriment_name,
                        value=nutriment_value
                    )
                    product.nutriments.add(nut)
                else:
                    nut = DbNutriments.objects.create(
                        name=nutriment_name,
                        value=nutriment_value
                    )
                    product.nutriments.add(nut)

    def delete_doubles(self, dbobject):

        # Deletes doubles in dbobject table
        for row in dbobject.objects.all().reverse():
            if dbobject.objects.filter(name=row.name).count() > 1:
                row.delete()


class SubstitutesFetcher:
    def __init__(self, product_input):

        self.product_input = product_input

    def get_product_nutriscore(self):

        # Gets the product nutriscore
        self.product = DbProduct.objects.get(name=self.product_input)
        nutriscore = self.product.nutriscore

        return nutriscore

    def get_product_categories(self):
        # Gets the categories associated with a product
        # Gets the product from db passed as an arg to class
        self.product = DbProduct.objects.get(name=self.product_input)

        # Gets the categories attached to product
        self.categories = self.product.categories.all()

        # inserts the categories names in a list
        self.product_cats = []
        for category in self.categories:
            self.product_cats.append(category.name)

        return self.product_cats

    def get_product_substitutes(self):
        # Gets the substitutes of a product 1/2
        self.product_cats = self.get_product_categories()

        self.substitutes_categories = []
        self.substitutes_names = []
        self.substitutes = {}

        # gets all products that shares one category in common with product
        for category in self.product_cats:
            products = DbProduct.objects.filter(
                categories__name__icontains=category
            )

        # gets all the categories of all products
        for product in products:

            self.substitutes_categories = list(product.categories.all())

            self.substitutes.update([(
                product.name,
                self.substitutes_categories
            )])

        return self.substitutes

    def get_product_substitutes_2(self):
        # Gets the substitutes of a product 2/2

        self.substitutes = self.get_product_substitutes()

        substitutes_final = []
        for substitute, categories in self.substitutes.items():
            shared_categories = 0
            for category in categories:
                if category.name in self.get_product_categories():
                    shared_categories += 1
            self.substitutes.update([(substitute, shared_categories)])

        sorted_substitutes = sorted(
            self.substitutes.items(), key=lambda x: x[1], reverse=True
        )
        # sorts the substitutes by most
        # shared categories with the original product

        for key, shared_cat in sorted_substitutes:
            if shared_cat > 1:
                substitutes_final.append(key)

        return substitutes_final


class FinalParser:
    def __init__(self, fetcher):

        self.fetcher = fetcher

    def give_letter_value(self, arg):
        # This method takes a nutriscore as an argument
        # and turns it into a score (int)
        # based on the value associated
        # with it in constants.nutriscore variable

        self.arg = arg
        for letter in arg:
            if letter in constants.nutriscore:
                score = constants.nutriscore[letter]

        return score

    def result_parser(self, prodselect):
        # This method compares the possible subtitutes from a list
        # (previously sorted by the most categories shared
        # with the selected product)
        # and gets the products with closest nutriscore
        # then finally prints it in a readable manner.

        self.favorites = []
        self.nutriscore = self.fetcher.get_product_nutriscore()

        self.nutriscore = self.give_letter_value(self.nutriscore)

        products = []

        for product_name in prodselect:
            product_obj = DbProduct.objects.get(name=product_name)
            products.append(product_obj)

        product_count = 0

        for product in products:
            product_nutriscore = self.give_letter_value(product.nutriscore)
            if (
                self.nutriscore <= 1
                and product_nutriscore <= 2
                and product_nutriscore > 0
            ):
                product_count += 1
                self.favorites.append(product)

            if (
                self.nutriscore <= 3
                and self.nutriscore > 1
                and product_nutriscore >= 2
            ):
                product_count += 1
                self.favorites.append(product)

            if self.nutriscore == 4 and product_nutriscore > 2:
                product_count += 1
                self.favorites.append(product)

        return self.favorites


    # prods = ProductParser().parser()
    # manager = ProductManager(prods)
    # manager.save_products()
    # manager.delete_doubles(DbProduct)
    # ProductManager('prods').delete_doubles(DbProduct)
