import pytest
import requests
import random
from datetime import datetime

from api.api_manager import ApiManager
from constants import BASE_URL
from custom_requester.custom_requester import CustomRequester
from resources.test_card_data import TestCardData
from utils.data_generator import DataGenerator
from entities.user import User
from resources.user_creds import SuperAdminCreds
from constants import Roles
from models.auth_model import TestUserData
from utils.data_generator import faker as global_faker
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper


# ФИКСТУРЫ ДЛЯ ТЕСТОВ AuthAPI и UserAPI

@pytest.fixture(scope='function')
def test_user():
    """
    Генерация случайного пользователя для тестов.
    
    Создает тестового пользователя с случайными данными:
    - email, имя и пароль генерируются автоматически
    - роль по умолчанию - USER
    
    Returns:
        TestUserData: Объект с данными тестового пользователя
    """


    random_password = DataGenerator.generation_random_password()

    return TestUserData(
        email=DataGenerator.generation_random_email(),
        fullName=DataGenerator.generation_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]  # Изменено с Roles.USER.value на Roles.USER
    )


@pytest.fixture(scope="function")
def registered_user(api_manager, test_user: TestUserData):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    
    Выполняет полный цикл работы с тестовым пользователем:
    - Регистрирует пользователя через API
    - Предоставляет данные для использования в тестах
    - Обеспечивает автоматическую очистку после завершения теста
    
    Args:
        api_manager: Менеджер для работы с API
        test_user: Данные тестового пользователя
        
    Yields:
        dict: Словарь с данными зарегистрированного пользователя, включая ID
        
    Note:
        Пользователь удаляет сам себя согласно API документации.
    """

    # Регистрируем нового пользователя через API
    response = api_manager.auth_api.register_user(user_data=test_user, expected_status=201)
    response_data = response.json()

    # Преобразуем Pydantic модель в словарь для удобства работы
    created_user = test_user.model_dump()
    # Добавляем ID пользователя, полученный от API после регистрации
    created_user["id"] = response_data["id"]

    # Сохраняем пароль в открытом виде для возможной авторизации
    created_user["password_plain"] = test_user.password

    yield created_user

    try:
        # Авторизуемся под созданным пользователем для удаления
        api_manager.auth_api.authenticate((test_user.email, test_user.password))
        # Пользователь удаляет сам себя
        api_manager.user_api.clean_up_user(user_id=created_user["id"])
    except Exception as e:
        print(f"Failed to clean up user {created_user.get('id')}: {e}")


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
    
    Создает центральный менеджер для работы со всеми API эндпоинтами.
    Использует переданную HTTP сессию для выполнения запросов.
    
    Args:
        session: HTTP сессия для выполнения запросов
        
    Returns:
        ApiManager: Настроенный менеджер для работы с API
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

    user_name = SuperAdminCreds.USERNAME
    password = SuperAdminCreds.PASSWORD

    if user_name is None or password is None:
        raise ValueError("SUPER_ADMIN_USERNAME и SUPER_ADMIN_PASSWORD должны быть установлены в переменных окружения")

    super_admin = User(
        user_name,
        password,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user: TestUserData):
    """
    Фикстура для создания общего юзера
    """

    updated_data = test_user.model_dump()
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
    patch_data = {"roles": [Roles.ADMIN.value]}
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


# ФИКСТУРЫ ДЛЯ ТЕСТОВ ReviewsAPI

@pytest.fixture(scope="function")
def review_data():
    """
    Фикстура для генерации валидных данных отзыва
    """

    return {
        "rating": random.randint(1, 5),
        "text": f"Тестовый отзыв - {global_faker.text(max_nb_chars=100)}"
    }

# ФИКСТУРЫ ДЛЯ ТЕСТОВ PaymentAPI

@pytest.fixture(scope='function')
def payment_request_data(create_movie):
    """
    Фикстура для генерации данных для создания платежа
    """

    return {
        "movieId": create_movie,
        "amount": global_faker.random_int(min=100, max=10000),
        "card": TestCardData.CARD_DATA
    }

# ФИКСТУРЫ ДЛЯ ТЕСТОВ БД 

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """

    db_session = get_db_session()

    yield db_session

    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """

    db_helper = DBHelper(db_session)

    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """

    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    
    yield user

    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope="function")
def movie_test_data():
    """
    Фикстура для генерации тестовых данных фильма для БД
    """
    locations = ["MSK", "SPB"]
    
    return {
        'name': f"Тестовый фильм - {global_faker.catch_phrase()}",
        'price': random.randint(100, 1000),
        'description': global_faker.text(max_nb_chars=200),
        'image_url': global_faker.image_url(),
        'location': random.choice(locations),
        'published': random.choice([True, False]),
        'rating': round(random.uniform(1.0, 5.0), 1),
        'genre_id': random.randint(1, 10),
        'created_at': datetime.now()
    }
