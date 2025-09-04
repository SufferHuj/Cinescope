from custom_requester.custom_requester import CustomRequester
from constants import MOVIES_API_BASE_URL


class MoviesAPI(CustomRequester):
    """
    Класс для работы с API фильмов.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_API_BASE_URL)

    def get_movies(self, params=None, expected_status=200):
        """
        Получение списка фильмов. :param params: Параметры запроса (например, page, pageSize, minPrice, maxPrice,
        locations, published, genreId, order, createdAt). :param expected_status: Ожидаемый статус-код. :return:
        Объект ответа requests.Response.
        """

        return self.send_request(
            method="GET",
            endpoint="/movies",
            params=params,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
        """
        Получение конкретного фильма по его ID.
        :param movie_id: ID фильма.
        :param expected_status: Ожидаемый статус-код.
        :return: Объект ответа requests.Response.
        """

        return self.send_request(
            method="GET",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=201):
        """
        Создание нового фильма. Требуется токен авторизации.
        :param movie_data: Данные нового фильма (словарь).
        :param expected_status: Ожидаемый статус-код (по умолчанию 201).
        :return: Объект ответа requests.Response.
        """

        return self.send_request(
            method="POST",
            endpoint="/movies",
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status):
        """
        Удаление фильма по его ID. Требуется токен авторизации.
        :param movie_id: ID фильма.
        :param expected_status: Ожидаемый статус-код (по умолчанию 200).
        :return: Объект ответа requests.Response.
        """

        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )
