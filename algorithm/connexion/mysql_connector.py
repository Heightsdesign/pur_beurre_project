import mysql.connector
import psycopg2

"""db_pur_beurre = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Eugenia06240",
    # database = 'pur_beurre'
)

dbcursor = db_pur_beurre.cursor(buffered=True)"""

db_pur_beurre = psycopg2.connect(
                            user="postgres",
                            password="Eug&nia06240",
                            host="127.0.0.1",
                            port="5432",
                            database="pur_beurre",
                            )
db_pur_beurre.set_client_encoding('UTF8')
dbcursor = db_pur_beurre.cursor()


