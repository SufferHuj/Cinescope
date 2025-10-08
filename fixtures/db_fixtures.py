import pytest
import random
from datetime import datetime
from sqlalchemy.orm import Session

from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from db_models.db_payment_model import PaymentStatus
from utils.data_generator import DataGenerator, faker as global_faker


@pytest.fixture(scope="module")
def db_session() -> Session:
    """Фикстура для создания сессии БД"""

    db_session = get_db_session()
    yield db_session
    db_session.close()


@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """Фикстура для экземпляра хелпера"""

    db_helper = DBHelper(db_session)
    return db_helper


@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """Фикстура для создания тестового пользователя в БД"""

    user = db_helper.users.create_test_user(DataGenerator.generate_user_data())
    
    yield user

    # Cleanup после теста
    if db_helper.users.get_user_by_id(user.id):
        db_helper.users.delete_user(user)


@pytest.fixture(scope="function")
def movie_test_data():
    """Фикстура для генерации тестовых данных фильма для БД"""

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


@pytest.fixture(scope="function")
def review_test_data():
    """Фикстура для генерации тестовых данных отзыва для БД"""
    
    return {
        'text': global_faker.text(max_nb_chars=200),
        'rating': global_faker.random_int(min=1, max=5),
        'hidden': False,
        'created_at': datetime.now()
    }


@pytest.fixture(scope="function")
def payment_test_data():
    """Фикстура для генерации тестовых данных платежа для БД тестов"""
    
    def _create_payment_data(user_id=None, movie_id=None, status=None):    
        return {
            'user_id': user_id or DataGenerator.generation_random_uuid(),
            'movie_id': movie_id or DataGenerator.generation_random_uuid(),
            'status': status or random.choice(list(PaymentStatus)),
            'amount': global_faker.random_int(min=100, max=2000),
            'total': global_faker.random_int(min=100, max=2000),
            'created_at': datetime.now()
        }
    
    return _create_payment_data