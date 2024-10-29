from ..urls.urls import CREATE_COURIER_URL, LOGIN_COURIER_URL, DELETE_COURIER_URL
from faker import Faker
import requests
import allure

MESSAGE_SAME_LOGIN = "Этот логин уже используется. Попробуйте другой."
MESSAGE_NOT_ENOUGH_DATA = "Недостаточно данных для создания учетной записи"


class TestCreateCourier:

    @allure.title('Проверка успешного создания курьера')
    def test_can_create_new_courier(self):
        fake = Faker("ru_RU")
        payload = {
            "login": fake.user_name(),
            "password": fake.password(),
            "firstName": fake.first_name()
        }

        response = requests.post(CREATE_COURIER_URL, data=payload)
        body = response.json()

        assert response.status_code == 201
        assert body["ok"] is True

        response = requests.post(LOGIN_COURIER_URL, data=payload)
        body = response.json()
        requests.delete(f"{DELETE_COURIER_URL}/{body['id']}", data=payload)

    @allure.title('Проверка неуспешного создания курьера - курьер с таким логином существует')
    def test_cant_create_two_couriers_with_same_login(self):
        fake = Faker("ru_RU")
        user_name = fake.user_name()
        payload = {
            "login": user_name,
            "password": fake.password(),
            "firstName": fake.first_name()
        }

        requests.post(CREATE_COURIER_URL, data=payload)
        response = requests.post(CREATE_COURIER_URL, data=payload)
        body = response.json()

        assert response.status_code == 409
        assert body["message"] == MESSAGE_SAME_LOGIN

    @allure.title('Проверка неуспешного создания курьера с неполными данными - отсутствует логин')
    def test_cant_create_courier_without_login(self):
        fake = Faker("ru_RU")
        payload = {
            "password": fake.password(),
            "firstName": fake.first_name()
        }

        requests.post(CREATE_COURIER_URL, data=payload)
        response = requests.post(CREATE_COURIER_URL, data=payload)
        body = response.json()

        assert response.status_code == 400
        assert body["message"] == MESSAGE_NOT_ENOUGH_DATA

    @allure.title('Проверка неуспешного создания курьера с неполными данными - отсутствует пароль')
    def test_cant_create_courier_without_password(self):
        fake = Faker("ru_RU")
        payload = {
            "login": fake.user_name(),
            "firstName": fake.first_name()
        }

        requests.post(CREATE_COURIER_URL, data=payload)
        response = requests.post(CREATE_COURIER_URL, data=payload)
        body = response.json()

        assert response.status_code == 400
        assert body["message"] == MESSAGE_NOT_ENOUGH_DATA
