from enum import Enum


class ColumnsNamesEnum(Enum):
    Id = "Id"
    Transaction = "Transaction"
    Date = "Date"


class VarTypesEnum(Enum):
    floatType = "float64"
    intType = "int32"


class SummaryResumeKeyNames(Enum):
    totalBalance = "totalBalance"
    averageCreditAmount = "averageCreditAmount"
    averageDebitAmount = "averageDebitAmount"
    transactionsByMonths = "transactionsByMonths"
    monthName = "monthName"
    numberTransactionOfMonth = "numberTransactionOfMonth"


AWS_SERVICE_SES = "ses"
AWS_REGION_WEST = "us-west-2"

SENDER = "correo@algo.com"
NAME_FILE = "resumen"
