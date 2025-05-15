from data.data_test import *

request_body = {
    "actionType": "string",
    "context": {
        "operationCode": "string",
        "operationId": "string",
        "contextParameters": [
            {
                "key": "string",
                "value": "string",
                "numberValue": 123,
                "boolValue": True
            }
        ]
    },
    "parameters": [
        {"key": "CompanyName", "value": str(COMPANY_NAME)},
        {"key": "INN", "value": str(INN)},
        {"key": "PositionType", "value": str(POSITION_TYPE)},
        {"key": "AverageMonthlyIncome", "numberValue": int(AVERAGE_MONTHLY_INCOME)},
        {"key": "WorkLengthYears", "numberValue": int(WORK_LENGTH_YEARS)},
        {"key": "WorkLengthMonths", "numberValue": int(WORK_LENGTH_MONTHS)}
    ]
}