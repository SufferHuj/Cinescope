from typing import List, Optional, Union
from sqlalchemy.orm import Session
from db_models.db_movie_model import MovieDBModel
from .base_db_helper import BaseDBHelper


class MovieDBHelper(BaseDBHelper):
    """Хелпер для работы с фильмами """
    
    def __init__(self, db_session: Session):
        """Инициализация хелпера фильмов"""

        super().__init__(db_session)

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ФИЛЬМАМИ ====================
    
    def create_test_movie(self, movie_data: dict) -> MovieDBModel:
        """Создает тестовый фильм в базе данных"""

        movie = MovieDBModel(**movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return movie

    def get_movie_by_id(self, movie_id: Union[str, int]) -> Optional[MovieDBModel]:
        """Получает фильм по ID"""

        return self.db_session.query(MovieDBModel).filter(MovieDBModel.id == movie_id).first()

    def get_movie_by_name(self, name: str) -> Optional[MovieDBModel]:
        """Получает фильм по названию"""

        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == name).first()

    def movie_exists_by_name(self, name: str) -> bool:
        """Проверяет существование фильма по названию"""

        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == name).count() > 0

    def get_movies_by_genre(self, genre_id: int) -> List[MovieDBModel]:
        """Получает все фильмы определенного жанра"""

        return self.db_session.query(MovieDBModel).filter(MovieDBModel.genre_id == genre_id).all()

    def get_movies_by_price_range(self, min_price: int, max_price: int) -> List[MovieDBModel]:
        """Получает фильмы в указанном ценовом диапазоне"""

        return self.db_session.query(MovieDBModel).filter(
            MovieDBModel.price >= min_price,
            MovieDBModel.price <= max_price
        ).all()

    def delete_movie(self, movie: MovieDBModel) -> None:
        """Удаляет фильм из базы данных"""
        
        self.db_session.delete(movie)
        self.db_session.commit()