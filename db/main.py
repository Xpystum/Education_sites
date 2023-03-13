import pymysql
import pprint
from mysql.connector import connect, errorcode, Error
from config import host, user, password, db_name

try:
    with connect(
    user=user,
    password= password,
    host = host,
    database=db_name,
    ) as connection:
        print(connection)
    # print("Successfully connected")
    # print('"#' * 20)

    try:
         with connection.cursor() as cursor:
             show_table = "show tables"
             cursor.execute(show_table)
             pprint.print(f"Table creares successfully:\t {cursor.fetchall()}")

    finally:
        connection.close()

except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
        