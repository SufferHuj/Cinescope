""" Модель платежа для работы с базой данных """

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import declarative_base
from typing import Dict, Any
from constants import PaymentStatus

Base = declarative_base()


class PaymentDBModel(Base):
    """ Модель платежа в БД """

    __tablename__ = 'payments'
    __mapper_args__ = {'confirm_deleted_rows': False}

    id = Column(Integer, primary_key=True, autoincrement=True)  # serial4 в БД
    user_id = Column(String, nullable=False)  # text в БД
    movie_id = Column(Integer, nullable=False)  # int4 в БД
    status = Column(Enum(PaymentStatus), nullable=False)  # public."Status" в БД
    amount = Column(Integer, nullable=False)  # int4 в БД
    total = Column(Integer, nullable=False)  # int4 в БД
    created_at = Column(DateTime, nullable=False)  # timestamp(3) в БД

    def to_dict(self) -> Dict[str, Any]:
        """ Преобразование объекта платежа в словарь. Returns: Словарь с данными платежа для сериализации """
        
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
        """ Строковое представление объекта платежа для отладки """

        return f"<Payment(id='{self.id}', user_id='{self.user_id}', movie_id='{self.movie_id}', status='{self.status}', total='{self.total}')>"