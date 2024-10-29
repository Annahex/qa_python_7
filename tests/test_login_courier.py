from ..urls.urls import LOGIN_COURIER_URL
import requests
import allure

MESSAGE_NOT_FOUND = "Учетная запись не найдена"
MESSAGE_NOT_ENOUGH_DATA = "Недостаточно данных для входа"


class TestLoginCourier:

    @allure.title('Проверка успешного логина для существующего курьера')
    def test_courier_can_login(self, login_and_password):
        (login, password) = login_and_password
        payload = {
            "login": login,
            "password": password
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)
        body = response.json()

        assert response.status_code == 200
        assert body["id"] > 0

    @allure.title('Проверка неуспешного логина для существующего курьера - неверный логин')
    def test_courier_cant_login_with_wrong_login(self, login_and_password):
        (login, password) = login_and_password
        payload = {
            "login": login + '123',
            "password": password
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)
        body = response.json()

        assert response.status_code == 404
        assert body["message"] == MESSAGE_NOT_FOUND

    @allure.title('Проверка неуспешного логина для существующего курьера - неверный пароль')
    def test_courier_cant_login_with_wrong_password(self, login_and_password):
        (login, password) = login_and_password
        payload = {
            "login": login,
            "password": password + '123'
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)
        body = response.json()

        assert response.status_code == 404
        assert body["message"] == MESSAGE_NOT_FOUND

    @allure.title('Проверка неуспешного логина для неполных данных - отсутсвует логин')
    def test_courier_cant_login_without_login(self, login_and_password):
        (_, password) = login_and_password
        payload = {
            "password": password
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)
        body = response.json()

        assert response.status_code == 400
        assert body["message"] == MESSAGE_NOT_ENOUGH_DATA

    @allure.title('Проверка неуспешного логина для неполных данных - отсутсвует пароль')
    def test_courier_cant_login_without_password(self, login_and_password):
        (login, _) = login_and_password
        payload = {
            "login": login
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)
        body = response.json()

        assert response.status_code == 400
        assert body["message"] == MESSAGE_NOT_ENOUGH_DATA
