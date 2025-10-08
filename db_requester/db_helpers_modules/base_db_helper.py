from typing import List, Union
from sqlalchemy.orm import Session
from db_models.db_user_model import UserDBModel
from db_models.db_movie_model import MovieDBModel
from db_models.db_genre_model import GenreDBModel
from db_models.db_review_model import ReviewDBModel
from db_models.db_payment_model import PaymentDBModel


class BaseDBHelper:
    """ Базовый класс для всех доменных хелперов базы данных """
    
    def __init__(self, db_session: Session):
        """Инициализация базового хелпера с сессией базы данных"""

        self.db_session = db_session

    # ==================== ОБЩИЕ МЕТОДЫ ====================
    
    def cleanup_test_data(self, objects_to_delete: List[Union[UserDBModel, MovieDBModel, GenreDBModel, ReviewDBModel, PaymentDBModel]]) -> None:
        """Очищает тестовые данные из базы данных после тестов"""

        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    def get_total_movies_count(self) -> int:
        """Получает общее количество фильмов в базе данных"""

        return self.db_session.query(MovieDBModel).count()

    def get_total_users_count(self) -> int:
        """Получает общее количество пользователей в базе данных"""
        
        return self.db_session.query(UserDBModel).count()