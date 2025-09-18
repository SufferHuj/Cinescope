import pytest

from resources.test_card_data import TestCardData
from utils.data_generator import faker as global_faker
from api.api_manager import ApiManager


class TestPaymentAPI:
    """
    Класс тестов для API платежей.
    
    Включает позитивные и негативные тесты для создания платежей,
    получения истории платежей пользователей и валидации данных карт.
    """

    # ПОЗИТИВНЫЕ ТЕСТЫ
    # ТЕСТЫ ДЛЯ POST/create
    def test_create_payment_success_with_correct_data(self, common_user, payment_request_data):
        """
        Проверка успешного создания платежа с корректными данными
        """
        response = common_user.api.payment_api.create_payment(
            payment_request_data=payment_request_data,
            expected_status=201
        )

        response_data = response.json()

        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "status" in response_data, "Ответ должен содержать статус платежа"
        assert response_data["status"] == "SUCCESS", "Статус платежа должен быть SUCCESS"

    # ТЕСТЫ GET /user/{user_id} - получение платежей пользователя по ID
    @pytest.mark.parametrize('general_user,expected_code', [
        ("super_admin", 200),
        ("admin", 200)],
                             indirect=['general_user'],
                             ids=["super_admin_access", "admin_access"])
    def test_get_user_payments_by_id_success(self, general_user, expected_code):
        """
        Получение платежей пользователя по ID для ролей ADMIN и SUPER_ADMIN
        """

        # Получаем ID текущего пользователя
        user_response = general_user.api.user_api.get_user(general_user.email)
        user_id = user_response.json()["id"]

        response = general_user.api.payment_api.get_user_payments_by_id(
            user_id=user_id,
            expected_status=expected_code
        )

        response_data = response.json()

        assert response.status_code == expected_code, f"Ожидался статус {expected_code}, получен {response.status_code}"
        assert isinstance(response_data, list), "Ответ должен содержать список платежей"

    # ТЕСТЫ ДЛЯ GET /user
    @pytest.mark.skip(reason="Тест под админом падает с 403")
    @pytest.mark.parametrize("general_user, expected_code", [
        ("super_admin", 200),
        ("admin", 200),
        ("common_user", 200)],
                             indirect=['general_user'],
                             ids=["super_admin", "admin", "common_user"])
    def test_create_user_payments_success(self, general_user, expected_code):
        """
        Проверка получения списка платежей для пользователей
        general_user: Фикстура пользователя с определенной ролью (через indirect)
        """

        response = general_user.api.payment_api.get_user_payments(expected_status=expected_code)
        response_data = response.json()

        assert response.status_code == 200, f"Ожидался статус код 200, получен {response.status_code}"
        assert isinstance(response_data, list), "Ответ должен быть списком платежей"

    # ТЕСТЫ GET /find-all
    @pytest.mark.parametrize('general_user, page, page_size, status, created_at, expected_code', [
        ("super_admin", 1, 10, "SUCCESS", "desc", 200),
        ("admin", 1, 10, "SUCCESS", "asc", 200),
    ], indirect=['general_user'], ids=["super_admin_access", "admin_access"])
    def test_get_all_payments_success(self, general_user, page, page_size, status, created_at, expected_code):
        """
        Успешное получение всех платежей с пагинацией и фильтрацией.
        """

        response = general_user.api.payment_api.get_find_all_user_payments(
            page=page,
            page_size=page_size,
            status=status,
            created_at=created_at,
            expected_status=expected_code
        )

        response_data = response.json()

        assert response.status_code == expected_code, f"Ожидался статус {expected_code}, получен {response.status_code}"
        assert 'payments' in response_data, "В ответе должен быть ключ 'payments'"
        assert 'count' in response_data, "В ответе должен быть ключ 'count'"
        assert 'page' in response_data, "В ответе должен быть ключ 'page'"
        assert 'pageSize' in response_data, "В ответе должен быть ключ 'pageSize'"
        assert 'pageCount' in response_data, "В ответе должен быть ключ 'pageCount'"

    # НЕГАТИВНЫЕ ТЕСТЫ
    # ТЕСТЫ ДЛЯ POST/create
    @pytest.mark.negative
    def test_create_payment_invalid_card(self, common_user, payment_request_data):
        """
        Попытка оплаты неверным номером карты (INVALID_CARD)
        """

        invalid_payment_data = payment_request_data.copy()
        invalid_payment_data["card"] = invalid_payment_data["card"].copy()
        invalid_payment_data["card"]["cardNumber"] = global_faker.random_number(digits=16)  # Невалидный номер

        response = common_user.api.payment_api.create_payment(
            payment_request_data=invalid_payment_data,
            expected_status=400
        )

        assert response.status_code == 400

    @pytest.mark.negative
    def test_create_payment_unauthorized(self, api_manager: ApiManager, payment_request_data):
        """
        Проверка оплаты создания платежа без авторизации
        """

        response = api_manager.payment_api.create_payment(
            payment_request_data=payment_request_data,
            expected_status=401
        )

        assert response.status_code == 401

    @pytest.mark.negative
    def test_create_payment_nonexistent_movie(self, common_user):
        """
        Проверка оплаты несуществующего фильма
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

    # ТЕСТЫ ДЛЯ GET /user/{user_id}
    @pytest.mark.negative
    def test_get_user_payments_by_id_forbidden_user_role(self, common_user, super_admin):
        """
        Проверка запрета доступа для роли USER к платежам (даже к своим собственным)
        """

        user_response = super_admin.api.user_api.get_user(common_user.email)
        common_user_id = user_response.json()["id"]

        response = common_user.api.payment_api.get_user_payments_by_id(
            user_id=common_user_id,
            expected_status=403
        )

        assert response.status_code == 403

    @pytest.mark.negative
    def test_get_user_payments_by_id_nonexistent_user(self, super_admin):
        """
        Проверка ошибки при запросе платежей несуществующего пользователя
        """

        fake_user_id = global_faker.uuid4()

        response = super_admin.api.payment_api.get_user_payments_by_id(
            user_id=fake_user_id,
            expected_status=404
        )

        assert response.status_code == 404

    @pytest.mark.negative
    def test_get_user_payments_by_id_unauthorized(self, api_manager: ApiManager):
        """
        Проверка ошибки при отсутствии авторизации
        """

        fake_user_id = global_faker.uuid4()

        response = api_manager.payment_api.get_user_payments_by_id(
            user_id=fake_user_id,
            expected_status=401
        )

        assert response.status_code == 401

    @pytest.mark.negative
    def test_get_user_payments_by_id_invalid_format(self, super_admin):
        """
        Проверка ошибки при невалидном формате ID пользователя
        """

        invalid_user_id = global_faker.pystr(min_chars=10, max_chars=20)

        response = super_admin.api.payment_api.get_user_payments_by_id(
            user_id=invalid_user_id,
            expected_status=404
        )

        assert response.status_code == 404

    # ТЕСТЫ ДЛЯ GET /user
    @pytest.mark.negative
    def test_get_user_payments_unauthorized(self, api_manager: ApiManager):
        """
        Проверка получения списка платежей без авторизации
        """

        response = api_manager.payment_api.get_user_payments(expected_status=401)

        assert response.status_code == 401

    # ТЕСТЫ GET /find-all
    @pytest.mark.negative
    @pytest.mark.skip(reason="Тест с невалидным размером страницы и невалидным порядком сортировки отдают 200")
    @pytest.mark.parametrize('page, page_size, status, created_at, expected_code', [
        (0, 10, "SUCCESS", "asc", 400),  # Невалидный номер страницы
        (1, 0, "SUCCESS", "asc", 400),  # Невалидный размер страницы
        (1, 10, "INVALID", "asc", 400),  # Невалидный статус
        (1, 10, "SUCCESS", "inv", 400),  # Невалидный порядок сортировки
    ])
    def test_get_find_all_user_payments_invalid_params(self, super_admin, page, page_size, status, created_at,
                                                       expected_code):
        """
        Проверки получения всех платежей с невалидными параметрами
        """

        response = super_admin.api.payment_api.get_find_all_user_payments(
            page=page,
            page_size=page_size,
            status=status,
            created_at=created_at,
            expected_status=expected_code
        )

        assert response.status_code == expected_code, f"Ожидался статус {expected_code}, получен {response.status_code}"

    @pytest.mark.negative
    def test_get_find_all_user_payments_negative(self, common_user):
        """
        Проверка ограничения доступа для пользователей без прав администратора
        """

        response = common_user.api.payment_api.get_find_all_user_payments(
            page=1,
            page_size=10,
            status="SUCCESS",
            created_at="asc",
            expected_status=403
        )
        response_data = response.json()

        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
        assert "error" in response_data, "Ответ должен содержать сообщение об ошибке"
        assert response_data["message"] == "Forbidden resource", "Ответ должен содержать причину ошибки"

    @pytest.mark.negative
    def test_get_find_all_user_payments_unauthorized(self, api_manager: ApiManager):
        """
        Проверка получения всех платежей без авторизации
        """

        response = api_manager.payment_api.get_find_all_user_payments(
            page=1,
            page_size=10,
            status="SUCCESS",
            created_at="asc",
            expected_status=401
        )

        assert response.status_code == 401
