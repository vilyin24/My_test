def request_company_name(companyName):
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
        {"key": "CompanyName", "value": companyName},
        {"key": "INN", "value": "7328070354"},
        {"key": "PositionType", "value": "MiddleManager"},
        {"key": "AverageMonthlyIncome", "numberValue": 100000},
        {"key": "WorkLengthYears", "numberValue": 0},
        {"key": "WorkLengthMonths", "numberValue": 3}
    ]
    }