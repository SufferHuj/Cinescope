""" Модель отзыва для работы с базой данных """

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()


class ReviewDBModel(Base):
    """ Модель отзыва в БД """

    __tablename__ = 'reviews'

    movie_id = Column(Integer, primary_key=True)  # int4 в БД
    user_id = Column(String, primary_key=True)  # text в БД
    hidden = Column(Boolean, default=False)  # bool в БД
    text = Column(Text)  # text в БД
    rating = Column(Integer)  # int4 в БД
    created_at = Column(DateTime)  # timestamp(3) в БД

    def to_dict(self) -> Dict[str, Any]:
        """ Преобразование объекта отзыва в словарь. Returns: Словарь с данными отзыва для сериализации """
        
        return {
            'movie_id': self.movie_id,
            'user_id': self.user_id,
            'hidden': self.hidden,
            'text': self.text,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        """ Строковое представление объекта отзыва для отладки """

        return f"<Review(movie_id='{self.movie_id}', user_id='{self.user_id}', rating='{self.rating}', hidden='{self.hidden}')>"