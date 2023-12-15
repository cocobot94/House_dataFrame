import sys
from psycopg2 import pool


class Conection:
    _USER = "postgres"
    _PASSWORD = "admin"
    _PORT = "5432"
    _HOST = "localhost"
    _DATABASE = "conexion"
    _MIN_CON = 1
    _MAX_CON = 5
    _pool = None

    # getting the pool connection
    @classmethod
    def get_pool(cls):
        if cls._pool == None:
            try:
                cls._pool = pool.SimpleConnectionPool(
                    cls._MIN_CON,
                    cls._MAX_CON,
                    user=cls._USER,
                    password=cls._PASSWORD,
                    port=cls._PORT,
                    host=cls._HOST,
                    database=cls._DATABASE,
                )
                return cls._pool
            except Exception:
                print("Ha ocurrido un error")
                sys.exit()
        return cls._pool

    @classmethod
    def get_conection(cls):
        conection = cls.get_pool().getconn()
        return conection

    @classmethod
    def put_conection(cls, conection):
        cls.get_pool().putconn(conection)

    @classmethod
    def close(cls):
        cls.get_pool().closeall()
