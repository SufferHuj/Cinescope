from custom_requester.custom_requester import CustomRequester

class MoviesAPI(CustomRequester):

    """
    Класс для работы с API фильмов.
    """

    def __init__(self, session, base_url):
        super().__init__(session=session, base_url=base_url)

    def get_movies(self, params=None, expected_status=200):
        """
        Получение списка фильмов.
        :param params: Параметры запроса (например, page, pageSize, minPrice, maxPrice, locations, published, genreId, order, createdAt).
        :param expected_status: Ожидаемый статус-код.
        :return: Объект ответа requests.Response.
        """
        return self.send_request(
            method="GET",
            endpoint="/movies",
            params=params,
            expected_status=expected_status
        )

    def get_movie_by_id(self, movie_id, expected_status=200):
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

    def create_movie(self, movie_data, headers=None, expected_status=201):
        """
        Создание нового фильма. Требуется токен авторизации.
        :param movie_data: Данные нового фильма (словарь).
        :param headers: Дополнительные заголовки, включая Authorization.
        :param expected_status: Ожидаемый статус-код (по умолчанию 201).
        :return: Объект ответа requests.Response.
        """
        return self.send_request(
            method="POST",
            endpoint="/movies",
            data=movie_data,
            headers=headers, # Передаем заголовки, содержащие токен
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, headers=None, expected_status=200): # Согласно Swagger, успешное удаление возвращает 200, а не 204
        """
        Удаление фильма по его ID. Требуется токен авторизации.
        :param movie_id: ID фильма.
        :param headers: Дополнительные заголовки, включая Authorization.
        :param expected_status: Ожидаемый статус-код (по умолчанию 200).
        :return: Объект ответа requests.Response.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{movie_id}",
            headers=headers, # Передаем заголовки, содержащие токен
            expected_status=expected_status
        )