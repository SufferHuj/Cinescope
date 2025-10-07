from custom_requester.custom_requester import CustomRequester
from constants import PAYMENT_API_BASE_URL


class PaymentAPI(CustomRequester):
    """ Класс для работы с API платежей """

    def __init__(self, session):
        """ Инициализация PaymentAPI """

        super().__init__(session=session, base_url=PAYMENT_API_BASE_URL)

    def create_payment(self, payment_request_data, expected_status=201):
        """ Создание платежа """

        return self.send_request(
            method="POST",
            endpoint="/create",
            data=payment_request_data,
            expected_status=expected_status
        )

    def get_user_payments(self, expected_status=200):
        """ Получение платежей текущего пользователя """

        return self.send_request(
            method="GET",
            endpoint="/user",
            expected_status=expected_status
        )

    def get_user_payments_by_id(self, user_id, expected_status=200):
        """ Получение платежей пользователя по ID """

        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    def get_find_all_user_payments(self, page=None, page_size=None, status=None, created_at=None, expected_status=200):
        """ Получение всех платежей пользователей с возможностью фильтрации """

        params = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['page_size'] = page_size
        if status is not None:
            params['status'] = status
        if created_at is not None:
            params['created_at'] = created_at

        return self.send_request(
            method="GET",
            endpoint="/find-all",
            params=params,
            expected_status=expected_status
        )
