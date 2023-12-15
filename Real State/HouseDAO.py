from Pool_Cursor import Pool_Cursor
from sqlalchemy import create_engine
import pandas as pd
from cleaning_data import Clean_data


class HouseDAO:
    def __init__(self, file, name) -> None:
        self.file = file
        self.name = name

    # limpia los datos de un archivo csv
    def __clean_csv(self):
        clean = Clean_data()
        clean.cleaning(self.file)
        return

    # crea una tabla
    def create_table(self):
        with Pool_Cursor() as cursor:
            columns_and_types = [
                ("id", "SERIAL PRIMARY KEY NOT NULL "),
            ]
            df = pd.read_csv(self.file)
            for columna in df.columns:
                if df[columna].dtype == "int64":
                    columns_and_types.append((columna, "INTEGER NOT NULL"))
                elif df[columna].dtype == "float64":
                    columns_and_types.append((columna, "DOUBLE PRECISION NOT NULL"))
                else:
                    columns_and_types.append((columna, "VARCHAR(100) NOT NULL"))
            query = f"CREATE TABLE {self.name} ({', '.join([f'{col[0]} {col[1]}' for col in columns_and_types])})"
            cursor.execute(query)

    # inserta el dataframe en la tabla si esta creada
    def insert_data(self):
        self.__clean_csv()
        df = pd.read_csv(self.file)
        engine = create_engine(f"postgresql://postgres:admin@localhost:5432/conexion")
        df.to_sql(self.name, engine, if_exists="append", index=False)

    # return a DataFrame from the data base
    def create_df_from_db(self):
        with Pool_Cursor() as cursor:
            sentence = "SELECT * FROM houses ORDER BY price"
            cursor.execute(sentence)
            registros = cursor.fetchall()
            cursor.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.name}'"
            )
            columnas = cursor.fetchall()
            df = pd.DataFrame(registros, columns=[columna[0] for columna in columnas])
            return df

    # vacia la tabla
    def limpiar_tabla(self):
        with Pool_Cursor() as cursor:
            sentence = f"DELETE FROM {self.name};"
            cursor.execute(sentence)

    # elimina la tabla
    def eliminar_tabla(self):
        with Pool_Cursor() as cursor:
            sentence = f"DROP TABLE {self.name};"
            cursor.execute(sentence)


if __name__ == "__main__":
    file = "house.csv"
    name = "houses"
    h = HouseDAO(file, name)
    # h.create_table()
    # h.insert_data()
    # h.limpiar_tabla()
    # h.eliminar_tabla()
    h.create_df_from_db()
