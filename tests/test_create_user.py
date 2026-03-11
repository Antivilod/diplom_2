import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import requests
import allure
from task3.data import ENDPOINT_REGISTER, MSG_USER_EXISTS, MSG_REQUIRED_FIELDS


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, user_data):
        response = requests.post(ENDPOINT_REGISTER, json=user_data)
        assert response.status_code == 200
        # ... остальные проверки

    @allure.title("Создание пользователя, который уже существует")
    def test_create_existing_user_failed(self, created_user):
        user = created_user["user"]
        response = requests.post(ENDPOINT_REGISTER, json=user)
        assert response.status_code == 403
        assert response.json()["message"] == MSG_USER_EXISTS

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_failed(self, user_data, missing_field):
        del user_data[missing_field]
        response = requests.post(ENDPOINT_REGISTER, json=user_data)
        assert response.status_code == 403
        assert response.json()["message"] == MSG_REQUIRED_FIELDS