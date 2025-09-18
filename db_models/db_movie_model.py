from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()


class MovieDBModel(Base):
    """
    Модель фильма в БД.
    
    Представляет таблицу movies в базе данных PostgreSQL.
    Содержит все необходимые поля для хранения информации о фильмах.
    
    Attributes:
        id (int): Уникальный идентификатор фильма
        name (str): Название фильма
        price (int): Цена фильма в копейках
        description (str): Описание фильма
        image_url (str): URL изображения фильма
        location (str): Местоположение показа
        published (bool): Статус публикации фильма
        rating (float): Рейтинг фильма
        genre_id (int): ID жанра фильма
        created_at (datetime): Дата и время создания записи
    """

    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)  # int в БД
    name = Column(String)  # text в БД
    price = Column(Integer)  # int в БД
    description = Column(Text)  # text в БД
    image_url = Column(String)  # text в БД
    location = Column(String)  # text в БД
    published = Column(Boolean)  # bool в БД
    rating = Column(Float)  # float в БД
    genre_id = Column(Integer)  # int в БД
    created_at = Column(DateTime)  # timestamp в БД

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование объекта фильма в словарь.
        
        Returns:
            Dict[str, Any]: Словарь с данными фильма для сериализации
        """

        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'image_url': self.image_url,
            'location': self.location,
            'published': self.published,
            'rating': self.rating,
            'genre_id': self.genre_id,
            'created_at': self.created_at
        }

    def __repr__(self):
        """
        Строковое представление объекта фильма для отладки.
        
        Returns:
            str: Строковое представление с основными атрибутами фильма
        """
        return f"<Movie(id='{self.id}', name='{self.name}', price={self.price})>"
