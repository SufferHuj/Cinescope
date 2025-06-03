from custom_requester.custom_requester import CustomRequester
from constants import REGISTER_ENDPOINT, BASE_URL, LOGIN_ENDPOINT


class AuthAPI(CustomRequester):

    """
    Класс для работы с аутентификацией
    """

    def __init__(self, session):

        super().__init__(session= session, base_url= BASE_URL)

    def register_user(self, user_data, expected_status = 201):

        """
        Регистрация нового пользователя
        user_data: данные пользователя
        expected_status: ожидаемый статус-код
        """
        return self.send_request(
            method= "POST",
            endpoint= REGISTER_ENDPOINT,
            data= user_data,
            expected_status= expected_status
        )

    def login_user(self, login_data, expected_status = 201):

        """
        Авторизация пользователя.
        login_data: Данные для логина.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )