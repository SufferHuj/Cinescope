import pytest


class TestMovieAPI:

    # Тесты для GET /movies
    def test_get_all_movies(self, common_user, movie_data):
        """
        Получение полного списка фильмов без фильтров.
        Проверка структуры ответа и базовых полей фильма.
        """

        response = common_user.api.movies_api.get_movies(movie_data)
        response_data = response.json()

        assert "movies" in response_data, "Ключ 'movies' отсутствует в ответе"

        if response_data["movies"]:  # Проверяем структуру, если список не пуст
            movie_item = response_data["movies"][0]
            assert "id" in movie_item, "Поле 'id' отсутствует в элементе фильма"
            assert "name" in movie_item, "Поле 'name' отсутствует в элементе фильма"
            assert "price" in movie_item, "Поле 'price' отсутствует в элементе фильма"
            assert "genreId" in movie_item, "Поле 'genreId' отсутствует в элементе фильма"

    @pytest.mark.parametrize(
        "min_price, max_price, location, genre_id", [
            (1, 10, "MSK", 1),
            (11, 99, "SPB", 2),
            (100, 1000, "MSK", 3)],
        ids=["test_1", "test_2", "test_3"]
    )
    def test_filter_movies_by_price(self, common_user, min_price, max_price, location, genre_id):
        """
        Фильтрация фильмов по minPrice и maxPrice.
        """

        params = {
            "minPrice": min_price,
            "maxPrice": max_price,
            "locations": location,
            "genreId": genre_id
        }

        response = common_user.api.movies_api.get_movies(params=params, expected_status=200)
        response_data = response.json()

        assert "movies" in response_data

        if not response_data["movies"]:
            print(f"Нет фильмов в диапазоне цен [{min_price}, {max_price}], тест пропущен для проверки цен.")
        for movie in response_data["movies"]:
            assert "price" in movie, "У фильма отсутствует поле 'price'"
            assert min_price <= movie["price"] <= max_price, \
                (f"Цена фильма {movie['price']} (ID: {movie.get('id')}) "
                 f"выходит за пределы диапазона [{min_price}, {max_price}]")
            assert "id" in movie
            assert "name" in movie

    # ТЕСТЫ ДЛЯ GET /movies/{id}
    def test_get_one_movie_by_id(self, create_movie, common_user):
        """
        Успешное получение фильма по id для пользователя USER
        """

        response = common_user.api.movies_api.get_movie(create_movie)
        response_data = response.json()

        assert "id" in response_data, "ID отсутствует в ответе на создание фильма"
        assert response_data["id"] == create_movie, "ID фильма отсутствует"

    # Тесты для POST /movies
    def test_create_movie_valid_data(self, movie_data, super_admin):
        """
        Успешное создание фильма с валидными данными (SUPER_ADMIN)
        """

        response = super_admin.api.movies_api.create_movie(
            movie_data=movie_data,
            expected_status=201
        )
        response_data = response.json()

        assert "id" in response_data, "ID отсутствует в ответе на создание фильма"
        assert response_data["name"] == movie_data["name"], "Имя фильма не совпадает с отправленным"
        assert response_data["description"] == movie_data["description"], "Описание фильма не совпадает"
        assert response_data["price"] == movie_data["price"], "Цена фильма не совпадает"
        assert response_data["genreId"] == movie_data["genreId"], "ID жанра не совпадает"

    # Тест для DELETE movies/{id}
    def test_delete_movie_success(self, create_movie, super_admin):
        """
        Успешное удаление фильма с валидным ID.
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

        # Получить удаленный фильм, ожидаем 404 Not Found
        with pytest.raises(ValueError) as ex:
            super_admin.api.movies_api.get_movie(
                movie_id=movie_id_to_delete
            )
        assert "Неожиданный код статуса: 404" in str(ex.value), \
            "Ожидалась ошибка ValueError со статусом 404 при попытке GET удаленного фильма."

    # НЕГАТИВНЫЕ ТЕСТЫ
    # POST /movies
    @pytest.mark.negative
    def test_create_movie_with_invalid_user(self, movie_data, common_user):
        """
        Проверка создания фильма под ролью USER
        """

        response = common_user.api.movies_api.create_movie(
            movie_data=movie_data,
            expected_status=403
        )

        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"

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
