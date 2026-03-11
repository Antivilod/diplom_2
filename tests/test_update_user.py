
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import requests
import allure
from task3.data import ENDPOINT_USER, ENDPOINT_REGISTER, MSG_UNAUTHORIZED, MSG_EMAIL_EXISTS
from helpers import generate_random_string, generate_user_data

@allure.epic("Stellar Burgers API")
@allure.feature("Изменение данных пользователя")
class TestUpdateUser:

    @allure.title("Изменение данных пользователя с авторизацией")
    @allure.description("Проверка, что авторизованный пользователь может изменить любое поле")
    @pytest.mark.parametrize("field_to_update", ["email", "name"])
    def test_update_user_with_auth_success(self, auth_headers, created_user, field_to_update):
        user = created_user["user"]
        new_value = f"updated_{generate_random_string(8)}"
        if field_to_update == "email":
            new_value += "@yandex.ru"
            update_data = {"email": new_value}
        else:
            update_data = {"name": new_value}

        response = requests.patch(ENDPOINT_USER, headers=auth_headers, json=update_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
        assert response_data["user"][field_to_update] == new_value

    @allure.title("Изменение данных пользователя без авторизации")
    @allure.description("Проверка, что неавторизованный пользователь не может изменить данные")
    @pytest.mark.parametrize("field_to_update", ["email", "name"])
    def test_update_user_without_auth_failed(self, created_user, field_to_update):
        user = created_user["user"]
        new_value = f"updated_{generate_random_string(8)}"
        if field_to_update == "email":
            new_value += "@yandex.ru"
            update_data = {"email": new_value}
        else:
            update_data = {"name": new_value}

        response = requests.patch(ENDPOINT_USER, json=update_data)

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == MSG_UNAUTHORIZED

    @allure.title("Изменение email на уже существующий")
    @allure.description("Проверка, что нельзя установить email, который уже используется")
    def test_update_email_to_existing_failed(self, auth_headers, created_user, user_data):
        # Создаём второго пользователя
        second_user_data = generate_user_data()
        response = requests.post(ENDPOINT_REGISTER, json=second_user_data)
        assert response.status_code == 200

        # Пытаемся изменить email первого пользователя на email второго
        update_data = {"email": second_user_data["email"]}
        response = requests.patch(ENDPOINT_USER, headers=auth_headers, json=update_data)

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == MSG_EMAIL_EXISTS