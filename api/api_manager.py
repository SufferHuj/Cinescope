from api.auth_api import AuthAPI
from api.user_api import UserAPI
from api.movies_api import MoviesAPI
from constants import BASE_URL, MOVIES_API_BASE_URL

class ApiManager:

    """
    Класс для управления API-классами с единой HTTP-сессией
    """

    # ИЗМЕНЕНО: Добавляем base_url в конструктор ApiManager
    def __init__(self, session):

        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """

        self.session = session
        # ИЗМЕНЕНО: Передаем BASE_URL в конструкторы AuthAPI и UserAPI, MOVIES_API_BASE_URL в MoviesAPI
        self.auth_api = AuthAPI(session, BASE_URL)
        self.user_api = UserAPI(session, BASE_URL)
        self.movies_api = MoviesAPI(session, MOVIES_API_BASE_URL)