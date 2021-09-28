"""This file contains fonction to check if the database is already created"""
from connexion.mysql_connector import dbcursor
from sqlalchemy_utils.functions import database_exists
from django.conf import settings



"""def db_check():
    #this fonction checks if the database pur beurre exists if it does returns 1 else 0
    dbcursor.execute(
        "SELECT schema_name FROM information_schema.schemata "
        "WHERE schema_name = 'pur_beurre';"
        )

    db_exists = dbcursor.fetchall()
    return len(db_exists)"""

def db_check():

    if database_exists(settings["SQLALCHEMY_DATABASE_URI"]):
        db_exists = 1
    else:
        db_exists = 0

    return db_exists
