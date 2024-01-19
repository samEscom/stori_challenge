import csv
import io

import pandas as pd
from pandas import DataFrame


class Summary:
    def __init__(self, csv_file: str):
        self.data: DataFrame = pd.DataFrame()
        self.__set_data(csv_file)

    def __set_data(self, csv_file) -> None:
        data = list()

        with io.StringIO(csv_file) as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                data.append(row)

        self.data: DataFrame = pd.DataFrame.from_records(data)

    def __save_data(self) -> None:
        pass

    def __process_data(self) -> None:
        pass

    def execute(self) -> None:

        self.__save_data()
        self.__process_data()

    def send_email(self, email: str) -> int:

        return 0
