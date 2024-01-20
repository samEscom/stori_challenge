import csv
import io
from calendar import month_name

import pandas as pd
from pandas import DataFrame

from src.constans import ColumnsNamesEnum, SummaryResumeKeyNames, VarTypesEnum
from src.email import Email


class Summary:
    def __init__(self, csv_file: str):
        self.data: DataFrame = pd.DataFrame()
        self.resume = dict()
        self.__set_data(csv_file)

    def __set_data(self, csv_file) -> None:
        data = list()

        with io.StringIO(csv_file) as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                data.append(row)

        self.data: DataFrame = pd.DataFrame.from_records(data)
        self.data = self.data.astype(
            {
                ColumnsNamesEnum.Transaction.value: VarTypesEnum.floatType.value,
                ColumnsNamesEnum.Id.value: VarTypesEnum.intType.value,
            }
        )

    def __save_data(self) -> None:
        pass

    def __set_total_balance(self) -> None:
        balance = self.data[ColumnsNamesEnum.Transaction.value].sum()
        self.resume[SummaryResumeKeyNames.totalBalance.value] = balance

    def __set_average_credit(self) -> None:
        credit_amount_average = self.data[
            self.data[ColumnsNamesEnum.Transaction.value] > 0
        ][ColumnsNamesEnum.Transaction.value].mean()
        self.resume[
            SummaryResumeKeyNames.averageCreditAmount.value
        ] = credit_amount_average

    def __set_average_debit(self) -> None:
        debit_amount_average = self.data[
            self.data[ColumnsNamesEnum.Transaction.value] < 0
        ][ColumnsNamesEnum.Transaction.value].mean()
        self.resume[
            SummaryResumeKeyNames.averageDebitAmount.value
        ] = debit_amount_average

    def __set_transactions_by_months(self) -> None:
        dates = self.data[ColumnsNamesEnum.Date.value].tolist()
        months = [int(i.split("/")[0]) for i in dates]

        transactions = list()
        for month_number in range(1, 13):
            month_total = months.count(month_number)

            if month_total > 0:
                transactions.append({
                    SummaryResumeKeyNames.monthName.value: month_name[month_number],
                    SummaryResumeKeyNames.numberTransactionOfMonth.value: month_total,
                })

        self.resume[SummaryResumeKeyNames.transactionsByMonths.value] = transactions

    def __process_data(self) -> None:
        self.__set_total_balance()
        self.__set_average_credit()
        self.__set_average_debit()
        self.__set_transactions_by_months()

    def execute(self) -> None:

        self.__save_data()
        self.__process_data()

    def send_email(self, email_str: str) -> int:

        email = Email()
        message = email.create_template(self.resume)

        return email.send(email_str, message)
