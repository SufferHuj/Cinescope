import pytest
import requests
from api.api_manager import ApiManager
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator


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

# @pytest.fixture(scope="session")
# def auth_session(test_user): # ВНИМАНИЕ: эта фикстура использует test_user, который по scope='function'.
#                              # Это может привести к тому, что auth_session будет создаваться для каждого теста,
#                              # даже если она scope='session'. Лучше передать email/password явно или
#                              # сделать test_user тоже session-scoped, если он не меняется.
#                              # На данный момент, для решения текущей проблемы, это не критично.
#
#     # Регистрируем нового пользователя
#     register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
#
#     response = requests.post(register_url, json= test_user, headers= HEADERS)
#
#     assert response.status_code == 201, "Ошибка регистрации пользователя"
#
#     # Логинимся для получения токена
#     login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
#
#     login_data = {
#         "email": test_user["email"],
#         "password": test_user["password"]
#     }
#
#     response = requests.post(login_url, json= login_data, headers= HEADERS)
#     assert response.status_code == 200, "Ошибка авторизации"
#
#     # Получаем токен и создаём сессию
#     token = response.json().get("accessToken")
#     assert token is not None, "Токен доступа отсутствует в ответе"
#
#     session = requests.Session()
#     session.headers.update(HEADERS)
#     session.headers.update({"Authorization": f"Bearer {token}"})
#     return session

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    Обеспечивает очистку созданного пользователя после завершения теста.
    """
    response = api_manager.auth_api.register_user(user_data= test_user, expected_status= 201)

    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]

    yield registered_user # Возвращаем зарегистрированного пользователя для использования в тесте
    # Код после 'yield' выполняется после завершения теста
    api_manager.user_api.clean_up_user(user_id= registered_user["id"])

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
    # ИЗМЕНЕНО: Добавляем BASE_URL при инициализации ApiManager
    return ApiManager(session, BASE_URL)