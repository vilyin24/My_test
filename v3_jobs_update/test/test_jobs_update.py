import json

import allure
import pytest
import requests
from config.config import Config
from enums.enum import StatusCode
from v3_jobs_update.schemas.request_body import request_body
from v3_jobs_update.schemas.response_schema import ValidateResponseBody
from data.data_test import *


def jobs_init_bdf_screen(broker_id, biztalk_id, job_id):
    url = f"{Config.BASE_URL_PREAPPROVED}/{broker_id}/jobs/init-bdf-screen/{biztalk_id}?jobId={job_id}"

    with allure.step("Отправляем запрос GET /jobs-init-bdf-screen для получения данных о работе"):
        response = requests.get(url, verify=False)

    with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
        allure.attach(json.dumps(response.json(), indent=4, ensure_ascii=False),
                      name="Response GET /jobs-init-bdf-screen",
                      attachment_type=allure.attachment_type.JSON)
    return response


@allure.feature("POST /v3/preapproved/jobs/update")
@allure.story("Обновление работы")
@allure.title("Обновление работы: brokerId = {broker_id}, biztalkId = {biztalk_id}")
@allure.description("Тест проверяет создание работы с различными brokerId и biztalkId")
@pytest.mark.parametrize(
    "broker_id, biztalk_id, job_id, expected_success, expected_error",
    [
        (VALID_BROKER_ID, VALID_BIZTALK_ID, job_id, True, None),  # Валидный кейс
        (INVALID_BROKER_ID, VALID_BIZTALK_ID, job_id, False, "Заявка не найдена"),  # Невалидный brokerId
        (VALID_BROKER_ID, INVALID_BIZTALK_ID, job_id, False, "Заявка не найдена"),  # Невалидный biztalkId
        (INVALID_BROKER_ID, INVALID_BIZTALK_ID, job_id, False, "Заявка не найдена"),  # Невалидный brokerId и biztalkId
    ]
)
def test_jobs_update(broker_id, biztalk_id, job_id, expected_success, expected_error):
    jobs_init_bdf_screen(broker_id, biztalk_id, job_id)

    url = f"{Config.BASE_URL_PREAPPROVED}/{broker_id}/jobs/{job_id}/update/{biztalk_id}"

    with allure.step("Отправляем запрос на обновление данных по работе"):
        response = requests.post(url, json=request_body, verify=False)
        response.raise_for_status()

    with allure.step("Парсим JSON-ответ"):
        try:
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Ошибка запроса: {e}")
        except ValueError:
            pytest.fail("Ошибка декодирования JSON в ответе")

    with allure.step(f"Статус код. Ожидаемый: {StatusCode.OK.value}, фактический: {response.status_code}"):
        assert response.status_code == StatusCode.OK.value, (
            f"Ожидался статус код {StatusCode.OK.value}, но получен {response.status_code}"
        )

    if expected_success:
        try:
            with allure.step("Валидируем JSON-ответ по схеме"):
                ValidateResponseBody.validate_response(response_data)

            with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
                allure.attach(json.dumps(response_data, indent=4, ensure_ascii=False),
                              name="Response JSON",
                              attachment_type=allure.attachment_type.JSON)
        except Exception as e:
            pytest.fail(f"Ошибка валидации JSON-схемы: {e}")
    else:
        with allure.step("Проверяем, что success = false"):
            assert response_data.get(
                "success") is False, f"Ожидался success=false, но получен {response_data.get('success')}"

        with allure.step(f"Проверяем, что текст в поле error соответствует требованиям - {expected_error}"):
            assert response_data.get("error") == expected_error, (
                f"Ожидалась ошибка '{expected_error}', но получена '{response_data.get('error')}'"
            )

        with allure.step("Проверяем, что errorCode = 0"):
            assert response_data.get("errorCode") == 0, "Ожидался errorCode = 0"

        with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
            allure.attach(json.dumps(response_data, indent=4, ensure_ascii=False),
                          name="Response JSON",
                          attachment_type=allure.attachment_type.JSON)
