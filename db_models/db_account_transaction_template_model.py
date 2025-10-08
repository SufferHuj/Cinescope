""" Модель шаблона транзакций счетов для работы с базой данных """

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()

class AccountTransactionTemplate(Base):
    """ Модель шаблона транзакций счетов в БД """

    __tablename__ = 'accounts_transaction_template'
    
    user = Column(String, primary_key=True, comment="Имя пользователя (первичный ключ)")
    balance = Column(Integer, nullable=False, comment="Баланс пользователя")

    def to_dict(self) -> Dict[str, Any]:
        """ Преобразование объекта шаблона транзакций в словарь. Returns: Словарь с данными шаблона для сериализации """
        
        return {
            'user': self.user,
            'balance': self.balance
        }

    def __repr__(self) -> str:
        """ Строковое представление объекта шаблона транзакций для отладки """

        return f"<AccountTransactionTemplate(user='{self.user}', balance={self.balance})>"
        