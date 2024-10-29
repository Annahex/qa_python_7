from ..urls.urls import CREATE_ORDER_URL
import requests
from faker import Faker
import pytest
import allure


class TestCreateOrder:

    colors = [
        [],
        ["BLACK"],
        ["GRAY"],
        ["BLACK", "GRAY"]
    ]

    @allure.title('Проверка создания заказа')
    @pytest.mark.parametrize('colors', colors)
    def test_can_create_order_without_color(self, colors):
        fake = Faker("ru_RU")
        payload = {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "address": fake.address(),
            "metroStation": 6,
            "phone": fake.phone_number(),
            "rentTime": 5,
            "deliveryDate": fake.date(),
            "comment": fake.text(),
            "colors": colors
        }

        response = requests.post(CREATE_ORDER_URL, data=payload)
        body = response.json()

        assert response.status_code == 201
        assert body["track"] > 0
