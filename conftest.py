import pytest
import requests
import random

from api.api_manager import ApiManager
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT, MOVIES_API_BASE_URL
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from entities.user import User
from resources.user_creds import SuperAdminCreds


@pytest.fixture(scope='function')
def test_user():

    """
    Генерация случайного пользователя для тестов.
    """

    random_email = DataGenerator.generation_random_email()
    random_name = DataGenerator.generation_random_name()
    random_password = DataGenerator.generation_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):

    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    Обеспечивает очистку созданного пользователя после завершения теста.
    """

    response = api_manager.auth_api.register_user(user_data=test_user, expected_status=201)
    response_data = response.json()

    # Обновлён test_user данными из ответа, особенно ID
    created_user = test_user.copy()
    created_user["id"] = response_data["id"]

    # Сохранён пароль, так как он не возвращается в ответе регистрации, но нужен для логина
    created_user["password_plain"] = test_user["password"]

    yield created_user

    try:
        api_manager.user_api.clean_up_user(user_id=created_user["id"])
    except Exception as e:
        print(f"Could not clean up user {created_user.get('id')}: {e}")

@pytest.fixture(scope="session")
def requester():

    """
    Фикстура для создания экземпляра CustomRequester.
    """

    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def session():

    """
    Фикстура для создания HTTP-сессии.
    """

    http_session = requests.Session()

    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):

    """
    Фикстура для создания экземпляра ApiManager.
    """

    return ApiManager(session)

# ФИКСТУРЫ ДЛЯ ТЕСТОВ MoviesAPI

@pytest.fixture()
def user_session():

    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session()

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):

    new_session = user_session

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        ["SUPER_ADMIN"],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data