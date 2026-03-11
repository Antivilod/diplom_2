import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import requests
import allure
from task3.data import ENDPOINT_LOGIN, MSG_INVALID_CREDENTIALS

@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestLoginUser:
    # ... тесты

    @allure.title("Логин под существующим пользователем")
    @allure.description("Проверка успешной авторизации с корректными данными")
    def test_login_existing_user_success(self, created_user):
        user = created_user["user"]
        login_data = {
            "email": user["email"],
            "password": user["password"]
        }
        response = requests.post(ENDPOINT_LOGIN, json=login_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
        assert "accessToken" in response_data
        assert "refreshToken" in response_data
        assert response_data["user"]["email"] == user["email"]
        assert response_data["user"]["name"] == user["name"]

    @allure.title("Логин с неверным логином и паролем")
    @allure.description("Проверка ошибки при неверных учётных данных")
    @pytest.mark.parametrize("wrong_field", ["email", "password"])
    def test_login_invalid_credentials_failed(self, created_user, wrong_field):
        user = created_user["user"].copy()
        if wrong_field == "email":
            user["email"] = "wrong_email@example.com"
        else:
            user["password"] = "wrong_password"

        login_data = {
            "email": user["email"],
            "password": user["password"]
        }
        response = requests.post(ENDPOINT_LOGIN, json=login_data)

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == MSG_INVALID_CREDENTIALS