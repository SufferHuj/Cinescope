from typing import List, Optional, Union
from sqlalchemy.orm import Session
from db_models.db_user_model import UserDBModel
from db_models.db_movie_model import MovieDBModel
from db_models.db_genre_model import GenreDBModel
from db_models.db_review_model import ReviewDBModel
from db_models.db_account_transaction_template_model import AccountTransactionTemplate
from db_models.db_payment_model import PaymentDBModel


class DBHelper:
    """ Класс-помощник для работы с базой данных в тестах
    Attributes: db_session (Session): Сессия SQLAlchemy для работы с БД """
    
    def __init__(self, db_session: Session):
        """ Инициализация DBHelper с сессией базы данных """

        self.db_session = db_session

    # ==================== ОБЩИЕ МЕТОДЫ ====================
    
    def cleanup_test_data(self, objects_to_delete: List[Union[UserDBModel, MovieDBModel, GenreDBModel, ReviewDBModel, PaymentDBModel]]) -> None:
        """ Очищает тестовые данные из базы данных после тестов """

        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    def get_total_movies_count(self) -> int:
        """ Получает общее количество фильмов в базе данных """

        return self.db_session.query(MovieDBModel).count()

    def get_total_users_count(self) -> int:
        """ Получает общее количество пользователей в базе данных """

        return self.db_session.query(UserDBModel).count()

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ПОЛЬЗОВАТЕЛЯМИ users ====================
    
    def create_test_user(self, user_data: dict) -> UserDBModel:
        """ Создает тестового пользователя в базе данных """
        
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: Union[str, int]) -> Optional[UserDBModel]:
        """ Получает пользователя по ID """

        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[UserDBModel]:
        """ Получает пользователя по email """

        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).first()

    def user_exists_by_email(self, email: str) -> bool:
        """ Проверяет существование пользователя по email """

        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).count() > 0

    def delete_user(self, user: UserDBModel) -> None:
        """ Удаляет пользователя из базы данных """

        self.db_session.delete(user)
        self.db_session.commit()

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ФИЛЬМАМИ movies ====================
    
    def create_test_movie(self, movie_data: dict) -> MovieDBModel:
        """ Создает тестовый фильм в базе данных """
        
        movie = MovieDBModel(**movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return movie

    def get_movie_by_id(self, movie_id: Union[str, int]) -> Optional[MovieDBModel]:
        """ Получает фильм по ID """

        return self.db_session.query(MovieDBModel).filter(MovieDBModel.id == movie_id).first()

    def get_movie_by_name(self, name: str) -> Optional[MovieDBModel]:
        """ Получает фильм по названию """

        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == name).first()

    def movie_exists_by_name(self, name: str) -> bool:
        """ Проверяет существование фильма по названию """

        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == name).count() > 0

    def get_movies_by_genre(self, genre_id: int) -> List[MovieDBModel]:
        """ Получает все фильмы определенного жанра """

        return self.db_session.query(MovieDBModel).filter(MovieDBModel.genre_id == genre_id).all()

    def get_movies_by_price_range(self, min_price: int, max_price: int) -> List[MovieDBModel]:
        """ Получает фильмы в указанном ценовом диапазоне """

        return self.db_session.query(MovieDBModel).filter(
            MovieDBModel.price >= min_price,
            MovieDBModel.price <= max_price
        ).all()

    def delete_movie(self, movie: MovieDBModel) -> None:
        """ Удаляет фильм из базы данных """

        self.db_session.delete(movie)
        self.db_session.commit()

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ЖАНРАМИ genres ====================
    
    def create_test_genre(self, genre_data: dict) -> GenreDBModel:
        """ Создает тестовый жанр в базе данных """

        genre = GenreDBModel(**genre_data)
        self.db_session.add(genre)
        self.db_session.commit()
        self.db_session.refresh(genre)
        return genre

    def get_genre_by_id(self, genre_id: Union[str, int]) -> Optional[GenreDBModel]:
        """ Получает жанр по ID """

        return self.db_session.query(GenreDBModel).filter(GenreDBModel.id == genre_id).first()

    def get_genre_by_name(self, name: str) -> Optional[GenreDBModel]:
        """ Получает жанр по названию """

        return self.db_session.query(GenreDBModel).filter(GenreDBModel.name == name).first()

    def genre_exists_by_name(self, name: str) -> bool:
        """ Проверяет существование жанра по названию """

        return self.db_session.query(GenreDBModel).filter(GenreDBModel.name == name).first() is not None

    def delete_genre(self, genre: GenreDBModel) -> None:
        """ Удаляет жанр из базы данных """

        self.db_session.delete(genre)
        self.db_session.commit()

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С АККАУНТАМИ accounts ====================
    
    def create_test_account(self, user_name: str, balance: int) -> AccountTransactionTemplate:
        """ Создает тестовый аккаунт в базе данных """

        account = AccountTransactionTemplate(user=user_name, balance=balance)
        self.db_session.add(account)
        self.db_session.commit()
        return account
    
    def get_account_by_user(self, user_name: str) -> Optional[AccountTransactionTemplate]:
        """ Получает аккаунт по имени пользователя """

        return self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first()
    
    def account_exists_by_user(self, user_name: str) -> bool:
        """ Проверяет существование аккаунта по имени пользователя """

        return self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first() is not None
    
    def update_account_balance(self, user_name: str, new_balance: int) -> bool:
        """ Обновляет баланс аккаунта """

        account = self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first()
        if account:
            account.balance = new_balance
            self.db_session.commit()
        else:
            raise ValueError(f"Аккаунт с именем пользователя '{user_name}' не найден")
    
    def get_all_accounts(self) -> List[AccountTransactionTemplate]:
        """ Получает все аккаунты из базы данных """

        return self.db_session.query(AccountTransactionTemplate).all()
    
    def delete_account_by_user(self, user_name: str) -> bool:
        """ Удаляет аккаунт по имени пользователя """

        account = self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first()
        if account:
            self.db_session.delete(account)
            self.db_session.commit()
            return True
        return False

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ОТЗЫВАМИ reviews ====================
    
    def create_test_review(self, review_data: dict) -> ReviewDBModel:
        """ Создает тестовый отзыв в базе данных """
        review = ReviewDBModel(**review_data)
        self.db_session.add(review)
        self.db_session.commit()
        self.db_session.refresh(review)
        return review

    def get_review_by_ids(self, movie_id: int, user_id: str) -> Optional[ReviewDBModel]:
        """ Получает отзыв по ID фильма и ID пользователя """

        return self.db_session.query(ReviewDBModel).filter(
            ReviewDBModel.movie_id == movie_id,
            ReviewDBModel.user_id == user_id
        ).first()

    def get_reviews_by_movie_id(self, movie_id: int) -> List[ReviewDBModel]:
        """ Получает все отзывы для определенного фильма """

        return self.db_session.query(ReviewDBModel).filter(ReviewDBModel.movie_id == movie_id).all()

    def review_exists_by_ids(self, movie_id: int, user_id: str) -> bool:
        """ Проверяет существование отзыва по ID фильма и ID пользователя """

        return self.db_session.query(ReviewDBModel).filter(
            ReviewDBModel.movie_id == movie_id,
            ReviewDBModel.user_id == user_id
        ).first() is not None

    def update_review_rating(self, movie_id: int, user_id: str, new_rating: int) -> bool:
        """ Обновляет рейтинг отзыва """

        review = self.get_review_by_ids(movie_id, user_id)
        if review:
            review.rating = new_rating
            self.db_session.commit()
            return True
        return False

    def update_review_text(self, movie_id: int, user_id: str, new_text: str) -> bool:
        """ Обновляет текст отзыва """

        review = self.get_review_by_ids(movie_id, user_id)
        if review:
            review.text = new_text
            self.db_session.commit()
            return True
        return False

    def hide_review(self, movie_id: int, user_id: str) -> bool:
        """ Скрывает отзыв """

        review = self.get_review_by_ids(movie_id, user_id)
        if review:
            review.hidden = True
            self.db_session.commit()
            return True
        return False

    def show_review(self, movie_id: int, user_id: str) -> bool:
        """ Показывает скрытый отзыв """

        review = self.get_review_by_ids(movie_id, user_id)
        if review:
            review.hidden = False
            self.db_session.commit()
            return True
        return False

    def delete_review(self, review: ReviewDBModel) -> None:
        """ Удаляет отзыв из базы данных """

        self.db_session.delete(review)
        self.db_session.commit()

    def delete_review_by_ids(self, movie_id: int, user_id: str) -> bool:
        """ Удаляет отзыв по ID фильма и ID пользователя. Returns: True, если отзыв был удален, False - если не найден """

        review = self.get_review_by_ids(movie_id, user_id)
        if review:
            self.db_session.delete(review)
            self.db_session.commit()
            return True
        return False

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ПЛАТЕЖАМИ payments ====================
    
    def create_test_payment(self, payment_data: dict) -> PaymentDBModel:
        """ Создает тестовый платеж в базе данных """

        payment = PaymentDBModel(**payment_data)
        self.db_session.add(payment)
        self.db_session.commit()
        self.db_session.refresh(payment)
        return payment

    def get_payment_by_id(self, payment_id: int) -> Optional[PaymentDBModel]:
        """ Получает платеж по ID """

        return self.db_session.query(PaymentDBModel).filter(PaymentDBModel.id == payment_id).first()

    def delete_payment(self, payment: PaymentDBModel) -> None:
        """ Удаляет платеж из базы данных """

        self.db_session.delete(payment)
        self.db_session.commit()
