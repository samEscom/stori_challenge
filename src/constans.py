from enum import Enum


# Name of columns on CSV file
class ColumnsNamesEnum(Enum):
    id = "Id"
    transaction = "Transaction"
    date_transaction = "Date"


class VarTypesEnum(Enum):
    float_type = "float64"
    int_type = "int32"


# The name of the keys  output body if success
class SummaryKeyNames(Enum):
    total_balance = "totalBalance"
    average_credit_amount = "averageCreditAmount"
    average_debit_amount = "averageDebitAmount"
    transactions_by_months = "transactionsByMonths"
    month_name = "monthName"
    number_transaction_of_month = "numberTransactionOfMonth"


# The name of the columns of the table
class SummaryDataNameColumns(Enum):
    id = "Id"
    date_send = "date_send"
    total_balance = "total_balance"
    average_credit_amount = "average_credit_amount"
    average_debit_amount = "average_debit_amount"
    transactions_by_months = "transactions_by_months"


# AWS SERVICES
AWS_SERVICE_SES = "ses"
AWS_SERVICE_S3 = "s3"
AWS_REGION_EAST = "us-east-2"
AWS_SERVICE_DYNAMO = "dynamodb"

# AWS SES SENDER
SENDER = "sam.escom@outlook.com"
NAME_FILE = "resumen"

# AWS VARS of bucket and name of table
BUCKET_NAME = "resumes-challenge"
TABLE_NAME = "summaries"


EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


# HTTP CONFIG
ACCESS_KEY = "A"
POST_METHOD = "POST"
