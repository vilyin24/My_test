import json

import requests
import pytest
import allure
from config.config import Config
from enums.enum import StatusCode
from data.data_test import *


@allure.step("Отправка GET-запроса для получения параметров заявки с brokerId = {broker_id} и biztalkId = {biztalk_id}")
def get_preapproved_parameters(broker_id, biztalk_id):
    url = f"{Config.BASE_URL_CREDIT}/{broker_id}/parameters/{biztalk_id}"
    response = requests.get(url, verify=False)
    return response


@allure.feature("GET /v3/preapproved/parameters")
@allure.story("Получение параметров заявки")
@allure.title("Тест параметров заявки: brokerId = {broker_id}, biztalkId = {biztalk_id}")
@allure.description("Проверка получения параметров заявки с различными brokerId и biztalkId")
@pytest.mark.parametrize("broker_id, biztalk_id, expected_success, expected_status", [
    (VALID_BROKER_ID, VALID_BIZTALK_ID, True, StatusCode.OK.value),
    (INVALID_BROKER_ID, VALID_BIZTALK_ID, False, StatusCode.OK.value),
    (INVALID_BROKER_ID, INVALID_BIZTALK_ID, False, StatusCode.OK.value),
    (VALID_BROKER_ID, INVALID_BIZTALK_ID, False, StatusCode.OK.value),
])
def test_preapproved_parameters(broker_id, biztalk_id, expected_success, expected_status):
    with allure.step("Отправляем запрос"):
        response = get_preapproved_parameters(broker_id, biztalk_id)

    with allure.step(f"Cтатус код. Ожидаемый: {expected_status}, фактический: {response.status_code}"):
        assert response.status_code == expected_status, f"Ожидали {expected_status}, но получили {response.status_code}"

    with allure.step("Парсим JSON-ответ"):
        data = response.json()

    with allure.step(f"Проверяем success. Ожидаемый: {expected_success}, фактический: {data['success']}"):
        assert data["success"] == expected_success, f"Ожидали {expected_success}, получили {data['success']}"

    with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
        allure.attach(json.dumps(data, indent=4, ensure_ascii=False),
                      name="Response JSON",
                      attachment_type=allure.attachment_type.JSON)

    if not expected_success:
        with allure.step("Проверяем, что присутствует ошибка и её текст корректен"):
            assert "error" in data
            assert data["error"] == "Не удалось обработать данные из кредитной заявки"
