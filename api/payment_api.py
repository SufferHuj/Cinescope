from custom_requester.custom_requester import CustomRequester
from constants import PAYMENT_API_BASE_URL


class PaymentAPI(CustomRequester):
    """
    Класс для работы с API платежей.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=PAYMENT_API_BASE_URL)

    def create_payment(self, payment_request_data, expected_status=201):
        """
        Создание платежа.
        
        :param payment_request_data: Данные для создания платежа.
        :param expected_status: Ожидаемый статус-код (по умолчанию 201).
        :return: Объект ответа requests.Response.
        """

        return self.send_request(
            method="POST",
            endpoint="/create",
            data=payment_request_data,
            expected_status=expected_status
        )