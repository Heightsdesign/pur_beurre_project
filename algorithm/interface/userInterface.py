"""Main file, contains program interaction with user"""

from db_and_objects import product
from interface import constants
from db_and_objects import Favorite

"""constants.selection"""


class UserInterface:
    # This class contains the fonctions needed for the user's
    # interaction with the interface

    def __init__(self):
        self.productmanager = product.ProductManager("product")

    def menu_constructor(self, lst):
        # Builds a menu with a given list

        print("\n")

        self.lst = lst
        x = 0

        for i in self.lst:
            x += 1
            print("\t" + str(x) + ". " + str(i))

        print("\n")

    def home_menu(self):
        # Handles the choices made in the home menu

        while True:

            menu = input(
                "Veuillez selectionner une option "
                "(entrez le chiffre correspondant ou entrez q pour quitter): "
            )
            print("\n")
            try:

                if int(menu) == 1:
                    constants.menu_choice.append(1)
                    break
                elif int(menu) == 2:
                    constants.menu_choice.append(2)
                    break

            except ValueError:

                if str(menu) == "q":
                    constants.menu_choice.append("q")
                    break
                else:
                    print(
                        "\n <<<Saisie incorrecte, veuillez "
                        "entrer le chiffre correspondant "
                        "au menu souhaité ou entrez q pour quitter.>>> \n"
                    )
                    self.menu_constructor(self.lst)

    def menu_selector(self):
        # Adds a number to a variable representing choice
        # made in the home menu and redirects
        # to the next selected menu

        if constants.menu_choice[0] == 1:
            print("\t" + "CATEGORIES")
            constants.categories_menu = 1
        elif constants.menu_choice[0] == 2:
            print("\t" + "FAVORIES")
            constants.favorites_menu = 1

    def categories_menu(self):
        # Builds the categories menu and handles the choices

        while constants.categories_menu == 1:

            constants.categories_choice = input(
                "Veuillez séléctionner la catégorie d'aliments "
                "que vous souhaitez substituer "
                "(entrez le chiffre correspondant ou q pour "
                "quitter le programme): "
            )
            print("\n")

            try:
                if (
                    int(constants.categories_choice) > 0
                    and int(constants.categories_choice) < 10
                ):

                    products_category = self.productmanager.products_category_fetcher()
                    num = 0
                    self.products_num = []
                    for prod in products_category:
                        num += 1
                        self.products_num.append(num)
                        print("\t" + str(num) + ". " + str(prod[1]))
                    break

            except ValueError:
                if str(constants.categories_choice) == "q":
                    print("Merci d'avoir utlisé Pur Beurre, à bientôt :) \n")
                    break

                elif str(constants.categories_choice) != "q":
                    print(
                        "\n"
                        + "<<< Saisie incorrecte veuillez entrer "
                        + "un chiffre correspondant "
                        + "à la catégorie souhaitée ou entrez q "
                        + "pour quitter le programme. >>>"
                        + "\n"
                    )

        return self.products_num

    def product_selection(self):
        # Could be called product selection menu,
        # handles the selection made by the user
        print("\n")

        while constants.categories_menu == 1:

            constants.product_input = input(
                "Veuillez séléctionner le produit "
                "que vous souhaitez substituer "
                "(Entrez le chiffre correspondant): "
            )

            try:
                if int(constants.product_input) in self.products_num:
                    self.productmanager.get_product_substitutes()
                    prodselect = self.productmanager.get_product_substitutes_2()
                    break

            except ValueError:
                if str(constants.product_input) == "q":
                    prodselect = 0
                    constants.categories_menu = 0
                    break

                elif str(constants.product_input) != "q":
                    print(
                        "\n"
                        + "<<<Saisie incorrecte veuillez "
                        + "entrer un chiffre correspondant "
                        + "au produit souhaité ou entrez q "
                        + "pour quitter le programme.>>>"
                        + "\n"
                    )

        return prodselect

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

        self.favorite = []
        self.nutriscore = (
            str(self.productmanager.get_product_nutriscore()[0])
            .replace(",", "")
            .replace("'", "")
            .replace("(", "")
            .replace(")", "")
        )
        self.nutriscore = self.give_letter_value(self.nutriscore)
        product_count = 0
        for result in prodselect:
            for attributes in result:
                if (
                    self.nutriscore < self.give_letter_value(attributes[3])
                    and self.give_letter_value(attributes[3])
                    <= self.nutriscore + 2
                ):
                    product_count += 1

                    self.favorite.append(result)

                    if (
                        product_count == 0
                        and self.give_letter_value(attributes[3])
                        < self.nutriscore + 3
                    ):
                        product_count += 1
                        self.favorite.append(result)

                    elif (
                        product_count == 0
                        and self.give_letter_value(attributes[3])
                        < self.nutriscore + 4
                    ):
                        product_count += 1
                        self.favorite.append(result)

                    elif product_count > 1:
                        self.favorite.pop(1)

                elif self.nutriscore == 4:
                    product_count += 1
                    self.favorite.append(result)

                    if product_count > 1:
                        self.favorite.pop(1)

        for prod in self.favorite:
            for attribute in prod:
                print(
                    "_________________________________________________________"
                    + "__________________________________________________"
                    + "\n"
                )
                print("Nom: " + str(attribute[0]) + "\n")
                print("Code: " + str(attribute[1]) + "\n")
                print("Ingredients: " + str(attribute[2]) + "\n")
                print("Nutriscore: " + str(attribute[3]) + "\n")
                print("URL: " + str(attribute[4]) + "\n")
                print(
                    "_________________________________________________________"
                    + "__________________________________________________"
                    + "\n"
                )

        return self.favorite[0]

    def favorite_saver(self):
        # This method allows the user to save in the db the substitute,
        # it actually just saves the id of the product
        # which is to be retrieved when he gets to the favorites menu.

        save_favorite = input(
            "\n"
            + "Voulez-vous ajouter ce substitut à vos favoris ? (y/n)"
            + "\n"
        )
        if save_favorite == "y":
            for attribute in self.favorite[0]:
                constants.fav = str(attribute[1])
            Favorite.Favorite(constants.fav).save()

        elif save_favorite == "n":
            constants.categories_menu = 0

        else:
            print(
                "\n"
                + "<<<Saisie incorrecte veuillez "
                + "entrer un chiffre correspondant "
                + "au produit souhaité ou entrez q "
                + "pour quitter le programme.>>>"
                + "\n"
            )

    def favorites_menu(self):
        # This method shows the favorites in the favorites menu

        Favorite.Favorite(constants.fav).parser()

    def run_user_interface(self):

        self.menu_constructor(constants.selection)
        self.home_menu()
        self.menu_selector()

        if constants.categories_menu == 1:
            try:
                self.menu_constructor(constants.categories_menu_list)
                self.categories_menu()
                prodselect = self.product_selection()

            except AttributeError:
                constants.categories_menu = 0

        if constants.categories_menu == 1:

            self.result_parser(prodselect)
            self.favorite_saver()

        elif constants.favorites_menu == 1:
            self.favorites_menu()

        else:
            print("\n Merci d'avoir utlisé Pur Beurre, à bientôt :) \n")
