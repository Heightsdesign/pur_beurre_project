# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main file, launches application"""

from db_and_objects.product import ProductParser
from db_and_objects.database import Database
from interface.userInterface import UserInterface
from connexion.db_checker import db_check


def main():
    # main fonction launches the application, checks if db exists, creates it if not
    print(
        "<<< Bienvenue, l'application Pur Beurre vous permet de substituer "
        "vos aliments favoris par des alternatives plus saines. >>>\n"
    )

    # if db_check() == 0:
    product_parser = ProductParser().parser()
    product_manager = Database(product_parser).database_constructor()
    UserInterface().run_user_interface()
    # else:
    # UserInterface().run_user_interface()
    # launch application


if __name__ == "__main__":
    main()
    import django

    django.setup()
