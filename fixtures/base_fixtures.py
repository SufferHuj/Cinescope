import pytest
import requests

from api.api_manager import ApiManager
from constants import BASE_URL
from custom_requester.custom_requester import CustomRequester


@pytest.fixture(scope="session")
def requester():
    """Фикстура для создания экземпляра CustomRequester"""

    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)


@pytest.fixture(scope="session")
def session():
    """Фикстура для создания HTTP-сессии"""

    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """Фикстура для создания экземпляра ApiManager"""

    return ApiManager(session)


@pytest.fixture()
def user_session():
    """Фикстура на создание сессии юзера"""
    
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()