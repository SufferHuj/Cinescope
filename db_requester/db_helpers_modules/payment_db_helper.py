from typing import Optional
from sqlalchemy.orm import Session
from db_models.db_payment_model import PaymentDBModel
from .base_db_helper import BaseDBHelper


class PaymentDBHelper(BaseDBHelper):
    """Хелпер для работы с платежами """
    
    def __init__(self, db_session: Session):
        """Инициализация хелпера платежей"""

        super().__init__(db_session)

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ПЛАТЕЖАМИ ====================
    
    def create_test_payment(self, payment_data: dict) -> PaymentDBModel:
        """Создает тестовый платеж в базе данных"""

        payment = PaymentDBModel(**payment_data)
        self.db_session.add(payment)
        self.db_session.commit()
        self.db_session.refresh(payment)
        return payment

    def get_payment_by_id(self, payment_id: int) -> Optional[PaymentDBModel]:
        """Получает платеж по ID"""

        return self.db_session.query(PaymentDBModel).filter(PaymentDBModel.id == payment_id).first()

    def delete_payment(self, payment: PaymentDBModel) -> None:
        """Удаляет платеж из базы данных"""
        
        self.db_session.delete(payment)
        self.db_session.commit()