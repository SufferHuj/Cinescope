from typing import List, Optional
from sqlalchemy.orm import Session
from db_models.db_review_model import ReviewDBModel
from .base_db_helper import BaseDBHelper


class ReviewDBHelper(BaseDBHelper):
    """Хелпер для работы с отзывами """
    
    def __init__(self, db_session: Session):
        """Инициализация хелпера отзывов"""

        super().__init__(db_session)

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ОТЗЫВАМИ ====================
    
    def create_test_review(self, review_data: dict) -> ReviewDBModel:
        """Создает тестовый отзыв в базе данных"""

        review = ReviewDBModel(**review_data)
        self.db_session.add(review)
        self.db_session.commit()
        self.db_session.refresh(review)
        return review

    def get_review_by_ids(self, movie_id: int, user_id: str) -> Optional[ReviewDBModel]:
        """Получает отзыв по ID фильма и ID пользователя"""

        return self.db_session.query(ReviewDBModel).filter(
            ReviewDBModel.movie_id == movie_id,
            ReviewDBModel.user_id == user_id
        ).first()

    def get_reviews_by_movie_id(self, movie_id: int) -> List[ReviewDBModel]:
        """Получает все отзывы для определенного фильма"""

        return self.db_session.query(ReviewDBModel).filter(ReviewDBModel.movie_id == movie_id).all()

    def review_exists_by_ids(self, movie_id: int, user_id: str) -> bool:
        """Проверяет существование отзыва по ID фильма и ID пользователя"""

        return self.db_session.query(ReviewDBModel).filter(
            ReviewDBModel.movie_id == movie_id,
            ReviewDBModel.user_id == user_id
        ).first() is not None

    def update_review_rating(self, movie_id: int, user_id: str, new_rating: int) -> bool:
        """Обновляет рейтинг отзыва"""

        review = self.get_review_by_ids(movie_id, user_id)
        if review:
            review.rating = new_rating
            self.db_session.commit()
            return True
        return False

    def update_review_text(self, movie_id: int, user_id: str, new_text: str) -> bool:
        """Обновляет текст отзыва"""

        review = self.get_review_by_ids(movie_id, user_id)
        if review:
            review.text = new_text
            self.db_session.commit()
            return True
        return False

    def hide_review(self, movie_id: int, user_id: str) -> bool:
        """Скрывает отзыв"""

        review = self.get_review_by_ids(movie_id, user_id)
        if review:
            review.hidden = True
            self.db_session.commit()
            return True
        return False

    def show_review(self, movie_id: int, user_id: str) -> bool:
        """Показывает скрытый отзыв"""

        review = self.get_review_by_ids(movie_id, user_id)
        if review:
            review.hidden = False
            self.db_session.commit()
            return True
        return False

    def delete_review(self, review: ReviewDBModel) -> None:
        """Удаляет отзыв из базы данных"""

        self.db_session.delete(review)
        self.db_session.commit()

    def delete_review_by_ids(self, movie_id: int, user_id: str) -> bool:
        """Удаляет отзыв по ID фильма и ID пользователя. Returns: True, если отзыв был удален, False - если не найден"""
        
        review = self.get_review_by_ids(movie_id, user_id)
        if review:
            self.db_session.delete(review)
            self.db_session.commit()
            return True
        return False