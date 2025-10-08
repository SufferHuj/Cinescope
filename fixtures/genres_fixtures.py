import pytest

from utils.data_generator import faker as global_faker


@pytest.fixture(scope="function")
def genre_data() -> dict[str, str]:
    """Фикстура для генерации валидных данных жанра"""
    
    return {
        "name": f"Тестовый жанр - {global_faker.word()}{global_faker.random_number(digits=4)}",
    }