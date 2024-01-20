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
