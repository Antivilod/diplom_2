import allure
import requests
from task3.data import ENDPOINT_ORDERS, MSG_UNAUTHORIZED


@allure.epic("Stellar Burgers API")
@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    @allure.description("Проверка, что авторизованный пользователь может получить список своих заказов")
    def test_get_orders_with_auth_success(self, auth_headers, ingredient_hashes):
        # Сначала создадим заказ, чтобы у пользователя точно были заказы
        order_data = {"ingredients": ingredient_hashes}
        create_response = requests.post(ENDPOINT_ORDERS, headers=auth_headers, json=order_data)
        assert create_response.status_code == 200

        # Получаем заказы пользователя
        response = requests.get(ENDPOINT_ORDERS, headers=auth_headers)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
        assert "orders" in response_data
        assert isinstance(response_data["orders"], list)
        assert len(response_data["orders"]) > 0

    @allure.title("Получение заказов неавторизованного пользователя")
    @allure.description("Проверка ошибки при попытке получить заказы без авторизации")
    def test_get_orders_without_auth_failed(self):
        response = requests.get(ENDPOINT_ORDERS)

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == MSG_UNAUTHORIZED