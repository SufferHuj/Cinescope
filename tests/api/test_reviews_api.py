import pytest
from api.api_manager import ApiManager
from utils.data_generator import faker as global_faker


class TestReviewsAPI:

    # ТЕСТЫ ДЛЯ GET /movies/{movieId}/reviews
    def test_get_movie_reviews_success(self, api_manager: ApiManager, create_movie):
        """
        Успешное получение отзывов фильма(PUBLIC).
        """
        movie_id = create_movie

        response = api_manager.reviews_api.get_movie_reviews(
            movie_id=movie_id,
            expected_status=200
        )
        response_data = response.json()

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert isinstance(response_data, list), "Ответ должен содержать список отзывов"

    # ТЕСТЫ ДЛЯ POST /movies/{movieId}/reviews
    def test_create_review_success(self, common_user, create_movie, review_data):
        """
        Успешное создание отзыва авторизованным пользователем.
        Роли: USER, ADMIN, SUPER_ADMIN
        Статус-код: 201
        """
        movie_id = create_movie

        response = common_user.api.reviews_api.create_review(
            movie_id=movie_id,
            review_data=review_data,
            expected_status=201
        )
        response_data = response.json()

        assert response.status_code == 201, f"Ожидался статус 201 или 404, получен {response.status_code}"
        assert "userId" in response_data, "Ответ должен содержать ID созданного отзыва"
        assert response_data["text"] == review_data["text"], "Текст отзыва должен совпадать"
        assert response_data["rating"] == review_data["rating"], "Рейтинг должен совпадать"

        if response.status_code == 404:
            assert "message" in response_data, "Ответ должен содержать сообщение об ошибке"

    # ТЕСТЫ ДЛЯ PUT /movies/{movieId}/reviews
    def test_update_review_success(self, common_user, create_movie, review_data):
        """
        Успешное редактирование отзыва.
        Роли: USER, ADMIN, SUPER_ADMIN
        """
        movie_id = create_movie

        # Сначала создаем отзыв
        create_response = common_user.api.reviews_api.create_review(
            movie_id=movie_id,
            review_data=review_data,
            expected_status=201
        )

        assert create_response.status_code == 201, "Отзыв должен быть создан для последующего редактирования"

        # Редактируем отзыв
        updated_review_data = {
            "rating": global_faker.random_int(min=1, max=5),
            "text": f"Обновленный тестовый отзыв - {global_faker.text(max_nb_chars=50)}",
        }

        response = common_user.api.reviews_api.update_review(
            movie_id=movie_id,
            review_data=updated_review_data,
            expected_status=200
        )
        response_data = response.json()

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert response_data["text"] == updated_review_data["text"], "Текст отзыва должен быть обновлен"
        assert response_data["rating"] == updated_review_data["rating"], "Рейтинг должен быть обновлен"

    # ТЕСТЫ ДЛЯ PATCH /movies/{movieId}/reviews/hide/{userId}

    def test_hide_review_success(self, super_admin, create_movie, review_data):
        """
        Успешное скрытие отзыва. Роли: ADMIN, SUPER_ADMIN
        """
        movie_id = create_movie

        # Создаем пользователя и отзыв
        create_response = super_admin.api.reviews_api.create_review(
            movie_id=movie_id,
            review_data=review_data,
            expected_status=201
        )

        created_review = create_response.json()
        user_id = created_review.get("userId")

        # Скрываем отзыв
        response = super_admin.api.reviews_api.hide_review(
            movie_id=movie_id,
            user_id=user_id,
            expected_status=200
        )

        assert response.status_code == 200, f"Ожидался статус 200 или 404, получен {response.status_code}"

    # ТЕСТЫ ДЛЯ PATCH /movies/{movieId}/reviews/show/{userId}

    def test_show_review_success(self, super_admin, create_movie, review_data):
        """
        Успешный показ отзыва. Роли: ADMIN, SUPER_ADMIN
        """
        movie_id = create_movie

        # Создаем пользователя и отзыв
        create_response = super_admin.api.reviews_api.create_review(
            movie_id=movie_id,
            review_data=review_data,
            expected_status=201
        )

        created_review = create_response.json()
        user_id = created_review.get("userId")

        # Показываем отзыв
        response = super_admin.api.reviews_api.show_review(
            movie_id=movie_id,
            user_id=user_id,
            expected_status=200
        )

        assert response.status_code == 200, f"Ожидался статус 200 или 404, получен {response.status_code}"

    # НЕГАТИВНЫЕ ТЕСТЫ
    # ТЕСТЫ ДЛЯ GET /movies/{movieId}/reviews
    @pytest.mark.negative
    def test_get_movie_reviews_not_found(self, api_manager: ApiManager):
        """
        Получение отзывов для несуществующего фильма.
        """
        nonexistent_movie_id = global_faker.random_number(digits=6, fix_len=True)

        response = api_manager.reviews_api.get_movie_reviews(
            movie_id=nonexistent_movie_id,
            expected_status=404
        )

        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"

    # ТЕСТЫ ДЛЯ POST /movies/{movieId}/reviews
    @pytest.mark.negative
    def test_create_review_unauthorized(self, api_manager: ApiManager, create_movie, review_data):
        """
        Создание отзыва неавторизованным пользователем.
        """
        movie_id = create_movie

        response = api_manager.reviews_api.create_review(
            movie_id=movie_id,
            review_data=review_data,
            expected_status=401
        )

        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

    @pytest.mark.negative
    def test_create_review_movie_not_found(self, common_user, review_data):
        """
        Создание отзыва для несуществующего фильма.
        """
        fake_movie_id = global_faker.random_number(digits=6, fix_len=True)

        response = common_user.api.reviews_api.create_review(
            movie_id=fake_movie_id,
            review_data=review_data,
            expected_status=404
        )

        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"

    @pytest.mark.negative
    def test_create_review_bad_request(self, common_user, create_movie):
        """
        Создание отзыва с некорректными данными.
        """
        movie_id = create_movie
        invalid_review_data = {
            "reviewText": "",  # Пустой текст отзыва
            "rating": global_faker.random_int(min=6, max=10)  # Некорректный рейтинг (должен быть 1-5)
        }

        response = common_user.api.reviews_api.create_review(
            movie_id=movie_id,
            review_data=invalid_review_data,
            expected_status=404
        )

        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"

    @pytest.mark.negative
    def test_create_review_conflict(self, common_user, create_movie, review_data):
        """
        Попытка создания дублирующего отзыва.
        Статус-код: 409 - Вы уже оставили отзыв к этому фильму или 404 (если API не реализован)
        """
        movie_id = create_movie

        # Создаем первый отзыв
        first_response = common_user.api.reviews_api.create_review(
            movie_id=movie_id,
            review_data=review_data,
            expected_status=201
        )

        assert first_response.status_code == 201, "Первый отзыв должен быть создан успешно"

        # Пытаемся создать второй отзыв для того же фильма
        response = common_user.api.reviews_api.create_review(
            movie_id=movie_id,
            review_data=review_data,
            expected_status=409
        )

        assert response.status_code == 409, f"Ожидался статус 409 или 404, получен {response.status_code}"

    # ТЕСТЫ ДЛЯ PUT /movies/{movieId}/reviews
    @pytest.mark.negative
    def test_update_review_unauthorized(self, api_manager: ApiManager, create_movie, review_data):
        """
        Редактирование отзыва неавторизованным пользователем.
        """
        movie_id = create_movie

        response = api_manager.reviews_api.update_review(
            movie_id=movie_id,
            review_data=review_data,
            expected_status=401
        )

        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

    @pytest.mark.negative
    def test_update_review_not_found(self, common_user, review_data):
        """
        Редактирование отзыва для несуществующего фильма.
        """
        nonexistent_movie_id = global_faker.random_number(digits=6, fix_len=True)

        response = common_user.api.reviews_api.update_review(
            movie_id=nonexistent_movie_id,
            review_data=review_data,
            expected_status=404
        )

        assert response.status_code == 404, f"Ожидался статус 404 или 400, получен {response.status_code}"
