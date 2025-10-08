import pytest

from resources.test_card_data import TestCardData
from utils.data_generator import faker as global_faker


@pytest.fixture(scope='function')
def payment_request_data(create_movie):
    """Фикстура для генерации данных для создания платежа"""
    
    return {
        "movieId": create_movie,
        "amount": global_faker.random_int(min=100, max=10000),
        "card": TestCardData.CARD_DATA
    }