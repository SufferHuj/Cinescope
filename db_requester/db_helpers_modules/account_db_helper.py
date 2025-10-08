from typing import List, Optional
from sqlalchemy.orm import Session
from db_models.db_account_transaction_template_model import AccountTransactionTemplate
from .base_db_helper import BaseDBHelper


class AccountDBHelper(BaseDBHelper):
    """ Хелпер для работы с аккаунтами в базе данных """
    
    def __init__(self, db_session: Session):
        """Инициализация хелпера аккаунтов"""

        super().__init__(db_session)

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С АККАУНТАМИ ====================
    
    def create_test_account(self, user_name: str, balance: int) -> AccountTransactionTemplate:
        """Создает тестовый аккаунт в базе данных"""

        account = AccountTransactionTemplate(user=user_name, balance=balance)
        self.db_session.add(account)
        self.db_session.commit()
        return account
    
    def get_account_by_user(self, user_name: str) -> Optional[AccountTransactionTemplate]:
        """Получает аккаунт по имени пользователя"""

        return self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first()
    
    def account_exists_by_user(self, user_name: str) -> bool:
        """Проверяет существование аккаунта по имени пользователя"""

        return self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first() is not None
    
    def update_account_balance(self, user_name: str, new_balance: int) -> bool:
        """Обновляет баланс аккаунта"""

        account = self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first()
        if account:
            account.balance = new_balance
            self.db_session.commit()
        else:
            raise ValueError(f"Аккаунт с именем пользователя '{user_name}' не найден")
    
    def get_all_accounts(self) -> List[AccountTransactionTemplate]:
        """Получает все аккаунты из базы данных"""

        return self.db_session.query(AccountTransactionTemplate).all()
    
    def delete_account_by_user(self, user_name: str) -> bool:
        """Удаляет аккаунт по имени пользователя"""
        
        account = self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first()
        if account:
            self.db_session.delete(account)
            self.db_session.commit()
            return True
        return False