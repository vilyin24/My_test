import json

import pytest
import requests
import allure
from config.config import Config
from enums.enum import StatusCode
from v3_personal_data_update_init_bdf_screen.schemas.request_body import request_body
from v3_personal_data_update_init_bdf_screen.schemas.response_schema import ValidateResponseBody
from data.data_test import VALID_BROKER_ID

@allure.feature("POST /v3/preapproved/personal-data/update-init-bdf-screen")
@allure.story("Обновление персональных данных")
@allure.title("Обновление персональных данных: проверка скрытия адреса проживания")
@allure.description("Проверка, что после обновления данных поле 'Адрес проживания' скрыто (hidden=true)")
def test_personal_data_update():
    # Используем Config.BASE_URL для построения полного URL
    url = f"{Config.BASE_URL_PREAPPROVED}/{VALID_BROKER_ID}/personal-data/update-init-bdf-screen"

    with allure.step("Отправляем POST-запрос на обновление персональных данных"):
        response = requests.post(url, json=request_body, verify=False)

    with allure.step(f"Проверяем статус-код: ожидаемый {StatusCode.OK.value}, фактический {response.status_code}"):
        assert response.status_code == StatusCode.OK.value, f"Ожидался статус код {StatusCode.OK}, но получен {response.status_code}"

    with allure.step("Парсим JSON-ответ и валидируем его по схеме"):
        response_data = response.json()
        ValidateResponseBody.validate_response(response_data)

    with allure.step("Проверяем, что компонент 'Адрес проживания' скрыт"):
        actual_address_component = next(
            (component for component in response_data['result']['componentGroups'][0]['components']
            if component['label'] == "Адрес проживания"), None
        )
    assert actual_address_component is not None, "Компонент 'Адрес проживания' не найден"
    assert actual_address_component["hidden"], "Поле 'Адрес проживания' должно быть скрыто"

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
