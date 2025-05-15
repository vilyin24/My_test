def request_body_registration_address(actualAddress):
    return {
        "actionType": "string",
        "context": {
            "operationCode": "string",
            "operationId": "string",
            "contextParameters": [
                {"key": "string", "value": "string", "numberValue": 0, "boolValue": True}
            ]
        },
        "parameters": [
            {"key": "ContactPersonPhone", "value": "9611245131"},
            {"key": "RegistrationAddress", "value": "г Казань, ул Татарстан, д 20, кв 220"},
            {"key": "ActualAddress", "value": actualAddress},
            {"key": "RegistrationAddressIsActual", "value": "false"},
            {"key": "MaritalStatus", "value": "Married"},
            {"key": "Education", "value": "Higher"}
        ]
    }