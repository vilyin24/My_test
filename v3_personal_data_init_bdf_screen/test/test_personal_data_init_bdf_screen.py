import json

import pytest
import requests
import allure
from config.config import Config
from enums.enum import StatusCode
from data.data_test import *

@allure.step("Отправка GET-запроса для получения персональных данных пользователя с brokerId = {broker_id} и biztalkId = {biztalk_id}")
def get_personal_data_init_bdf_screen(broker_id, biztalk_id):
    url = f"{Config.BASE_URL_PREAPPROVED}/{broker_id}/personal-data/init-bdf-screen/{biztalk_id}"
    response = requests.get(url, verify=False)
    return response

@allure.feature("GET /v3/preapproved/personal-data/init-bdf-screen")
@allure.story("Получение персональных данных")
@allure.title("Тест персональных данных: brokerId={broker_id}, biztalkId={biztalk_id}")
@allure.description("Проверка получения персональных данных пользователя с различными brokerId и biztalkId.")
@pytest.mark.parametrize("broker_id, biztalk_id, expected_success, expected_status", [
    (VALID_BROKER_ID, VALID_BIZTALK_ID, True, StatusCode.OK.value),
    (INVALID_BROKER_ID, VALID_BIZTALK_ID, False, StatusCode.OK.value),
    (INVALID_BROKER_ID, INVALID_BIZTALK_ID, False, StatusCode.OK.value),
    (VALID_BROKER_ID, INVALID_BIZTALK_ID, False, StatusCode.OK.value),
])

def test_personal_data_init_bdf_screen(broker_id, biztalk_id, expected_success, expected_status):

    with allure.step("Отправляем запрос"):
        response = get_personal_data_init_bdf_screen(broker_id, biztalk_id)

    with allure.step(f"Статус-код. Ожидаемый: {expected_status}, фактический: {response.status_code}"):
        assert response.status_code == expected_status

    with allure.step("Парсим JSON-ответ"):
        data = response.json()

    with allure.step(f"Проверяем success. Ожидаемый: {expected_success}, фактический: {data['success']}"):
        assert data["success"] == expected_success

    with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
        allure.attach(json.dumps(data, indent=4, ensure_ascii=False),
                      name="Response JSON",
                      attachment_type=allure.attachment_type.JSON)

    if not expected_success:
        with allure.step("Проверяем наличие поля 'error' в респонсе"):
            assert "error" in data, "Ожидали поле 'error', но его нет в ответе"

        if broker_id == VALID_BROKER_ID and biztalk_id == INVALID_BIZTALK_ID:
            with allure.step(
                    f"Проверяем текст ошибки для некорректного biztalkId. Ожидаемый: 'Заявка brokerId {broker_id}. Некорректный идентификатор пользователя'"):
                assert data["error"] == f"Заявка brokerId {broker_id}. Некорректный идентификатор пользователя", \
                    f"Ожидали 'Заявка brokerId {broker_id}. Некорректный идентификатор пользователя', получили '{data['error']}'"
        else:
            with allure.step(
                    f"Проверяем текст ошибки для несуществующего brokerId. Ожидаемый: 'Заявка brokerId {broker_id} не найдена'"):
                assert data["error"] == f"Заявка brokerId {broker_id} не найдена", \
                    f"Ожидали 'Заявка brokerId {broker_id} не найдена', получили '{data['error']}'"