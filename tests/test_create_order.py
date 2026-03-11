import allure
import requests
from task3.data import ENDPOINT_ORDERS, MSG_NO_INGREDIENTS
from helpers import generate_invalid_ingredient_hash


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.description("Проверка успешного создания заказа авторизованным пользователем")
    def test_create_order_with_auth_and_ingredients_success(self, auth_headers, ingredient_hashes):
        order_data = {"ingredients": ingredient_hashes}
        response = requests.post(ENDPOINT_ORDERS, headers=auth_headers, json=order_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
        assert "name" in response_data
        assert "order" in response_data
        assert "number" in response_data["order"]

    @allure.title("Создание заказа без авторизации")
    @allure.description("Проверка, что неавторизованный пользователь может создать заказ")
    def test_create_order_without_auth_success(self, ingredient_hashes):
        order_data = {"ingredients": ingredient_hashes}
        response = requests.post(ENDPOINT_ORDERS, json=order_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Проверка ошибки при попытке создать заказ без ингредиентов")
    def test_create_order_without_ingredients_failed(self, auth_headers):
        order_data = {"ingredients": []}
        response = requests.post(ENDPOINT_ORDERS, headers=auth_headers, json=order_data)

        assert response.status_code == 400
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == MSG_NO_INGREDIENTS

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.description("Проверка ошибки при передаче невалидного хеша")
    def test_create_order_with_invalid_hash_failed(self, auth_headers):
        invalid_hash = generate_invalid_ingredient_hash()
        order_data = {"ingredients": [invalid_hash]}
        response = requests.post(ENDPOINT_ORDERS, headers=auth_headers, json=order_data)

        assert response.status_code == 500

    @allure.title("Создание заказа с ингредиентами без авторизации")
    @allure.description("Проверка, что неавторизованный пользователь может создать заказ с ингредиентами")
    def test_create_order_with_ingredients_without_auth_success(self, ingredient_hashes):
        order_data = {"ingredients": ingredient_hashes}
        response = requests.post(ENDPOINT_ORDERS, json=order_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True