import pytest
import random

from utils.data_generator import faker as global_faker


@pytest.fixture(scope="function")
def review_data():
    """Фикстура для генерации валидных данных отзыва"""
    
    return {
        "rating": random.randint(1, 5),
        "text": f"Тестовый отзыв - {global_faker.text(max_nb_chars=100)}"
    }