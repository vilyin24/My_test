import json

import allure
import pytest
import requests
from config.config import Config
from data.data_test import *
from v3_personal_data_update_bdf_screen.schemas_validation.schemas_registration_address import request_body_registration_address


def extract_validation_error(response_json):
    for group in response_json.get("result", {}).get("componentGroups", []):
        for component in group.get("components", []):
            if component.get("label") == "Адрес постоянной регистрации":
                return component.get("validationError")
    return None

@allure.feature("POST /v3/preapproved/personal-data/update-bdf-screen")
@allure.story("Валидация персональных данных")
@allure.title("Тест на валидацию Адреса регистрации: brokerId = {broker_id}, biztalkId = {biztalk_id}")
@allure.description("Проверка срабатывания валидации на бэке для поля RegistrationAddress")
@pytest.mark.parametrize("registrationAddress, expected_error", [
    ("г Казань, ул Татарстан", "Проверьте правильность введенного адреса"),
    ("ул Татарстан", "Проверьте правильность введенного адреса"),
    # ("", "Проверьте правильность введенного адреса"),
])

def test_registration_address_validation(registrationAddress, expected_error):
    url = f"{Config.BASE_URL_PREAPPROVED}/{VALID_BROKER_ID}/personal-data/update-bdf-screen/{VALID_BIZTALK_ID}"
    payload = request_body_registration_address(registrationAddress)

    with allure.step("Отправка запроса"):
        response = requests.post(url, json=payload, verify=False)

    with allure.step("Парсим JSON-ответ и валидируем его"):
        response_json = response.json()

    validation_error = extract_validation_error(response_json)

    with allure.step(f"Для поля RegistrationAddress сработала валидация. ValidationError = {validation_error}"):
        assert validation_error == expected_error

    with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
        allure.attach(json.dumps(response_json, indent=4, ensure_ascii=False),
                      name="Response JSON",
                      attachment_type=allure.attachment_type.JSON)