import json

import allure
import requests
import pytest
from config.config import Config
from enums.enum import StatusCode
from data.data_test import *

def jobs_init_bdf_screen(broker_id, biztalk_id, job_id):
    url = f"{Config.BASE_URL_PREAPPROVED}/{broker_id}/jobs/init-bdf-screen/{biztalk_id}?jobId={job_id}"
    response = requests.get(url, verify=False)
    return response

@allure.feature("GET /v3/preapproved/jobs/init-bdf-screen")
@allure.story("Инициализация BDUI для экрана работ в преапруве")
@allure.title("Тест инициализации BDUI для экрана работ: brokerId = {broker_id}, biztalkId = {biztalk_id}")
@allure.description("Проверка инициализации BDUI для экрана работ")
@pytest.mark.parametrize("broker_id, biztalk_id, expected_success, expected_status", [
    (VALID_BROKER_ID, VALID_BIZTALK_ID, True, StatusCode.OK.value),
    (INVALID_BROKER_ID, VALID_BIZTALK_ID, False, StatusCode.OK.value),
    (INVALID_BROKER_ID, INVALID_BIZTALK_ID, False, StatusCode.OK.value),
    (VALID_BROKER_ID, INVALID_BIZTALK_ID, False, StatusCode.OK.value),
])

def test_jobs_init_bdf_screen(broker_id, biztalk_id, expected_success, expected_status):
    with allure.step("Отправляем запрос"):
        response = jobs_init_bdf_screen(broker_id, biztalk_id, job_id)

    with allure.step(f"Статус-код. Ожидаемый {expected_status}, фактический {response.status_code}"):
        assert response.status_code == expected_status, f"Ожидался статус {expected_status}, но получен {response.status_code}"

    with allure.step("Парсим JSON-ответ"):
        data = response.json()

    with allure.step(f"Проверяем, что success = {expected_success}"):
        assert data ["success"] == expected_success

    with allure.step("Проверяем наличие и корректность ошибки"):
        if not expected_success:
            assert "error" in data
            assert data ["error"] == "Заявка не найдена"

    with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
        allure.attach(json.dumps(data, indent=4, ensure_ascii=False),
                      name="Response JSON",
                      attachment_type=allure.attachment_type.JSON)
