def request_work_lenght_months(workLenghtMonths):
    return {
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
        {"key": "CompanyName", "value": "АО СПЗ"},
        {"key": "INN", "value": "7328070354"},
        {"key": "PositionType", "value": "MiddleManager"},
        {"key": "AverageMonthlyIncome", "numberValue": 100000},
        {"key": "WorkLengthYears", "numberValue": 0},
        {"key": "WorkLengthMonths", "numberValue": workLenghtMonths}
    ]
    }