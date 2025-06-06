import pytest
from api.api_manager import ApiManager


class TestMovieAPI:

    # Тесты для GET

    def test_get_all_movies(self, api_manager: ApiManager):

        """
        Получение полного списка фильмов без фильтров.
        Проверка структуры ответа и базовых полей фильма.
        """
        response = api_manager.movies_api.get_movies(expected_status=200)
        response_data = response.json()

        assert "movies" in response_data, "Ключ 'movies' отсутствует в ответе"

        if response_data["movies"]: # Проверяем структуру, если список не пуст
            movie_item = response_data["movies"][0]
            assert "id" in movie_item, "Поле 'id' отсутствует в элементе фильма"
            assert "name" in movie_item, "Поле 'name' отсутствует в элементе фильма"
            assert "price" in movie_item, "Поле 'price' отсутствует в элементе фильма"
            assert "genreId" in movie_item, "Поле 'genreId' отсутствует в элементе фильма"


    def test_filter_movies_by_price(self, api_manager: ApiManager):

        """
        Фильтрация фильмов по minPrice и maxPrice.
        """

        min_price, max_price = 100, 1000
        params = {"minPrice": min_price, "maxPrice": max_price}

        response = api_manager.movies_api.get_movies(params=params, expected_status=200)
        response_data = response.json()

        assert "movies" in response_data

        if not response_data["movies"]:
            print(f"Нет фильмов в диапазоне цен [{min_price}, {max_price}], тест пропущен для проверки цен.")
        for movie in response_data["movies"]:
            assert "price" in movie, "У фильма отсутствует поле 'price'"
            assert min_price <= movie["price"] <= max_price, \
                f"Цена фильма {movie['price']} (ID: {movie.get('id')}) выходит за пределы диапазона [{min_price}, {max_price}]"
            assert "id" in movie
            assert "name" in movie

    # Тест для POST

    def test_create_movie_valid_data(self, super_admin_token, movie_data, api_manager: ApiManager):
        """
        Успешное создание фильма с валидными данными.
        """
        headers = {"Authorization": f"Bearer {super_admin_token}"}
        response = api_manager.movies_api.create_movie(
            movie_data=movie_data,
            headers=headers,
            expected_status=201
        )
        response_data = response.json()

        assert "id" in response_data, "ID отсутствует в ответе на создание фильма"
        assert response_data["name"] == movie_data["name"], "Имя фильма не совпадает с отправленным"
        assert response_data["description"] == movie_data["description"], "Описание фильма не совпадает"
        assert response_data["price"] == movie_data["price"], "Цена фильма не совпадает"
        assert response_data["genreId"] == movie_data["genreId"], "ID жанра не совпадает"


    # Тесты для DELETE

    def test_delete_movie_success(self, api_manager: ApiManager, create_movie, super_admin_token):

        """
        Успешное удаление фильма с валидным ID.
        Фикстура 'create_movie' создает фильм и возвращает его ID.
        """

        movie_id_to_delete = create_movie  # ID фильма из фикстуры

        headers = {"Authorization": f"Bearer {super_admin_token}"}

        response = api_manager.movies_api.delete_movie(
            movie_id=movie_id_to_delete,
            headers=headers,
            expected_status=200
        )

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    def test_delete_movie_check_get_fails(self, api_manager: ApiManager, create_movie, super_admin_token):

        """
        Проверка, что фильм больше не доступен через GET /movies/{id} после удаления.
        Фикстура 'create_movie' создает фильм, возвращает ID и удаляет его в teardown.
        Этот тест сам удаляет фильм и проверяет его недоступность.
        """

        movie_id_to_delete_and_check = create_movie
        headers = {"Authorization": f"Bearer {super_admin_token}"}

        api_manager.movies_api.delete_movie(
            movie_id=movie_id_to_delete_and_check,
            headers=headers,
            expected_status=200
        )

        # Получить удаленный фильм, ожидаем 404 Not Found
        with pytest.raises(ValueError) as ex:
            api_manager.movies_api.get_movie_by_id(
                movie_id=movie_id_to_delete_and_check
                # get_movie_by_id по умолчанию ожидает 200,
                # поэтому если фильм не найден (404), CustomRequester выбросит ValueError
            )
        assert "Unexpected status code: 404" in str(ex.value), \
            "Ожидалась ошибка ValueError со статусом 404 при попытке GET удаленного фильма."