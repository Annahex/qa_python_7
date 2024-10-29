import requests
import pytest
from faker import Faker
from .urls.urls import CREATE_COURIER_URL, DELETE_COURIER_URL, LOGIN_COURIER_URL


@pytest.fixture()
def login_and_password():
    fake = Faker("ru_RU")
    login = fake.user_name()
    password = fake.password()
    payload = {
        "login": login,
        "password": password,
        "firstName": fake.first_name()
    }
    requests.post(CREATE_COURIER_URL, data=payload)
    yield login, password
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(LOGIN_COURIER_URL, data=payload)
    body = response.json()
    requests.delete(f"{DELETE_COURIER_URL}/{body['id']}", data=payload)
