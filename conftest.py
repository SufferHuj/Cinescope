import pytest
import requests
import random

from api.api_manager import ApiManager
from constants import BASE_URL
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from entities.user import User
from resources.user_creds import SuperAdminCreds
from constants import Roles
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
        "roles": [Roles.USER.value]
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
        print(f"Не удалось очистить пользователя {created_user.get('id')}: {e}")


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


@pytest.fixture()
def user_session():
    """
    Фикстура на создание сессии юзера
    """

    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    """
    Фикстура на создание пользователя с ролью SUPER_ADMIN
    """

    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    """
    Фикстура для создания общего юзера
    """

    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    """
    Фикстура для создания юзера с ролью USER
    """

    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    """
    Фикстура для создания юзера с ролью ADMIN
    """

    new_session = user_session()

    # Создаем пользователя
    response = super_admin.api.user_api.create_user(creation_user_data)
    created_user = response.json()
    user_id = created_user["id"]

    # Присваиваем пользователю роль ADMIN
    patch_data = {"roles": [Roles.ADMIN.value, Roles.SUPER_ADMIN.value]}
    super_admin.api.user_api.patch_user(user_id, patch_data)

    admin_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value],
        new_session)

    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user


@pytest.fixture
def general_user(request):
    """
    Фикстура для передачи ролей пользователей в тестовый метод
    """
    return request.getfixturevalue(request.param)


# ФИКСТУРЫ ДЛЯ ТЕСТОВ MoviesAPI
@pytest.fixture(scope='function')
def movie_data():
    """
    Фикстура для генерации валидных данных фильма.
    """

    location = ["MSK", "SPB"]

    return {
        "name": f"Тестовое кино - {global_faker.catch_phrase()}",
        "imageUrl": global_faker.image_url(),
        "price": random.randint(50, 500),
        "description": global_faker.text(max_nb_chars=150),
        "location": random.choice(location),
        "published": True,
        "genreId": random.randint(1, 10)
    }


@pytest.fixture(scope="function")
def create_movie(super_admin, movie_data):
    """
    Фикстура для создания фильма и возврата его ID.
    Обеспечивает очистку (удаление) созданного фильма после теста.
    Имя фикстуры 'create_movie' соответствует использованию в примере теста на удаление.
    """

    response = super_admin.api.movies_api.create_movie(
        movie_data=movie_data,
        expected_status=201
    )

    created_movie_details = response.json()

    assert "id" in created_movie_details, "ID фильма отсутствует в ответе на создание"
    movie_id = created_movie_details["id"]

    return movie_id


# ФИКСТУРЫ ДЛЯ ТЕСТОВ GenresAPI

@pytest.fixture(scope="function")
def genre_data() -> dict[str, str]:
    """
    Фикстура для генерации валидных данных жанра
    """

    return {
        "name": f"Тестовый жанр - {global_faker.word()}{global_faker.random_number(digits=4)}",
    }
