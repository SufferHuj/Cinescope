"""
Модель платежа для работы с базой данных.
Содержит SQLAlchemy модель для таблицы payments.
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import declarative_base
from typing import Dict, Any
import enum

Base = declarative_base()


class PaymentStatus(enum.Enum):
    """
    Перечисление статусов платежа.
    
    Соответствует типу public."Status" в базе данных.
    """
    SUCCESS = "SUCCESS"
    INVALID_CARD = "INVALID_CARD"
    ERROR = "ERROR"


class PaymentDBModel(Base):
    """
    Модель платежа в БД.
    
    Представляет таблицу payments в базе данных PostgreSQL.
    Содержит все необходимые поля для хранения информации о платежах за фильмы.
    
    Attributes:
        id (int): Уникальный идентификатор платежа (автоинкремент)
        user_id (str): ID пользователя, совершившего платеж
        movie_id (int): ID фильма, за который произведен платеж
        status (PaymentStatus): Статус платежа (SUCCESS, INVALID_CARD, ERROR)
        amount (int): Сумма платежа в копейках
        total (int): Общая сумма платежа в копейках
        created_at (datetime): Дата и время создания платежа
    """

    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)  # serial4 в БД
    user_id = Column(String, nullable=False)  # text в БД
    movie_id = Column(Integer, nullable=False)  # int4 в БД
    status = Column(Enum(PaymentStatus), nullable=False)  # public."Status" в БД
    amount = Column(Integer, nullable=False)  # int4 в БД
    total = Column(Integer, nullable=False)  # int4 в БД
    created_at = Column(DateTime, nullable=False)  # timestamp(3) в БД

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование объекта платежа в словарь.
        
        Returns:
            Dict[str, Any]: Словарь с данными платежа для сериализации
        """
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'status': self.status.value if self.status else None,
            'amount': self.amount,
            'total': self.total,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        """
        Строковое представление объекта платежа для отладки.
        
        Returns:
            str: Строковое представление с основными атрибутами платежа
        """
        return f"<Payment(id='{self.id}', user_id='{self.user_id}', movie_id='{self.movie_id}', status='{self.status}', total='{self.total}')>"