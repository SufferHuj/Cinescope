import pytest

from constants import Roles
from entities.user import User
from models.auth_model import TestUserData
from resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator


@pytest.fixture(scope='function')
def test_user():
    """Генерация случайного пользователя для тестов"""

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
    """Фикстура для регистрации и получения данных зарегистрированного пользователя"""

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


@pytest.fixture
def super_admin(user_session):
    """Фикстура на создание пользователя с ролью SUPER_ADMIN"""

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
    """Фикстура для создания общего юзера"""

    updated_data = test_user.model_dump()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    """Фикстура для создания юзера с ролью USER"""

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
    """Фикстура для создания юзера с ролью ADMIN"""

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
    """Фикстура для передачи ролей пользователей в тестовый метод"""
    
    return request.getfixturevalue(request.param)