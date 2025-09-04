import pytest
from api.api_manager import ApiManager
from resources.test_card_data import TestCardData
from utils.data_generator import faker as global_faker


class TestPaymentAPI:
    """
    Тесты для Payment API
    """

    # ПОЗИТИВНЫЕ ТЕСТЫ
    # ТЕСТЫ ДЛЯ POST/create
    @pytest.mark.skip(reason="Отдает 503")
    def test_create_payment_success_with_correct_data(self, common_user, payment_request_data):
        """
        1. Успешное создание платежа с корректными данными.
        Статус-код: 201
        """
        response = common_user.api.payment_api.create_payment(
            payment_request_data=payment_request_data,
            expected_status=201
        )

        response_data = response.json()

        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "status" in response_data, "Ответ должен содержать статус платежа"
        assert response_data["status"] == "SUCCESS", f"Статус платежа должен быть SUCCESS"

    # НЕГАТИВНЫЕ ТЕСТЫ
    # ТЕСТЫ ДЛЯ POST/create
    @pytest.mark.skip(reason="Отдает 503")
    @pytest.mark.negative
    def test_create_payment_invalid_card(self, common_user, payment_request_data):
        """
        2. Ошибка при неверном номере карты (INVALID_CARD).
        Статус-код: 400
        """
        # Модифицируем данные карты для негативного теста
        invalid_payment_data = payment_request_data.copy()
        invalid_payment_data["card"] = invalid_payment_data["card"].copy()
        invalid_payment_data["card"]["cardNumber"] = "1234567890123456"  # Невалидный номер

        response = common_user.api.payment_api.create_payment(
            payment_request_data=invalid_payment_data,
            expected_status=400
        )

        assert response.status_code == 400

    @pytest.mark.negative
    def test_create_payment_unauthorized(self, api_manager: ApiManager, payment_request_data):
        """
        3. Ошибка при попытке создания платежа без авторизации.
        Статус-код: 401
        """
        response = api_manager.payment_api.create_payment(
            payment_request_data=payment_request_data,
            expected_status=401
        )

        assert response.status_code == 401

    @pytest.mark.negative
    def test_create_payment_nonexistent_movie(self, common_user):
        """
        4. Ошибка при попытке оплаты несуществующего фильма.
        Статус-код: 404
        """
        fake_movie_id = global_faker.random_number(digits=6, fix_len=True)

        payment_request_data = {
            "movieId": fake_movie_id,
            "amount": global_faker.random_int(min=100, max=10000),
            "card": TestCardData.CARD_DATA
        }

        response = common_user.api.payment_api.create_payment(
            payment_request_data=payment_request_data,
            expected_status=404
        )

        assert response.status_code == 404
