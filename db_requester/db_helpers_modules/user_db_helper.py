from typing import Optional, Union
from sqlalchemy.orm import Session
from db_models.db_user_model import UserDBModel
from .base_db_helper import BaseDBHelper


class UserDBHelper(BaseDBHelper):
    """ Хелпер для работы с пользователями в базе данных """
    
    def __init__(self, db_session: Session):
        """Инициализация хелпера пользователей"""

        super().__init__(db_session)

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ПОЛЬЗОВАТЕЛЯМИ ====================
    
    def create_test_user(self, user_data: dict) -> UserDBModel:
        """Создает тестового пользователя в базе данных"""

        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: Union[str, int]) -> Optional[UserDBModel]:
        """Получает пользователя по ID"""

        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[UserDBModel]:
        """Получает пользователя по email"""

        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).first()

    def user_exists_by_email(self, email: str) -> bool:
        """Проверяет существование пользователя по email"""

        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).count() > 0

    def delete_user(self, user: UserDBModel) -> None:
        """Удаляет пользователя из базы данных"""
        
        self.db_session.delete(user)
        self.db_session.commit()