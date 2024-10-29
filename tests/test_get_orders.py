from ..urls.urls import GET_ORDER_URL
import requests
import allure


class TestGetOrder:

    @allure.title('Проверка получения списка заказов')
    def test_can_create_order_without_color(self):
        response = requests.get(GET_ORDER_URL)
        body = response.json()

        assert response.status_code == 200
        assert len(body["orders"]) >= 0
        assert body["pageInfo"]["page"] >= 0
        assert body["pageInfo"]["total"] >= 0
        assert body["pageInfo"]["limit"] >= 0
        assert len(body["availableStations"]) >= 0
