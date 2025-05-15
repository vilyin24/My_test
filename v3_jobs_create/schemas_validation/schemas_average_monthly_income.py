def request_average_monthly_income(monthlyIncome):
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
        {"key": "AverageMonthlyIncome", "numberValue": monthlyIncome},
        {"key": "WorkLengthYears", "numberValue": 0},
        {"key": "WorkLengthMonths", "numberValue": 3}
    ]
    }