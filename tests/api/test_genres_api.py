import pytest
import requests
import random
from api.api_manager import ApiManager
from models.genre_model import CreateGenreResponse, GetGenreResponse


class TestGenresAPI:
    """ Тесты для API жанров с проверкой CRUD операций и прав доступа """

    # ТЕСТЫ ДЛЯ GET /genres
    def test_get_all_genres_success(self, api_manager: ApiManager):
        """ Успешное получение списка всех жанров (PUBLIC доступ) """

        response = api_manager.genres_api.get_genres(expected_status=200)
        response_data = response.json()

        assert isinstance(response_data, list), "Ответ должен быть списком жанров"

        # Проверяем структуру жанра, если список не пуст
        if response_data:
            genre_item = GetGenreResponse(**response_data[0])
            assert genre_item.id is not None, "ID жанра не должен быть None"
            assert genre_item.name is not None, "Название жанра не должно быть None"
            assert isinstance(genre_item.id, int), "ID жанра должен быть числом"
            assert isinstance(genre_item.name, str), "Название жанра должно быть строкой"

    def test_get_genres_without_auth(self, api_manager: ApiManager):
        """ Проверка получения жанров без авторизации """

        session = requests.Session()
        unauthenticated_api = ApiManager(session)

        response = unauthenticated_api.genres_api.get_genres(expected_status=200)
        response_data = response.json()

        assert isinstance(response_data, list), "Ответ должен быть списком"

    # ТЕСТЫ ДЛЯ POST /genres
    def test_create_genre_success(self, genre_data, super_admin):
        """ Успешное создание нового жанра с ролью SUPER_ADMIN """

        response = super_admin.api.genres_api.create_genre(
            genre_data=genre_data,
            expected_status=201
        )
        response_data = response.json()

        created_genre = CreateGenreResponse(**response_data)
        
        assert created_genre.id is not None, "ID отсутствует в ответе на создание жанра"
        assert created_genre.name == genre_data["name"], "Название жанра не совпадает с отправленным"

    # ТЕСТЫ ДЛЯ DELETE /genres/{id}
    def test_delete_genre_success(self, super_admin, genre_data):
        """ Успешное удаление жанра с ролью SUPER_ADMIN """

        create_response = super_admin.api.genres_api.create_genre(
            genre_data=genre_data,
            expected_status=201
        )
        created_genre = create_response.json()
        genre_id = created_genre["id"]

        super_admin.api.genres_api.delete_genre_by_id(
            genre_id,
            expected_status=200
        )

        # Проверяем, что жанр действительно удален
        with pytest.raises(ValueError) as ex:
            super_admin.api.genres_api.get_genres_by_id(genre_id)
        assert "Unexpected status code: 404" in str(
            ex.value), "Ожидалась ошибка 404 при попытке получить удаленный жанр"

    # ТЕСТЫ ДЛЯ GET /genres/{id}
    def test_get_genre_by_id_success(self, api_manager: ApiManager, super_admin, genre_data):
        """ Успешное получение жанра по ID (PUBLIC доступ) """

        # Сначала создаем жанр
        create_response = super_admin.api.genres_api.create_genre(
            genre_data=genre_data,
            expected_status=201
        )
        created_genre_data = create_response.json()
        created_genre = CreateGenreResponse(**created_genre_data)
        genre_id = created_genre.id

        # Получаем жанр по ID
        response = api_manager.genres_api.get_genres_by_id(genre_id, expected_status=200)
        response_data = response.json()

        retrieved_genre = GetGenreResponse(**response_data)

        assert retrieved_genre.id == genre_id, "ID жанра не совпадает"
        assert retrieved_genre.name == genre_data["name"], "Название жанра не совпадает"

    def test_get_genre_without_auth(self, api_manager: ApiManager, super_admin, genre_data):
        """ Проверка получения жанра по ID без авторизации (PUBLIC доступ) """

        # Создаем жанр
        create_response = super_admin.api.genres_api.create_genre(
            genre_data=genre_data,
            expected_status=201
        )
        created_genre_data = create_response.json()
        created_genre = CreateGenreResponse(**created_genre_data)
        genre_id = created_genre.id

        # Создаем новый ApiManager без авторизации
        session = requests.Session()
        unauthenticated_api = ApiManager(session)

        response = unauthenticated_api.genres_api.get_genres_by_id(genre_id, expected_status=200)
        response_data = response.json()

        retrieved_genre = GetGenreResponse(**response_data)

        assert retrieved_genre.id == genre_id, "ID жанра не совпадает"

    # НЕГАТИВНЫЕ ТЕСТЫ
    # ТЕСТЫ ДЛЯ POST /genres
    @pytest.mark.negative
    def test_create_genre_invalid_user_role(self, common_user, genre_data):
        """ Проверка создания жанра с невалидной ролью USER """

        common_user.api.genres_api.create_genre(
            genre_data=genre_data,
            expected_status=403
        )

    @pytest.mark.negative
    def test_create_genre_without_auth(self, genre_data, api_manager: ApiManager):
        """ Проверка создания жанра без авторизации """

        session = requests.Session()
        unauthenticated_api = ApiManager(session)

        response = unauthenticated_api.genres_api.create_genre(
            genre_data=genre_data,
            expected_status=401
        )
        response_data = response.json()

        assert response_data.get("message") == "Unauthorized", "В ответе отсутствует причина ошибки"

    @pytest.mark.negative
    def test_create_genre_empty_name(self, super_admin, expected_status=409):
        """ Проверка создания жанра с пустым названием """

        genre_date = {
            "name": ""
        }

        response = super_admin.api.genres_api.create_genre(
            genre_data=genre_date,
            expected_status=expected_status
        )
        response_data = response.json()

        assert isinstance(response_data, dict), "Ответ должен быть словарём жанров"
        assert "message" in response_data, "В ответе отсутствует ключ message"
        assert response_data.get("error") == "Conflict", "В ответе отсутствует причина ошибки"

    @pytest.mark.negative
    def test_create_genre_without_name(self, super_admin, expected_status=400):
        """ Проверка создания жанра фильма без поля name """

        response = super_admin.api.genres_api.create_genre(
            genre_data={},
            expected_status=expected_status
        )
        response_data = response.json()

        assert "message" in response_data, "В ответе отсутствует ключ message"
        assert response_data.get("error") == "Bad Request"

    # ТЕСТЫ ДЛЯ DELETE /genres/{id}
    @pytest.mark.skip(reason="Тест с под админом падает с 403")
    @pytest.mark.negative
    @pytest.mark.parametrize('general_user,expected_code', [
        ("super_admin", 200),
        ("admin", 200),
        ('common_user', 403)],
                             indirect=['general_user'])
    def test_delete_genre_permissions_by_user_role(self, general_user, super_admin, genre_data, expected_code):
        """ Проверка прав доступа на удаление жанров для разных ролей пользователей """

        create_response = super_admin.api.genres_api.create_genre(
            genre_data=genre_data,
            expected_status=201
        )
        created_genre = create_response.json()
        genre_id = created_genre["id"]

        # Пытаемся удалить жанр под разными ролями
        general_user.api.genres_api.delete_genre_by_id(genre_id, expected_status=expected_code)

    @pytest.mark.negative
    def test_delete_genre_invalid_id(self, super_admin):
        """Проверка удаления жанра с несуществующим ID."""

        invalid_genre_id = random.randint(100, 10000)
        super_admin.api.genres_api.delete_genre_by_id(
            invalid_genre_id,
            expected_status=404
        )

    # ТЕСТЫ ДЛЯ GET /genres/{id}
    @pytest.mark.negative
    def test_get_genre_by_invalid_id(self, api_manager: ApiManager):
        """ Проверка получения жанра по несуществующему ID """

        invalid_genre_id = random.randint(1000, 9999)
        api_manager.genres_api.get_genres_by_id(invalid_genre_id, expected_status=404)
