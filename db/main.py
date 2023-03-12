import pymysql
from mysql.connector import connect, Error
from config import host, user, password, db_name

try:
    connection = pymysql.connect(
    host = host,
    port=3306,
    user=user,
    password= password,
    database=db_name,
    cursorclass= pymysql.cursors.DictCursor
    )
    print("Successfully connected")
    print('"#' * 20)

    # try:
    #    
    # except:
    #     sdfgsdf
    # finally:
    #     connection.close()
    try:
         with connection.cursor() as cursor:
             show_table = "show tables"
             cursor.execute(show_table)
             print(f"Table creares successfully:\t {cursor.fetchall()}")

    finally:
        connection.close()

except Exception as ex:
    print("Connection refused")
    print(ex)

