# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main file, launches application"""

# from interface.userInterface import SiteDevInterface
import sys

sys.path.append("D:/Openclassrooms/P8/pur_beurre_project/algorithm")


"""
def main():
    # main fonction launches the application, checks if db exists, creates it if not
    print(
        "<<< Bienvenue, l'application Pur Beurre vous permet de substituer "
        "vos aliments favoris par des alternatives plus saines. >>>\n"
    )

    SiteDevInterface().get_product_input()
"""


if __name__ == "__main__":
    main()
    import django

    django.setup()
