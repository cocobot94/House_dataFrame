import sys
from Conexion import Conection


class Pool_Cursor:
    def __init__(self) -> None:
        self._conection = None
        self._cursor = None

    def __enter__(self):
        self._conection = Conection.get_conection()
        self._cursor = self._conection.cursor()
        return self._cursor

    def __exit__(self, type_exc, value_exc, traceback):
        if value_exc:
            self._conection.rollback()
        else:
            self._conection.commit()
        self._cursor.close()
        Conection().put_conection(self._conection)
