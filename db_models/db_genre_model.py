""" Модель жанра для работы с базой данных """

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()


class GenreDBModel(Base):
    """ Модель жанра в БД """

    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)  # serial4 в БД
    name = Column(String)  # text в БД

    def to_dict(self) -> Dict[str, Any]:
        """ Преобразование объекта жанра в словарь. Returns: Словарь с данными жанра для сериализации """
        
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        """ Строковое представление объекта жанра для отладки """

        return f"<Genre(id='{self.id}', name='{self.name}')>"