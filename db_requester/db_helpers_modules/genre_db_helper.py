from typing import Optional, Union
from sqlalchemy.orm import Session
from db_models.db_genre_model import GenreDBModel
from .base_db_helper import BaseDBHelper


class GenreDBHelper(BaseDBHelper):
    """ Хелпер для работы с жанрами """
    
    def __init__(self, db_session: Session):
        """Инициализация хелпера жанров"""

        super().__init__(db_session)

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ЖАНРАМИ ====================
    
    def create_test_genre(self, genre_data: dict) -> GenreDBModel:
        """Создает тестовый жанр в базе данных"""

        genre = GenreDBModel(**genre_data)
        self.db_session.add(genre)
        self.db_session.commit()
        self.db_session.refresh(genre)
        return genre

    def get_genre_by_id(self, genre_id: Union[str, int]) -> Optional[GenreDBModel]:
        """Получает жанр по ID"""

        return self.db_session.query(GenreDBModel).filter(GenreDBModel.id == genre_id).first()

    def get_genre_by_name(self, name: str) -> Optional[GenreDBModel]:
        """Получает жанр по названию"""

        return self.db_session.query(GenreDBModel).filter(GenreDBModel.name == name).first()

    def genre_exists_by_name(self, name: str) -> bool:
        """Проверяет существование жанра по названию"""

        return self.db_session.query(GenreDBModel).filter(GenreDBModel.name == name).first() is not None

    def delete_genre(self, genre: GenreDBModel) -> None:
        """Удаляет жанр из базы данных"""
        
        self.db_session.delete(genre)
        self.db_session.commit()