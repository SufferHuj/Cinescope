import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT


class TestAuthAPI:

    # проверка успешной регистрации
    def test_register_user(self, test_user):
        # URL для регистрации
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"

        # Отправка запроса на регистрацию
        response = requests.post(register_url, json= test_user, headers= HEADERS)

        # Логируем ответ для диагностики
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        # Проверки
        assert response.status_code == 201, "Ошибка регистрации пользователя"
        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"

        # Проверяем, что роль USER назначена по умолчанию
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    # проверка успешной авторизации
    def test_login_user(self, test_user):

        # url для логина
        login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"

        # отправка запрос на логин
        response = requests.post(login_url, json= test_user, headers= HEADERS)

        # логируем ответ для диагностики
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        # проверки
        assert response.status_code in (200, 201), "Ошибка авторизации"
        assert "accessToken" in response.json(), "Токен доступа отсутствует в ответе"
        assert "user" in response.json(), "Поле 'user' отсутствует в ответе"
        assert response.json()["user"]["email"] == test_user["email"], "Email в ответе не совпадает"


    # НЕГАТИВНЫЕ ПРОВЕРКИ

    # проверка авторизации с невалидным паролем
    @pytest.mark.negative
    def test_login_with_invalid_password(self, test_user):

        # url для логина
        login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"

        # неверный пароль
        login_data = {
            "email": test_user["email"],
            "password": "asD3_3_f"
        }

        response = requests.post(login_url, json= login_data, headers= HEADERS)

        assert response.status_code == 401, "Пароль должен быть невалидный"
        assert "error" in response.json(), "Сообщение об ошибке отсутствует в ответе"
        assert "Unauthorized" in response.json().get("error", ""), "Сообщение об ошибке некорректное"

    # проверка авторизации с несуществующим email
    @pytest.mark.negative
    def test_login_with_invalid_login(self, test_user):

        # url для логина
        login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"

        # неверный пароль
        login_data = {
            "email": "test@gmail.com",
            "password": test_user["password"]
        }

        response = requests.post(login_url, json= login_data, headers= HEADERS)

        assert response.status_code == 401, "Email должен быть невалидный"
        assert "error" in response.json(), "Сообщение об ошибке отсутствует в ответе"
        assert "Unauthorized" in response.json().get("error", ""), "Сообщение об ошибке некорректное"

    # проверка авторизации с пустым телом запроса
    @pytest.mark.negative
    def test_login_without_body(self, test_user):

        login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"

        # пустое тело
        login_data = {}

        response = requests.post(login_url, json=login_data, headers=HEADERS)

        assert response.status_code == 401, "Тело ответа должно быть пустым"
        assert "error" in response.json(), "Сообщение об ошибке отсутствует в ответе"
        assert "Unauthorized" in response.json().get("error", ""), "Сообщение об ошибке некорректное"