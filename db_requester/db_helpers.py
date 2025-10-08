from sqlalchemy.orm import Session
from .db_helpers_modules.base_db_helper import BaseDBHelper
from .db_helpers_modules.user_db_helper import UserDBHelper
from .db_helpers_modules.movie_db_helper import MovieDBHelper
from .db_helpers_modules.genre_db_helper import GenreDBHelper
from .db_helpers_modules.account_db_helper import AccountDBHelper
from .db_helpers_modules.review_db_helper import ReviewDBHelper
from .db_helpers_modules.payment_db_helper import PaymentDBHelper


class DBHelper:
    """ Главный класс-помощник для работы с БД в тестах """
    
    def __init__(self, db_session: Session):
        """Инициализация DBHelper с сессией базы данных и всеми доменными хелперами"""

        self.db_session = db_session  # Сессия SQLAlchemy для работы с БД
        
        # Инициализация доменных хелперов
        self.users = UserDBHelper(db_session)  # Хелпер для работы с пользователями
        self.movies = MovieDBHelper(db_session)  # Хелпер для работы с фильмами
        self.genres = GenreDBHelper(db_session)  # Хелпер для работы с жанрами
        self.accounts = AccountDBHelper(db_session)  # Хелпер для работы с аккаунтами
        self.reviews = ReviewDBHelper(db_session)  # Хелпер для работы с отзывами
        self.payments = PaymentDBHelper(db_session)  # Хелпер для работы с платежами
        
        # Базовый хелпер для общих методов
        self._base = BaseDBHelper(db_session)

    # ==================== ОБЩИЕ МЕТОДЫ (делегирование к базовому хелперу) ====================
    
    def cleanup_test_data(self, objects_to_delete):
        """Очищает тестовые данные из базы данных после тестов"""

        return self._base.cleanup_test_data(objects_to_delete)

    def get_total_movies_count(self):
        """Получает общее количество фильмов в базе данных"""

        return self._base.get_total_movies_count()

    def get_total_users_count(self):
        """Получает общее количество пользователей в базе данных"""
        
        return self._base.get_total_users_count()
