from custom_requester.custom_requester import CustomRequester
from constants import MOVIES_API_BASE_URL


class GenresAPI(CustomRequester):
    """
    Класс для работы с API жанров фильмов
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_API_BASE_URL)

    def get_genres(self, expected_status=200):
        """
        Получение списка жанров фильмов.
        Доступно для всех PUBLIC
        """

        return self.send_request(
            method="GET",
            endpoint="/genres",
            expected_status=expected_status,
        )

    def get_genres_by_id(self, genre_id, expected_status=200):
        """
        Получение жанра по id
        """

        return self.send_request(
            method="GET",
            endpoint=f"/genres/{genre_id}",
            expected_status=expected_status,
        )

    def create_genre(self, genre_data, expected_status=201):
        """
        Создание нового жанра. Требуется токен авторизации с ролью SUPER_ADMIN.
        :param genre_data: Данные нового жанра (словарь с полем 'name').
        :param expected_status: 201
        """

        return self.send_request(
            method="POST",
            endpoint="/genres",
            data=genre_data,
            expected_status=expected_status,
        )

    def delete_genre_by_id(self, genre_id, expected_status=200):
        """
        Удаление жанра по id
        """

        return self.send_request(
            method="DELETE",
            endpoint=f"/genres/{genre_id}",
            expected_status=expected_status,
        )
