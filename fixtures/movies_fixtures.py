import pytest
import random

from utils.data_generator import faker as global_faker


@pytest.fixture(scope='function')
def movie_data():
    """Фикстура для генерации валидных данных фильма"""

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
    """Фикстура для создания фильма и возврата его ID"""
    
    response = super_admin.api.movies_api.create_movie(
        movie_data=movie_data,
        expected_status=201
    )

    created_movie_details = response.json()

    assert "id" in created_movie_details, "ID фильма отсутствует в ответе на создание"
    movie_id = created_movie_details["id"]

    return movie_id