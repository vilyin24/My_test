import json

import pytest
import requests
import allure
from config.config import Config
from enums.enum import StatusCode
from v3_personal_data_update_bdf_screen.schemas.request_body import request_body
from v3_personal_data_update_bdf_screen.schemas.response_schema import ValidateResponseBody
from data.data_test import *


@allure.feature("POST /v3/preapproved/personal-data/update-bdf-screen")
@allure.story("Обновление персональных данных")
@allure.title("Тест обновления персональных данных: brokerId = {broker_id}, biztalkId = {biztalk_id}")
@allure.description("Проверка успешности обновления персональных данных с разными brokerId и biztalkId.")
@pytest.mark.parametrize(
    "broker_id, biztalk_id, expected_success, expected_error",
    [
        (VALID_BROKER_ID, VALID_BIZTALK_ID, True, None),  # Валидный кейс
        (INVALID_BROKER_ID, VALID_BIZTALK_ID, False, "Не удалось записать клиентские данные"),  # Невалидный brokerId
        (VALID_BROKER_ID, INVALID_BIZTALK_ID, False, "Не удалось записать клиентские данные"),  # Невалидный biztalkId
        (INVALID_BROKER_ID, INVALID_BIZTALK_ID, False, "Не удалось записать клиентские данные"), # Невалидный brokerId и biztalkId
    ]
)

def test_personal_data_update_bdf_screen(broker_id, biztalk_id, expected_success, expected_error):
    url = f"{Config.BASE_URL_PREAPPROVED}/{broker_id}/personal-data/update-bdf-screen/{biztalk_id}"

    with allure.step("Отправка запроса"):
        try:
            response = requests.post(url, json=request_body, verify=False)
            response.raise_for_status()
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Ошибка запроса: {e}")
        except ValueError:
            pytest.fail("Ошибка декодирования JSON в ответе")

    with allure.step(f"Статус-код. Ожидаемый: {StatusCode.OK.value}, фактический: {response.status_code}"):
        assert response.status_code == StatusCode.OK.value, (
            f"Ожидался статус код {StatusCode.OK.value}, но получен {response.status_code}"
        )

    with allure.step("Парсим JSON-ответ и валидируем его"):
        if expected_success:
            try:
                with allure.step("Для успешного кейса проверяем stepType = 3"):
                    ValidateResponseBody.validate_response(response_data)
            except Exception as e:
                pytest.fail(f"Ошибка валидации JSON-схемы: {e}")
        else:
            with allure.step("Проверяем, что для негативного кейса вернулся success = false"):
                assert response_data.get(
                    "success") is False, f"Ожидался success = false, но получен {response_data.get('success')}"
            with allure.step(f"Проверяем, что текст в поле error соответствует требованиям - {expected_error}"):
                assert response_data.get("error") == expected_error, (
                    f"Ожидалась ошибка '{expected_error}', но получена '{response_data.get('error')}'"
                )

        with allure.step("Значение errorCode = 0"):
            assert response_data.get("errorCode") == 0, "Ожидался errorCode = 0"

        with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
            allure.attach(json.dumps(response_data, indent=4, ensure_ascii=False),
                          name="Response JSON",
                          attachment_type=allure.attachment_type.JSON)

