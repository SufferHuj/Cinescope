"""
Модель пользователя для работы с базой данных.
Содержит SQLAlchemy модель для таблицы users.
"""

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()


class UserDBModel(Base):
    """
    Модель пользователя в БД.
    
    Представляет таблицу users в базе данных PostgreSQL.
    Содержит все необходимые поля для хранения информации о пользователях.
    
    Attributes:
        id (str): Уникальный идентификатор пользователя (UUID)
        email (str): Email адрес пользователя
        full_name (str): Полное имя пользователя
        password (str): Хэш пароля пользователя
        created_at (datetime): Дата и время создания аккаунта
        updated_at (datetime): Дата и время последнего обновления
        verified (bool): Статус верификации email
        banned (bool): Статус блокировки пользователя
        roles (str): Роли пользователя в системе
    """

    __tablename__ = 'users'

    id = Column(String, primary_key=True)  # text в БД
    email = Column(String)  # text в БД
    full_name = Column(String)  # text в БД
    password = Column(String)  # text в БД
    created_at = Column(DateTime)  # timestamp в БД
    updated_at = Column(DateTime)  # timestamp в БД
    verified = Column(Boolean)  # bool в БД
    banned = Column(Boolean)  # bool в БД
    roles = Column(String)  # text в БД (Role enum)

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование объекта пользователя в словарь.
        
        Returns:
            Dict[str, Any]: Словарь с данными пользователя для сериализации
        """
        
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'verified': self.verified,
            'banned': self.banned,
            'roles': self.roles
        }

    def __repr__(self):
        """
        Строковое представление объекта пользователя для отладки.
        
        Returns:
            str: Строковое представление с основными атрибутами пользователя
        """
        return f"<User(id='{self.id}', email='{self.email}')>"
