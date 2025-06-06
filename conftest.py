import pytest
import requests
import random

from api.api_manager import ApiManager
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT, MOVIES_API_BASE_URL
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from utils.data_generator import faker as global_faker


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

@pytest.fixture(scope='session')
def super_admin_data():

    """
    Данные для создания/логина супер-администратора.
    """

    email = 'api1@gmail.com'
    password = 'asdqwe123Q'

    return {
        "email": email,
        "fullName": "Admin",
        "password": password,
        "passwordRepeat": password,
        "roles": ["SUPER_ADMIN"]
    }

@pytest.fixture(scope="session")
def super_admin_token(api_manager_session_scope, super_admin_data): # Используки session-scoped ApiManager

    """
    Фикстура для получения токена супер-администратора.
    Регистрирует и/или логинит супер-администратора.
    """

    # Логин
    login_data = {
        "email": super_admin_data["email"],
        "password": super_admin_data["password"]
    }
    response = api_manager_session_scope.auth_api.login_user(login_data=login_data, expected_status=200)
    token = response.json().get("accessToken")
    if not token:
        pytest.fail("Failed to get SUPER_ADMIN access token.")
    print(f"SUPER_ADMIN token obtained for {super_admin_data['email']}")
    return token

@pytest.fixture(scope="session")
def api_manager_session_scope(): # Отдельный ApiManager для session-scope фикстур, чтобы избежать конфликтов

    """
    ApiManager с привязкой к сессии для super_admin_token
    """

    s = requests.Session()
    manager = ApiManager(s)

    yield manager
    s.close()

@pytest.fixture(scope='function')
def movie_data():

    """
    Фикстура для генерации валидных данных фильма.
    """
    location = ["MSK", "SPB"]
    return {
        "name": f"Test Movie - {global_faker.catch_phrase()}",
        "imageUrl": global_faker.image_url(),
        "price": random.randint(50, 500),
        "description": global_faker.text(max_nb_chars=150),
        "location": random.choice(location),
        "published": True,
        "genreId": random.randint(1, 10)
    }

@pytest.fixture(scope="function")
def create_movie(api_manager, super_admin_token, movie_data):

    """
    Фикстура для создания фильма и возврата его ID.
    Обеспечивает очистку (удаление) созданного фильма после теста.
    Имя фикстуры 'create_movie' соответствует использованию в примере теста на удаление.
    """

    headers_with_token = {
        "Authorization": f"Bearer {super_admin_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = api_manager.movies_api.create_movie(
        movie_data=movie_data,
        headers=headers_with_token,
        expected_status=201
    )
    created_movie_details = response.json()
    assert "id" in created_movie_details, "ID фильма отсутствует в ответе на создание"
    movie_id = created_movie_details["id"]

    yield movie_id

    # Код очистки после завершения теста
    try:
        print(f"Attempting to clean up movie with ID: {movie_id}")

        api_manager.movies_api.delete_movie(
            movie_id=movie_id,
            headers=headers_with_token,
            expected_status=200
        )
        print(f"Successfully cleaned up movie with ID: {movie_id}")
    except ValueError as e:
        # Если фильм уже был удален тестом, API может вернуть 404
        if "404" in str(e) or "not found" in str(e).lower():
            print(f"Movie with ID {movie_id} not found during cleanup (already deleted or never existed).")
        else:
            print(f"Error during movie cleanup (ID: {movie_id}): {e}. This might be an issue.")

    except Exception as e:
        print(f"An unexpected error occurred during movie cleanup (ID: {movie_id}): {e}")