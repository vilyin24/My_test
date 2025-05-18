import json

import requests
import pytest
import allure
from config.config import  Config

from enums.enum import StatusCode
from data.data_test import *

@allure.step("GET statuses_v2")
def get_programs(biztalk_id):
    url = f"{Config.BASE_URL_BROKER}/{biztalk_id}/statuses/v2"
    response = requests.get(url, verify=False)
    return response

@allure.feature("GET statuses_v2")
@allure.title("Информация о баннерах")
@allure.description("GET statuses_v2")
@pytest.mark.parametrize("biztalk_id, expected_success, expected_status", [
    (VALID_BIZTALK_ID, True, StatusCode.OK.value),
    (VALID_BIZTALK_ID_BANNERS, True, StatusCode.OK.value),
    (INVALID_BIZTALK_ID, False, StatusCode.OK.value),
])

def test_get_jobs(biztalk_id, expected_success, expected_status):

    with allure.step("Отправляем запрос"):
        response = get_programs(biztalk_id)

    with allure.step(f"Статус-код. Ожидаемый: {expected_status}, фактический: {response.status_code}"):
        assert response.status_code == expected_status, f"Ожидали {expected_status}, но получили {response.status_code}"

    with allure.step("Парсим JSON-ответ"):
        data = response.json()

    with allure.step("Проверяем success в респонсе"):
        assert data["success"] == expected_success, f"Ожидали success = {expected_success}, но получили {data['success']}"

    with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
        allure.attach(json.dumps(data, indent=4, ensure_ascii=False),
                        name="Response JSON",
                        attachment_type=allure.attachment_type.JSON)

    if not expected_success:
        with allure.step("Проверяем сообщение об ошибке"):
            assert "error" in data, "В респонсе отсутствует поле 'error'"
            assert data["error"] == {data['error']}
