import pymysql
import pprint
from config import host, user, password, db_name

try:
    connection = pymysql.connect(
    host = host,
    port= 3306,
    user= user,
    password= password,
    database=db_name,
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

    finally:
        connection.close()

except Exception as ex:
    print("Connection refused")
    print(ex)

