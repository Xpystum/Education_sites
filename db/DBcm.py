import pymysql


class CredentialsError(Exception):
    pass

class SQLError(Exception):
    pass

class ConnectionError(Exception):
    pass

class DbConfing: 
    def __init__(self,host:str , user: str , port:int ,password: str , db_name: str) -> None:
         self.host = host
         self.user = user
         self.port = port
         self.password = password
         self.database = db_name

class UseDatabase:
    def __init__(self, DbConfing) -> None:
        self.host = DbConfing.host
        self.user = DbConfing.user
        self.port = DbConfing.port
        self.password = DbConfing.password
        self.database = DbConfing.database
        
    def __enter__(self) -> 'cursor':
        try:
            self.connection = pymysql.connect(
                                host = self.host,
                                port = self.port,
                                user = self.user,
                                password =  self.password,
                                database = self.database,
                                cursorclass = pymysql.cursors.DictCursor,)# это нужно для того, чтобы получить результат в виде словаря, где ключами будут названия колонок.
            self.cursor = self.connection.cursor()
            return self.cursor
        except pymysql.err.InternalError as err:
            raise ConnectionError(err)
        except pymysql.err.ProgrammingError as err:
            raise CredentialsError(err)
        
    def __exit__(self, exc_type, exc_value,exc_trace) -> None:
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        if exc_type is pymysql.err.ProgrammingError:
            raise SQLError(exc_value)
        elif exc_type:
            raise exc_type(exc_value)
        