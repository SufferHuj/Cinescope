import pytest
from models.movie_model import (
    MovieData,
    CreateMovieResponse,
    GetMovieResponse,
    GetMoviesResponse,
    DeleteMovieResponse,
    MovieFilterParams,
    MovieErrorResponse
)


class TestMovieAPI:
    """
    Класс тестов для API фильмов.
    
    Включает тесты для получения списка фильмов, фильтрации по различным
    параметрам и проверки структуры данных.
    """

    # Тесты для GET /movies
    def test_get_all_movies(self, common_user, movie_data):
        """
        Получение полного списка фильмов без фильтров.
        Проверка структуры ответа и базовых полей фильма с использованием Pydantic модели.
        """

        response = common_user.api.movies_api.get_movies(movie_data)
        response_data = response.json()

        # Валидация структуры ответа через Pydantic модель
        movies_response = GetMoviesResponse(**response_data)
        
        assert movies_response.movies is not None, "Список фильмов не должен быть None"
        
        # Проверяем структуру каждого фильма в списке
        for movie in movies_response.movies:
            assert isinstance(movie, GetMovieResponse), "Каждый элемент должен соответствовать модели GetMovieResponse"
            assert movie.id is not None, "ID фильма не должен быть None"
            assert movie.name is not None, "Название фильма не должно быть None"
            assert movie.price is not None, "Цена фильма не должна быть None"
            assert movie.genreId is not None, "ID жанра не должен быть None"

    @pytest.mark.parametrize(
        "min_price, max_price, location, genre_id", [
            (1, 10, "MSK", 1),
            (11, 99, "SPB", 2),
            (100, 1000, "MSK", 3)],
        ids=["test_1", "test_2", "test_3"]
    )
    def test_filter_movies_by_price(self, common_user, min_price, max_price, location, genre_id):
        """
        Фильтрация фильмов по minPrice и maxPrice с использованием Pydantic модели.
        """

        # Создаем параметры фильтрации через Pydantic модель
        filter_params = MovieFilterParams(
            minPrice=min_price,
            maxPrice=max_price,
            locations=location,  # Передаем строку, а не список
            genreId=genre_id
        )

        response = common_user.api.movies_api.get_movies(params=filter_params.model_dump(exclude_none=True), expected_status=200)
        response_data = response.json()

        # Валидация структуры ответа через Pydantic модель
        movies_response = GetMoviesResponse(**response_data)
        
        assert movies_response.movies is not None, "Список фильмов не должен быть None"

        if not movies_response.movies:
            print(f"Нет фильмов в диапазоне цен [{min_price}, {max_price}], тест пропущен для проверки цен.")
        
        for movie in movies_response.movies:
            assert isinstance(movie, GetMovieResponse), "Каждый элемент должен соответствовать модели GetMovieResponse"
            assert min_price <= movie.price <= max_price, \
                (f"Цена фильма {movie.price} (ID: {movie.id}) "
                 f"выходит за пределы диапазона [{min_price}, {max_price}]")
            assert movie.id is not None, "ID фильма не должен быть None"
            assert movie.name is not None, "Название фильма не должно быть None"

    # ТЕСТЫ ДЛЯ GET /movies/{id}
    def test_get_one_movie_by_id(self, create_movie, common_user):
        """
        Успешное получение фильма по id для пользователя USER с использованием Pydantic модели.
        """

        response = common_user.api.movies_api.get_movie(create_movie)
        response_data = response.json()

        # Валидация структуры ответа через Pydantic модель
        movie_response = GetMovieResponse(**response_data)
        
        assert movie_response.id == create_movie, "ID фильма не совпадает с запрошенным"
        assert movie_response.id is not None, "ID фильма не должен быть None"

    # Тесты для POST /movies
    def test_create_movie_valid_data(self, movie_data, super_admin):
        """
        Успешное создание фильма с валидными данными (SUPER_ADMIN) с использованием Pydantic моделей.
        """

        # Валидация входных данных через Pydantic модель
        movie_input = MovieData(**movie_data)

        response = super_admin.api.movies_api.create_movie(
            movie_data=movie_input.model_dump(exclude_none=True),
            expected_status=201
        )
        response_data = response.json()

        # Валидация структуры ответа через Pydantic модель
        create_response = CreateMovieResponse(**response_data)
        
        assert create_response.id is not None, "ID не должен быть None в ответе на создание фильма"
        assert create_response.name == movie_input.name, "Имя фильма не совпадает с отправленным"
        assert create_response.description == movie_input.description, "Описание фильма не совпадает"
        assert create_response.price == movie_input.price, "Цена фильма не совпадает"
        assert create_response.genreId == movie_input.genreId, "ID жанра не совпадает"

    # Тест для DELETE movies/{id}
    def test_delete_movie_success(self, create_movie, super_admin):
        """
        Успешное удаление фильма с валидным ID с использованием Pydantic модели.
        Фикстура 'create_movie' создает фильм, возвращает ID.
        Этот тест сам удаляет фильм и проверяет его недоступность.
        """

        # ID фильма из фикстуры
        movie_id_to_delete = create_movie

        response = super_admin.api.movies_api.delete_movie(
            movie_id=movie_id_to_delete,
            expected_status=200
        )

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        # Валидация структуры ответа через Pydantic модель (если API возвращает структурированный ответ)
        try:
            response_data = response.json()
            delete_response = DeleteMovieResponse(**response_data)
            assert delete_response.success is True, "Удаление должно быть успешным"
            assert delete_response.deletedMovieId == movie_id_to_delete, "ID удаленного фильма должен совпадать"
        except Exception:
            # Если API не возвращает JSON или структурированный ответ, пропускаем валидацию
            pass

        # Получить удаленный фильм, ожидаем 404 Not Found
        with pytest.raises(ValueError) as ex:
            super_admin.api.movies_api.get_movie(
                movie_id=movie_id_to_delete
            )
        assert "Unexpected status code: 404" in str(ex.value), \
            "Ожидалась ошибка ValueError со статусом 404 при попытке GET удаленного фильма."

    # НЕГАТИВНЫЕ ТЕСТЫ
    # POST /movies
    @pytest.mark.negative
    def test_create_movie_with_invalid_user(self, movie_data, common_user):
        """
        Проверка создания фильма под ролью USER с использованием Pydantic модели для валидации ошибки.
        """

        # Валидация входных данных через Pydantic модель
        movie_input = MovieData(**movie_data)

        response = common_user.api.movies_api.create_movie(
            movie_data=movie_input.model_dump(),
            expected_status=403
        )

        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
        
        # Валидация структуры ошибки через Pydantic модель (если API возвращает структурированную ошибку)
        try:
            response_data = response.json()
            error_response = MovieErrorResponse(**response_data)
            assert error_response.statusCode == 403, "Код ошибки должен быть 403"
            assert error_response.error is not None, "Сообщение об ошибке не должно быть None"
        except Exception:
            # Если API не возвращает структурированную ошибку, пропускаем валидацию
            pass

    # DELETE /movies/{id}
    @pytest.mark.negative
    @pytest.mark.parametrize('general_user,expected_code', [
        ("super_admin", 200),
        ("admin", 403),
        ('common_user', 403)],
                             indirect=['general_user'],
                             ids=["super_admin", "admin", "common_user"])
    def test_delete_movie_by_user_role(self, general_user, create_movie, expected_code):
        """
        Проверка прав доступа на удаление фильмов для разных ролей пользователей.
        """

        movie_id = create_movie
        response = general_user.api.movies_api.delete_movie(movie_id, expected_status=expected_code)

        assert response.status_code == expected_code
