import pytest
from api.api_manager import ApiManager


class TestAuthAPI:

    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """

        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=[200, 201])
        response_data = response.json()

        assert response.status_code in [200, 201]
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    # НЕГАТИВНЫЕ ПРОВЕРКИ

    @pytest.mark.negative
    def test_login_with_invalid_password(self, api_manager: ApiManager, registered_user):
        """
        Проверка авторизации с невалидным паролем.
        """

        login_data = {
            "email": registered_user["email"],
            "password": "WrongPassword123!"
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        assert "error" in response_data, "Сообщение об ошибке отсутствует в ответе"
        assert "Unauthorized" in response_data.get("error", ""), "Сообщение об ошибке некорректное"

    @pytest.mark.negative
    def test_login_with_invalid_login(self, api_manager: ApiManager, registered_user):
        """
        Проверка авторизации с несуществующим email
        """

        login_data = {
            "email": "test@gmail.com",
            "password": registered_user["password"]
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        assert "error" in response_data, "Сообщение об ошибке отсутствует в ответе"
        assert "Unauthorized" in response_data.get("error", ""), "Сообщение об ошибке некорректное"

    @pytest.mark.negative
    def test_login_without_body(self, api_manager: ApiManager, registered_user):
        """
        Проверка авторизации с пустым телом запроса
        """

        login_data = {}

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        assert "error" in response_data, "Сообщение об ошибке отсутствует в ответе"
        assert "Unauthorized" in response_data.get("error", ""), "Сообщение об ошибке некорректное"
