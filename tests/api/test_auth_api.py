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

        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

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
        проверка авторизации с несуществующим email
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
        проверка авторизации с пустым телом запроса
        """

        login_data = {}

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        assert "error" in response_data, "Сообщение об ошибке отсутствует в ответе"
        assert "Unauthorized" in response_data.get("error", ""), "Сообщение об ошибке некорректное"

class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert response_by_id.get('roles', []) == creation_user_data['roles']
        assert response_by_id.get('verified') is True