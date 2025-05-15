import json

import allure
import requests
import pytest
from config.config import Config
from enums.enum import StatusCode
from data.data_test import *

# Только для валидного кейса!!!
with allure.step("Отправляем запрос GET /jobs для получения списка работ"):
    def get_jobs(broker_id, biztalk_id):
        url = f"{Config.BASE_URL_PREAPPROVED}/{broker_id}/jobs/{biztalk_id}"
        response = requests.get(url, verify=False)
        response.raise_for_status()

        with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
            allure.attach(json.dumps(response.json(), indent=4, ensure_ascii=False),
                          name="Response JSON",
                          attachment_type=allure.attachment_type.JSON)
        return response

# Получаем последний job_id перед удалением
@pytest.fixture(scope="module")
def job_id_delete():
    response = get_jobs(VALID_BROKER_ID, VALID_BIZTALK_ID)
    jobs = response.json().get("result", {}).get("jobs", [])

    if not jobs:
        allure.attach(f"Список работ пуст. По brokerId {VALID_BROKER_ID} нет работ для удаления.",
                      name="Job list empty",
                      attachment_type=allure.attachment_type.TEXT)
        # print(f"Список работ пуст. По brokerId {VALID_BROKER_ID} нет работ для удаления.")
        return None

    return jobs[-1]["id"]

@allure.feature("DELETE /v3/preapproved/jobs/{jobId}/delete")
@allure.story("Удаление работы")
@allure.title("Удаление работы: brokerId = {broker_id}, jobId = {job_id_delete}")
@allure.description("Тест проверяет удаление записи о работе с различными brokerId")
@pytest.mark.parametrize("broker_id, expected_status, expected_error", [
    (VALID_BROKER_ID, StatusCode.OK.value, None),
    (INVALID_BROKER_ID, StatusCode.OK.value, "Работа не найдена"),
])

def test_delete_job(broker_id, expected_status, expected_error, job_id_delete):

    if not job_id_delete:
        allure.attach("job_id пуст, тест пропущен", name="Test Skipped", attachment_type=allure.attachment_type.TEXT)
        pytest.skip(" job_id пуст, тест пропущен")

    url = f"{Config.BASE_URL_PREAPPROVED}/{broker_id}/jobs/{job_id_delete}/delete"

    with allure.step("Отправляем запрос DELETE"):
        response = requests.delete(url, verify=False)

    with allure.step(f"Статус код. Ожидаемый: {expected_status}, фактический: {response.status_code}"):
        assert response.status_code == expected_status

    with allure.step("Парсим JSON-ответ"):
        data = response.json()

    if expected_error is None:
        with allure.step("Проверяем, что success = true"):
            assert data["success"] is True

        with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
            allure.attach(json.dumps(data, indent=4, ensure_ascii=False),
                          name="Response JSON",
                          attachment_type=allure.attachment_type.JSON)
    else:
        with allure.step("Проверяем, что success = false и есть поле error"):
            assert "error" in data
            assert data["success"] is False

        with allure.step(f"Проверяем текст ошибки: ожидаемый '{expected_error}', фактический '{data.get('error')}'"):
            assert data["error"] == expected_error, (
                f"Ожидалась ошибка '{expected_error}', но получена '{data.get('error')}'"
            )

        with allure.step("Прикрепляем JSON-ответ в Allure-отчёт"):
            allure.attach(json.dumps(data, indent=4, ensure_ascii=False),
                          name="Response JSON",
                          attachment_type=allure.attachment_type.JSON)