from custom_requester.custom_requester import CustomRequester
from constants import MOVIES_API_BASE_URL


class ReviewsAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_API_BASE_URL)

    def get_movie_reviews(self, movie_id, expected_status=200):
        """
        Получение отзывов о фильме. Доступ PUBLIC
        """

        return self.send_request(
            method="GET",
            endpoint=f"/movies/{movie_id}/reviews",
            expected_status=expected_status
        )

    def create_review(self, movie_id, review_data, expected_status=200):
        """
        Создание отзыва к фильму. Role: USER, ADMIN, SUPER_ADMIN
        """

        return self.send_request(
            method="POST",
            endpoint=f"/movies/{movie_id}/reviews",
            data=review_data,
            expected_status=expected_status
        )

    def update_review(self, movie_id, review_data, expected_status=200):
        """
        Редактирование отзыва к фильму. Role: USER, ADMIN, SUPER_ADMIN
        """

        return self.send_request(
            method="PUT",
            endpoint=f"/movies/{movie_id}/reviews",
            data=review_data,
            expected_status=expected_status
        )

    def hide_review(self, movie_id, user_id, expected_status=200):
        """
        Скрытие отзыва к фильму. Требуется токен авторизации. Role: USER, ADMIN, SUPER_ADMIN
        """

        return self.send_request(
            method="PATCH",
            endpoint=f"/movies/{movie_id}/reviews/hide/{user_id}",
            expected_status=expected_status
        )

    def show_review(self, movie_id, user_id, expected_status):
        """
        Показ отзыва к фильму. Требуется токен авторизации. Role: USER, ADMIN, SUPER_ADMIN
        """

        return self.send_request(
            method="PATCH",
            endpoint=f"/movies/{movie_id}/reviews/show/{user_id}",
            expected_status=expected_status
        )
