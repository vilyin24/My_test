VALID_RESPONSE_SCHEMA = {
        "type": "object",
        "properties": {
            "result": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "componentGroups": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "displayName": {"type": "string"},
                                "hidden": {"type": "boolean"},
                                "components": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "type": {"type": "string"},
                                            "label": {"type": "string"},
                                            "hidden": {"type": "boolean"},
                                            "parameters": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "key": {"type": "string"},
                                                        "value": {"type": ["string", "null"]},
                                                        "boolValue": {"type": ["boolean", "null"]},
                                                        "hidden": {"type": "boolean"},
                                                        "isRequired": {"type": "boolean"},
                                                        "readOnly": {"type": "boolean"}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "actions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string"},
                                "actionUrl": {"type": "string"},
                                "buttonName": {"type": ["string", "null"]},
                                "disabled": {"type": "boolean"},
                                "includeStepParameters": {"type": "boolean"}
                            }
                        }
                    },
                    "isFinished": {"type": "boolean"},
                    "isFinalScreen": {"type": "boolean"},
                    "stepType": {"type": "integer"}
                },
            },
            "success": {"type": "boolean"},
            "errorCode": {"type": "integer"}
        },
        "required": ["result", "success", "errorCode"]
    }

class ValidateResponseBody:
    @staticmethod
    def validate_response(response_schema):
        # Пример простой валидации
        from jsonschema import validate
        validate(instance=response_schema, schema=VALID_RESPONSE_SCHEMA)