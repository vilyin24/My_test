import json

import allure
import pytest
import requests
from config.config import Config
from data.data_test import *
from v3_jobs_update.schemas_validation.schemas_position_type import request_position_type


def extract_validation_error(response_json):
    for group in response_json.get("result", {}).get("componentGroups", []):
        for component in group.get("components", []):
            if component.get("label") == "Квалификация":
                return component.get("validationError")
    return None

@allure.feature("POST /v3/preapproved/jobs/update")
@allure.story("Валидация при обновлении работы")
@allure.title("Тест на валидацию Квалификации: brokerId = {broker_id}, biztalkId = {biztalk_id}")
@allure.description("Проверка срабатывания валидации на бэке для поля PositionType")
@pytest.mark.parametrize("positionType, expected_error", [
    ("", "Квалификация не может быть пустой"),
])

def test_position_type_validation(positionType, expected_error):
    url = f"{Config.BASE_URL_PREAPPROVED}/{VALID_BROKER_ID}/jobs/{job_id}/update/{VALID_BIZTALK_ID}"
    payload = request_position_type(positionType)

    with allure.step("Отправка запроса"):
        response = requests.post(url, json=payload, verify=False)

    with allure.step("Парсим JSON-ответ и валидируем его"):
        response_json = response.json()
    validation_error = extract_validation_error(response_json)

    with allure.step(f"Для поля PositionType сработала валидация. ValidationError = {validation_error}"):
        assert validation_error == expected_error

    with allure.step("Проверяем, что при срабатывании валидации stepType = 0"):
        step_type = response_json.get("result", {}).get("stepType", "")
    assert step_type == 0, f"Ожидали stepType = 0, а получили stepType = {step_type}"

    with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
        allure.attach(json.dumps(response_json, indent=4, ensure_ascii=False),
                      name="Response JSON",
                      attachment_type=allure.attachment_type.JSON)
