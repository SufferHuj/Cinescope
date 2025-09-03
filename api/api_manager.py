from api.auth_api import AuthAPI
from api.user_api import UserAPI
from api.movies_api import MoviesAPI
from api.genres_api import GenresAPI
from api.reviews_api import ReviewsAPI


class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией
    """

    def __init__(self, session):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """

        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesAPI(session)
        self.genres_api = GenresAPI(session)
        self.reviews_api = ReviewsAPI(session)

    def close_session(self):
        self.session.close()
