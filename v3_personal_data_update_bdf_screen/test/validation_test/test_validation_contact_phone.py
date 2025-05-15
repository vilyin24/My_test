import json

import pytest
import requests
import allure
from config.config import Config
from data.data_test import *
from v3_personal_data_update_bdf_screen.schemas_validation.schemas_contact_person_phone import request_body_phone


def extract_validation_error(response_json):
    for group in response_json.get("result", {}).get("componentGroups", []):
        for component in group.get("components", []):
            if component.get("label") == "Телефон контактного лица":
                return component.get("validationError")
    return None

@allure.feature("POST /v3/preapproved/personal-data/update-bdf-screen")
@allure.story("Валидация персональных данных")
@allure.title("Тест на валидацию Контактного телефона: brokerId = {broker_id}, biztalkId = {biztalk_id}")
@allure.description("Проверка срабатывания валидации на бэке для поля ContactPersonPhone.")
@pytest.mark.parametrize("phone, expected_error", [
    ("9611245", "Проверьте правильность ввода телефонного номера"),
    ("123", "Проверьте правильность ввода телефонного номера"),
    ("+381241123", "Проверьте правильность ввода телефонного номера"),
    ("", "Проверьте правильность ввода телефонного номера"),
])

def test_contact_person_phone_validation(phone, expected_error):
    url = f"{Config.BASE_URL_PREAPPROVED}/{VALID_BROKER_ID}/personal-data/update-bdf-screen/{VALID_BIZTALK_ID}"
    payload = request_body_phone(phone)

    with allure.step("Отправка запроса"):
        response = requests.post(url, json=payload, verify=False)

    with allure.step("Парсим JSON-ответ и валидируем его"):
        response_json = response.json()

    validation_error = extract_validation_error(response_json)
    with allure.step(f"Для поля ContactPersonPhone сработала валидация. ValidationError = {validation_error}"):
        assert validation_error == expected_error

    with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
        allure.attach(json.dumps(response_json, indent=4, ensure_ascii=False),
                      name="Response JSON",
                      attachment_type=allure.attachment_type.JSON)
