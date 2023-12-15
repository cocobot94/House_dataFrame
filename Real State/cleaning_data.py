import re
import pandas as pd


class Clean_data:
    def __cleaned_data(self, values):
        return re.sub(r"[^0-9.]", "", str(values))

    # fiference between apply--> (for a column)& applymap--> (for the entire df)

    def cleaning(self, file):
        df = pd.read_csv(file)
        for columna in df.columns:
            if df[columna].dtype != str:
                df[columna] = df[columna].apply(self.__cleaned_data)
                df[columna] = pd.to_numeric(df[columna], errors="coerce")
        df = df.fillna(df.mean().round(3))
        df.to_csv(file, index=False)


if __name__ == "__main__":
    file = "house.csv"
    c = Clean_data()
    c.cleaning(file)
