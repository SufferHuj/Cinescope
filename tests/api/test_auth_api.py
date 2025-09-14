import pytest
from api.api_manager import ApiManager
from models.auth_model import RegisterUserResponse, LoginUserResponse, ErrorResponse
from utils.data_generator import DataGenerator


class TestAuthAPI:

    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию пользователя.
        """

        response = api_manager.auth_api.register_user(test_user)
        response_data = RegisterUserResponse(**response.json())

        assert response_data.email == test_user.email, "Email не совпадает"
        assert response_data.fullName == test_user.fullName, "Имя не совпадает"
        assert response_data.roles == test_user.roles, "Роли не совпадают"
        assert response_data.verified is not None, "Статус верификации отсутствует в ответе"
        assert response_data.createdAt is not None, "Дата создания пользователя отсутствует в ответе"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """

        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=201)
        response_data = LoginUserResponse(**response.json())

        assert response.status_code == 201
        assert response_data.user.email == registered_user["email"], "Email не совпадает"
        assert response_data.user.fullName == registered_user["fullName"], "Имя не совпадает"
        assert response_data.user.roles == registered_user["roles"], "Роли не совпадают"
        assert response_data.accessToken is not None, "Токен доступа отсутствует в ответе"
        assert response_data.refreshToken is not None, "Токен обновления отсутствует в ответе"

    # НЕГАТИВНЫЕ ПРОВЕРКИ

    @pytest.mark.negative
    def test_login_with_invalid_password(self, api_manager: ApiManager, registered_user):
        """
        Проверка авторизации с невалидным паролем.
        """

        login_data = {
            "email": registered_user["email"],
            "password": DataGenerator.generation_random_password()
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        error_data = ErrorResponse(**response.json())

        assert response.status_code == 401
        assert error_data.error is not None, "Сообщение об ошибке отсутствует в ответе"
        assert "Unauthorized" in error_data.error, "Сообщение об ошибке некорректное"

    @pytest.mark.negative
    def test_login_with_invalid_login(self, api_manager: ApiManager, registered_user):
        """
        Проверка авторизации с несуществующим email
        """

        login_data = {
            "email": DataGenerator.generation_random_email(),
            "password": registered_user["password"]
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        error_data = ErrorResponse(**response.json())

        assert response.status_code == 401
        assert error_data.error is not None, "Сообщение об ошибке отсутствует в ответе"
        assert "Unauthorized" in error_data.error, "Сообщение об ошибке некорректное"

    @pytest.mark.negative
    def test_login_without_body(self, api_manager: ApiManager, registered_user):
        """
        Проверка авторизации с пустым телом запроса
        """

        login_data = {}

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        error_data = ErrorResponse(**response.json())

        assert response.status_code == 401
        assert error_data.error is not None, "Сообщение об ошибке отсутствует в ответе"
        assert "Unauthorized" in error_data.error, "Сообщение об ошибке некорректное"
