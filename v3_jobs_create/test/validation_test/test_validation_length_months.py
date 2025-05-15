import json

import allure
import pytest
import requests
from config.config import Config
from data.data_test import *
from v3_jobs_create.schemas_validation.schemas_work_lenght_months import request_work_lenght_months


def extract_validation_error(response_json):
    for group in response_json.get("result", {}).get("componentGroups", []):
        for component in group.get("components", []):
            if component.get("label") == "мес":
                return component.get("validationError")
    return None

@allure.feature("POST /v3/preapproved/jobs/create")
@allure.story("Валидация при создании работы")
@allure.title("Тест на валидацию Стажа < 3 Месяцев: brokerId = {broker_id}, biztalkId = {biztalk_id}")
@allure.description("Проверка срабатывания валидации на бэке для поля WorkLenghtMonths")
@pytest.mark.parametrize("workLenghtMonths, expected_error", [
    ("0", "Стаж не может быть меньше трёх месяцев"),
    ("1", "Стаж не может быть меньше трёх месяцев"),
    ("2", "Стаж не может быть меньше трёх месяцев"),
    ("-1", "Стаж не может быть меньше трёх месяцев"),
])

def test_work_lenght_months_validation(workLenghtMonths, expected_error):
    url = f"{Config.BASE_URL_PREAPPROVED}/{VALID_BROKER_ID}/jobs/create/{VALID_BIZTALK_ID}"
    payload = request_work_lenght_months(workLenghtMonths)

    with allure.step("Отправка запроса"):
        response = requests.post(url, json=payload, verify=False)

    with allure.step("Парсим JSON-ответ и валидируем его"):
        response_json = response.json()
        validation_error = extract_validation_error(response_json)

    with allure.step(f"Для поля WorkLenghtMonths сработала валидация. ValidationError = {validation_error}"):
        assert validation_error == expected_error

    with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
        allure.attach(json.dumps(response_json, indent=4, ensure_ascii=False),
                      name="Response JSON",
                      attachment_type=allure.attachment_type.JSON)
