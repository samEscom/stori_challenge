from enum import Enum


class ColumnsNamesEnum(Enum):
    id = "Id"
    transaction = "Transaction"
    date_transaction = "Date"


class VarTypesEnum(Enum):
    float_type = "float64"
    int_type = "int32"


class SummaryKeyNames(Enum):
    total_balance = "totalBalance"
    average_credit_amount = "averageCreditAmount"
    average_debit_amount = "averageDebitAmount"
    transactions_by_months = "transactionsByMonths"
    month_name = "monthName"
    number_transaction_of_month = "numberTransactionOfMonth"


class SummaryDataNameColumns(Enum):
    id = "Id"
    date_send = "date_send"
    total_balance = "total_balance"
    average_credit_amount = "average_credit_amount"
    average_debit_amount = "average_debit_amount"
    transactions_by_months = "transactions_by_months"


AWS_SERVICE_SES = "ses"
AWS_SERVICE_S3 = "s3"
AWS_REGION_EAST = "us-east-2"

SENDER = "sam.escom@outlook.com"
NAME_FILE = "resumen"
BUCKET_NAME = "resumes-challenge"
