import json

import pytest
import requests
import allure
from config.config import Config
from enums.enum import StatusCode
from v3_personal_data_update_init_bdf_screen.schemas.request_body import request_body
from v3_personal_data_update_init_bdf_screen.schemas.response_schema import ValidateResponseBody
from data.data_test import *


@allure.feature("Отправляем POST banners/{BIZTALK}/{BROKER}/hide")
@allure.title("Скрытие баннера")
@allure.description("Скрытие баннера запрос /banners/{}/{}/hide")
@pytest.mark.parametrize("broker_id, biztalk_id, expected_status", [
    (VALID_BROKER_ID_BANNERS, VALID_BIZTALK_ID_BANNERS, StatusCode.OK.value),
    (INVALID_BROKER_ID, VALID_BIZTALK_ID_BANNERS, StatusCode.OK.value),
    (INVALID_BROKER_ID, INVALID_BIZTALK_ID, StatusCode.OK.value),
    (VALID_BROKER_ID_BANNERS, INVALID_BIZTALK_ID, StatusCode.OK.value),
])
def test_personal_data_update(broker_id, biztalk_id, expected_status):
    # Используем Config.BASE_URL для построения полного URL
    url = f"{Config.BASE_URL_BANNERS}/{biztalk_id}/{broker_id}/hide"

    with allure.step("Отправляем POST-запрос "):
        response = requests.post(url, verify=False)

    with allure.step(f"Проверяем статус-код: ожидаемый {StatusCode.OK.value}, фактический {response.status_code}"):
        assert response.status_code == StatusCode.OK.value, f"Ожидался статус код {StatusCode.OK}, но получен {response.status_code}"

    with allure.step("Парсим JSON-ответ и валидируем его по схеме"):
        response_data = response.json()
        ValidateResponseBody.validate_response(response_data)

    with allure.step("Выводим тело ответа в консоль"):
        try:
            response_text = response.text
            print("Response body: ", response.json())

            with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
                allure.attach(json.dumps(response_text, indent=4, ensure_ascii=False),
                              name="Response JSON",
                              attachment_type=allure.attachment_type.JSON)
        except ValueError:
            print("Не удалось распарсить ответ как JSON. Ответ: ", response.text)
            with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
                allure.attach(json.dumps(response.text, indent=4, ensure_ascii=False),
                              name="Response JSON",
                              attachment_type=allure.attachment_type.JSON)
