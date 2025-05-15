from jsonschema import validate
from jsonschema.exceptions import ValidationError

VALID_RESPONSE = {

  "type": "object",
  "properties": {
    "result": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "componentGroups": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "displayName": { "type": "string" },
              "hidden": { "type": "boolean" },
              "components": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "type": { "type": "string" },
                    "label": { "type": "string" },
                    "hidden": { "type": "boolean" },
                    "parameters": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "key": { "type": "string" },
                          "value": { "type": ["string", "null"] },
                          "numberValue": { "type": ["number", "null"] },
                          "hidden": { "type": "boolean" },
                          "isRequired": { "type": "boolean" },
                          "readOnly": { "type": "boolean" },
                          "numberSettings": {
                            "type": "object",
                            "properties": {
                              "scale": { "type": "integer" }
                            },
                            "required": ["scale"]
                          }
                        },
                        "required": ["key"]
                      }
                    },
                    "options": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "key": { "type": "string" },
                          "value": { "type": "string" }
                        },
                        "required": ["key", "value"]
                      }
                    }
                  },
                  "required": ["type", "label", "hidden"]
                }
              }
            },
            "required": ["displayName", "hidden", "components"]
          }
        },
        "actions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string" },
              "actionUrl": { "type": "string" },
              "buttonName": { "type": "string" },
              "disabled": { "type": "boolean" },
              "includeStepParameters": { "type": "boolean" }
            }
          }
        },
        "isFinished": { "type": "boolean" },
        "isFinalScreen": { "type": "boolean" },
        "stepType": { "type": "integer" }
      },
      "required": ["title", "componentGroups", "actions", "isFinished", "isFinalScreen", "stepType"]
    },
    "success": { "type": "boolean" },
    "errorCode": { "type": "integer" }
  },
  "required": ["result", "success", "errorCode"]
}

class ValidateResponseBody:

    # Функция для валидации JSON-ответа по схеме и проверки stepType
    @staticmethod
    def validate_response(response_data):

        try:
            validate(instance=response_data, schema=VALID_RESPONSE)
        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации JSON-схемы: {e.message}")

        # Проверяем, что stepType = 3 (должен быть при успешном запросе)
        assert "result" in response_data, "Поле 'result' отсутствует в респонсе"
        step_type = response_data["result"].get("stepType")
        assert step_type == 3, f"Ожидалось stepType = 3, но получено {step_type}"