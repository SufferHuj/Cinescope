from custom_requester.custom_requester import CustomRequester
from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT, BASE_URL # ИЗМЕНЕНО: Импортируем BASE_URL

class AuthAPI(CustomRequester):

    """
    Класс для работы с аутентификацией
    """

    # ИЗМЕНЕНО: Конструктор теперь принимает base_url
    def __init__(self, session, base_url):
        # ИЗМЕНЕНО: Используем переданный base_url, а не хардкод
        super().__init__(session=session, base_url=base_url)

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

    def login_user(self, login_data, expected_status = 200):
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

    def authenticate(self, user_cards):

        login_data = {
            "email": user_cards[0],
            "password": user_cards[1]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self._update_session_headers(**{"authorization": "Bearer" + token})