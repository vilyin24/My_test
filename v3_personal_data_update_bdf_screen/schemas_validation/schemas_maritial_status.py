def request_body_maritial_status(maritialStatus):
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
            {"key": "ActualAddress", "value": "г Казань, ул Татарстан, д 20, кв 220"},
            {"key": "RegistrationAddressIsActual", "value": "true"},
            {"key": "MaritalStatus", "value": maritialStatus},
            {"key": "Education", "value": "Higher"}
        ]
    }