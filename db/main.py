import pymysql
import pprint
<<<<<<< HEAD
from config import host, user, password, db_name

try:
    connection = pymysql.connect(
    host = host,
    port= 3306,
    user= user,
=======
from mysql.connector import connect, errorcode, Error
from config import host, user, password, db_name

try:
    with connect(
    user=user,
>>>>>>> bc6e36da44065a540a0dbed02dbe7c1c13f17c46
    password= password,
    host = host,
    database=db_name,
<<<<<<< HEAD
    cursorclass= pymysql.cursors.DictCursor # это нужно для того, чтобы получить результат в виде словаря, где ключами будут названия колонок.
    )
    print("Successfully connected")
    print('"#' * 20)

    try:
         with connection.cursor() as cursor:
            _SQL = "insert into log (`phrase`, `letters`, `ip`, `browser_string`, `result`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(_SQL, ('hitch-hiker', 'xyz' , '127.0.0.1', 'Firefox','set()'))
            connection.commit()
            _SQL = """SELECT * FROM LOG"""
            cursor.execute(_SQL)
            for row in cursor.fetchall():
                print(row)

            #   (%(phrase)s, %(letters)s, %(ip)s, %(Brouser)s, %(result)s)
            # ('hitch-hiker','aeiou','127.0.0.1','Firefox',"{'e','i'}")
            #  _SQL = """describe log"""
            #  cursor.execute(_SQL)
            #  pp = pprint.PrettyPrinter(width=41, compact=True)
            #  print("Info from Date Base:\t")
            #  for row in cursor.fetchall():
            #      print(row)
            # pprint.pprint(cursor.fetchall())
=======
    ) as connection:
        print(connection)
    # print("Successfully connected")
    # print('"#' * 20)

    try:
         with connection.cursor() as cursor:
             show_table = "show tables"
             cursor.execute(show_table)
             pprint.print(f"Table creares successfully:\t {cursor.fetchall()}")
>>>>>>> bc6e36da44065a540a0dbed02dbe7c1c13f17c46

    finally:
        connection.close()

except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
        