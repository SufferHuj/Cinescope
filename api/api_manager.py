from api.auth_api import AuthAPI
from api.user_api import UserAPI

class ApiManager:

    """
    Класс для управления API-классами с единой HTTP-сессией.
    """

    # ИЗМЕНЕНО: Добавляем base_url в конструктор ApiManager
    def __init__(self, session, base_url):

        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        :param base_url: Базовый URL для всех API-классов.
        """

        self.session = session
        # ИЗМЕНЕНО: Передаем base_url в конструкторы AuthAPI и UserAPI
        self.auth_api = AuthAPI(session, base_url)
        self.user_api = UserAPI(session, base_url)