from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()

class AccountTransactionTemplate(Base):
    """
    Модель для таблицы accounts_transaction_template.
    
    Представляет шаблон транзакций счетов с балансом пользователей.
    """

    __tablename__ = 'accounts_transaction_template'
    
    user = Column(String, primary_key=True, comment="Имя пользователя (первичный ключ)")
    balance = Column(Integer, nullable=False, comment="Баланс пользователя")

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует объект в словарь.
        
        Returns:
            Dict[str, Any]: Словарь с данными объекта
        """
        return {
            'user': self.user,
            'balance': self.balance
        }

    def __repr__(self) -> str:
        """
        Строковое представление объекта
        """
        return f"<AccountTransactionTemplate(user='{self.user}', balance={self.balance})>"
        