"""Main file, contains program interaction with user"""

from db_and_objects import product
from interface import constants
from substitutes.models import Product as DbProduct


"""constants.selection"""


class SiteDevInterface:

    def __init__(self):
        self.productmanager = product.ProductManager("product")
        self.substitutesfetcher = product.SubstitutesFetcher("Lipton Ice Tea saveur peche 1 L")

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
        self.nutriscore = self.substitutesfetcher.get_product_nutriscore()
        print(self.nutriscore)
        self.nutriscore = self.give_letter_value(self.nutriscore)
        print(self.nutriscore)
        products = []


        for product_name in prodselect:
            product_obj = DbProduct.objects.get(name=product_name)
            products.append(product_obj)

        print(products)

        product_count = 0

        for product in products:
            product_nutriscore = self.give_letter_value(product.nutriscore)
            if (
                self.nutriscore <= 1
                and product_nutriscore
                <= 2
                and product_nutriscore
                > 0
            ):
                product_count += 1
                self.favorites.append(product)

            if (
                self.nutriscore <= 3
                and self.nutriscore > 1
                and product_nutriscore
                >=2
            ):
                product_count += 1
                self.favorites.append(product)

            if (
                self.nutriscore == 4
                and product_nutriscore
                > 2
            ):
                product_count += 1
                self.favorites.append(product)



        for prod in self.favorites:
            print(
                "_________________________________________________________"
                + "__________________________________________________"
                + "\n"
            )
            print("Nom: " + prod.name + "\n")
            print("Code: " + str(prod.id) + "\n")
            print("Nutriscore: " + prod.nutriscore + "\n")
            print("URL: " + prod.url + "\n")
            print(
                "_________________________________________________________"
                + "__________________________________________________"
                + "\n"
            )

        return self.favorites

    def get_product_input(self):

        program_active = 1

        while program_active == 1 :
            self.result_parser(self.substitutesfetcher.get_product_substitutes_2())
            program_active = 0# do something

        return program_active
