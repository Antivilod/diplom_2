import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import requests
from task3.data import ENDPOINT_REGISTER, ENDPOINT_LOGIN, ENDPOINT_USER, ENDPOINT_INGREDIENTS
from helpers import generate_user_data


@pytest.fixture
def user_data():
    """Фикстура, возвращающая данные нового пользователя."""
    return generate_user_data()


@pytest.fixture
def created_user(user_data):
    """
    Фикстура создаёт пользователя, возвращает его данные и токен.
    После теста пользователь удаляется.
    """
    # Регистрация пользователя
    response = requests.post(ENDPOINT_REGISTER, json=user_data)
    assert response.status_code == 200
    response_data = response.json()
    access_token = response_data.get("accessToken")

    # Возвращаем данные и токен
    yield {
        "user": user_data,
        "access_token": access_token
    }

    # Удаление пользователя после теста
    if access_token:
        headers = {"Authorization": access_token}
        requests.delete(ENDPOINT_USER, headers=headers)


@pytest.fixture
def auth_headers(created_user):
    """Фикстура возвращает заголовки с токеном авторизации."""
    access_token = created_user["access_token"]
    return {"Authorization": access_token}


@pytest.fixture
def ingredient_hashes():
    """Фикстура получает список актуальных хешей ингредиентов."""
    response = requests.get(ENDPOINT_INGREDIENTS)
    assert response.status_code == 200
    data = response.json()
    # Берём первые два ингредиента для тестов
    hashes = [ing["_id"] for ing in data["data"][:2]]
    return hashes