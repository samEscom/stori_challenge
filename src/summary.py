import csv
import io
from calendar import month_name
from datetime import datetime
from typing import Optional, Union

import pandas as pd
from pandas import DataFrame

from src.aws import Aws
from src.constans import (
    ColumnsNamesEnum,
    SummaryDataNameColumns,
    SummaryKeyNames,
    VarTypesEnum,
)
from src.email import Email


class Summary:
    def __init__(self, email_str: str, file_name: str):
        self.aws = Aws()
        self.save_flag: Union[str, int]
        self.email_str: str = email_str
        self.data_frame: DataFrame = pd.DataFrame()
        self.summary_data = dict()
        self.__set_data(self.aws.get_csv_file(file_name))

    def __set_data(self, csv_file) -> None:
        data = list()
        data_file = csv_file.decode("utf-8")
        with io.StringIO(data_file) as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                data.append(row)

        self.data_frame: DataFrame = pd.DataFrame.from_records(data)
        self.data_frame = self.data_frame.astype(
            {
                ColumnsNamesEnum.transaction.value: VarTypesEnum.float_type.value,
                ColumnsNamesEnum.id.value: VarTypesEnum.int_type.value,
            }
        )

    def __save_data(self) -> None:

        resume_data = {
            SummaryDataNameColumns.id.value: self.email_str,
            SummaryDataNameColumns.date_send.value: str(datetime.now()),
            SummaryDataNameColumns.total_balance.value: str(
                self.summary_data[SummaryKeyNames.total_balance.value]
            ),
            SummaryDataNameColumns.average_debit_amount.value: str(
                self.summary_data[SummaryKeyNames.average_debit_amount.value]
            ),
            SummaryDataNameColumns.average_credit_amount.value: str(
                self.summary_data[SummaryKeyNames.average_credit_amount.value]
            ),
            SummaryDataNameColumns.transactions_by_months.value: self.summary_data[
                SummaryKeyNames.transactions_by_months.value
            ],
        }

        self.save_flag = self.aws.save_data(resume_data)

    def __set_total_balance(self) -> None:
        balance = self.data_frame[ColumnsNamesEnum.transaction.value].sum()
        self.summary_data[SummaryKeyNames.total_balance.value] = balance

    def __set_average_credit(self) -> None:
        credit_amount_average = self.data_frame[
            self.data_frame[ColumnsNamesEnum.transaction.value] > 0
        ][ColumnsNamesEnum.transaction.value].mean()
        self.summary_data[
            SummaryKeyNames.average_credit_amount.value
        ] = credit_amount_average

    def __set_average_debit(self) -> None:
        debit_amount_average = self.data_frame[
            self.data_frame[ColumnsNamesEnum.transaction.value] < 0
        ][ColumnsNamesEnum.transaction.value].mean()
        self.summary_data[
            SummaryKeyNames.average_debit_amount.value
        ] = debit_amount_average

    def __set_transactions_by_months(self) -> None:
        dates = self.data_frame[ColumnsNamesEnum.date_transaction.value].tolist()
        months = [int(i.split("/")[0]) for i in dates]

        transactions = list()
        for month_number in range(1, 13):
            month_total = months.count(month_number)

            if month_total > 0:
                transactions.append(
                    {
                        SummaryKeyNames.month_name.value: month_name[month_number],
                        SummaryKeyNames.number_transaction_of_month.value: month_total,
                    }
                )

        self.summary_data[SummaryKeyNames.transactions_by_months.value] = transactions

    def __process_data(self) -> None:
        self.__set_total_balance()
        self.__set_average_credit()
        self.__set_average_debit()
        self.__set_transactions_by_months()

    def execute(self) -> None:
        self.__process_data()
        self.__save_data()

    def send_email(self) -> Optional[str]:

        email = Email(self.aws)
        message_str = email.create_template(self.summary_data)

        return email.send(
            pd.DataFrame.from_records(self.summary_data), self.email_str, message_str
        )
