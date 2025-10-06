from typing import List, Optional, Union
from sqlalchemy.orm import Session
from db_models.db_user_model import UserDBModel
from db_models.db_movie_model import MovieDBModel
from db_models.db_genre_model import GenreDBModel
from db_models.db_account_transaction_template_model import AccountTransactionTemplate


class DBHelper:
    """
    Класс-помощник для работы с базой данных в тестах.
    
    Предоставляет удобные методы для создания, получения, обновления и удаления
    тестовых данных из базы данных. Используется для подготовки тестовых данных
    и проверки состояния БД после выполнения тестов.
    
    Attributes:
        db_session (Session): Сессия SQLAlchemy для работы с БД
    """
    
    def __init__(self, db_session: Session):
        """
        Инициализация DBHelper с сессией базы данных.
        
        Args:
            db_session (Session): Активная сессия SQLAlchemy
        """
        self.db_session = db_session

    # ==================== ОБЩИЕ МЕТОДЫ ====================
    
    def cleanup_test_data(self, objects_to_delete: List[Union[UserDBModel, MovieDBModel, GenreDBModel]]) -> None:
        """
        Очищает тестовые данные из базы данных.
        
        Удаляет переданные объекты из БД. Полезно для очистки после тестов.
        
        Args:
            objects_to_delete (List[Union[UserDBModel, MovieDBModel]]): 
                Список объектов для удаления
                
        Example:
            test_objects = [user1, user2, movie1, movie2]
            db_helper.cleanup_test_data(test_objects)
        """
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    def get_total_movies_count(self) -> int:
        """
        Получает общее количество фильмов в базе данных.
        
        Returns:
            int: Общее количество фильмов
        """
        return self.db_session.query(MovieDBModel).count()

    def get_total_users_count(self) -> int:
        """
        Получает общее количество пользователей в базе данных.
        
        Returns:
            int: Общее количество пользователей
        """
        return self.db_session.query(UserDBModel).count()

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ПОЛЬЗОВАТЕЛЯМИ users ====================
    
    def create_test_user(self, user_data: dict) -> UserDBModel:
        """
        Создает тестового пользователя в базе данных.
        
        Args:
            user_data (dict): Словарь с данными пользователя
            
        Returns:
            UserDBModel: Созданный объект пользователя с присвоенным ID
            
        Example:
            user_data = {
                'email': 'test@example.com',
                'full_name': 'Test User',
                'password_hash': 'hashed_password'
            }
            user = db_helper.create_test_user(user_data)
        """
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: Union[str, int]) -> Optional[UserDBModel]:
        """
        Получает пользователя по ID.
        
        Args:
            user_id (Union[str, int]): ID пользователя
            
        Returns:
            Optional[UserDBModel]: Объект пользователя или None, если не найден
        """
        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[UserDBModel]:
        """
        Получает пользователя по email.
        
        Args:
            email (str): Email адрес пользователя
            
        Returns:
            Optional[UserDBModel]: Объект пользователя или None, если не найден
        """
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).first()

    def user_exists_by_email(self, email: str) -> bool:
        """
        Проверяет существование пользователя по email.
        
        Args:
            email (str): Email адрес для проверки
            
        Returns:
            bool: True, если пользователь существует, False - если нет
        """
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).count() > 0

    def delete_user(self, user: UserDBModel) -> None:
        """
        Удаляет пользователя из базы данных.
        
        Args:
            user (UserDBModel): Объект пользователя для удаления
        """
        self.db_session.delete(user)
        self.db_session.commit()

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ФИЛЬМАМИ movies ====================
    
    def create_test_movie(self, movie_data: dict) -> MovieDBModel:
        """
        Создает тестовый фильм в базе данных.
        
        Args:
            movie_data (dict): Словарь с данными фильма
            
        Returns:
            MovieDBModel: Созданный объект фильма с присвоенным ID
            
        Example:
            movie_data = {
                'name': 'Test Movie',
                'price': 500,
                'description': 'Test description',
                'location': 'MSK',
                'published': True,
                'genre_id': 1
            }
            movie = db_helper.create_test_movie(movie_data)
        """
        movie = MovieDBModel(**movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return movie

    def get_movie_by_id(self, movie_id: Union[str, int]) -> Optional[MovieDBModel]:
        """
        Получает фильм по ID.
        
        Args:
            movie_id (Union[str, int]): ID фильма
            
        Returns:
            Optional[MovieDBModel]: Объект фильма или None, если не найден
        """
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.id == movie_id).first()

    def get_movie_by_name(self, name: str) -> Optional[MovieDBModel]:
        """
        Получает фильм по названию.
        
        Args:
            name (str): Название фильма
            
        Returns:
            Optional[MovieDBModel]: Объект фильма или None, если не найден
        """
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == name).first()

    def movie_exists_by_name(self, name: str) -> bool:
        """
        Проверяет существование фильма по названию.
        
        Args:
            name (str): Название фильма для проверки
            
        Returns:
            bool: True, если фильм существует, False - если нет
        """
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == name).count() > 0

    def get_movies_by_genre(self, genre_id: int) -> List[MovieDBModel]:
        """
        Получает все фильмы определенного жанра.
        
        Args:
            genre_id (int): ID жанра
            
        Returns:
            List[MovieDBModel]: Список фильмов указанного жанра
        """
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.genre_id == genre_id).all()

    def get_movies_by_price_range(self, min_price: int, max_price: int) -> List[MovieDBModel]:
        """
        Получает фильмы в указанном ценовом диапазоне.
        
        Args:
            min_price (int): Минимальная цена
            max_price (int): Максимальная цена
            
        Returns:
            List[MovieDBModel]: Список фильмов в указанном ценовом диапазоне
        """
        return self.db_session.query(MovieDBModel).filter(
            MovieDBModel.price >= min_price,
            MovieDBModel.price <= max_price
        ).all()

    def delete_movie(self, movie: MovieDBModel) -> None:
        """
        Удаляет фильм из базы данных.
        
        Args:
            movie (MovieDBModel): Объект фильма для удаления
        """
        self.db_session.delete(movie)
        self.db_session.commit()

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С ЖАНРАМИ genres ====================
    
    def create_test_genre(self, genre_data: dict) -> GenreDBModel:
        """
        Создает тестовый жанр в базе данных.
        
        Args:
            genre_data (dict): Словарь с данными жанра
            
        Returns:
            GenreDBModel: Созданный объект жанра с присвоенным ID
            
        Example:
            genre_data = {
                'name': 'Action'
            }
            genre = db_helper.create_test_genre(genre_data)
        """
        genre = GenreDBModel(**genre_data)
        self.db_session.add(genre)
        self.db_session.commit()
        self.db_session.refresh(genre)
        return genre

    def get_genre_by_id(self, genre_id: Union[str, int]) -> Optional[GenreDBModel]:
        """
        Получает жанр по ID.
        
        Args:
            genre_id (Union[str, int]): ID жанра
            
        Returns:
            Optional[GenreDBModel]: Объект жанра или None, если не найден
        """
        return self.db_session.query(GenreDBModel).filter(GenreDBModel.id == genre_id).first()

    def get_genre_by_name(self, name: str) -> Optional[GenreDBModel]:
        """
        Получает жанр по названию.
        
        Args:
            name (str): Название жанра
            
        Returns:
            Optional[GenreDBModel]: Объект жанра или None, если не найден
        """
        return self.db_session.query(GenreDBModel).filter(GenreDBModel.name == name).first()

    def genre_exists_by_name(self, name: str) -> bool:
        """
        Проверяет существование жанра по названию.
        
        Args:
            name (str): Название жанра
            
        Returns:
            bool: True, если жанр существует, False в противном случае
        """
        return self.db_session.query(GenreDBModel).filter(GenreDBModel.name == name).first() is not None

    def delete_genre(self, genre: GenreDBModel) -> None:
        """
        Удаляет жанр из базы данных.
        
        Args:
            genre (GenreDBModel): Объект жанра для удаления
        """
        self.db_session.delete(genre)
        self.db_session.commit()

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С АККАУНТАМИ accounts ====================
    
    def create_test_account(self, user_name: str, balance: int):
        """
        Создает тестовый аккаунт в базе данных.
        
        Args:
            user_name: Имя пользователя
            balance: Начальный баланс
            
        Returns:
            AccountTransactionTemplate: Созданный объект аккаунта
        """
        account = AccountTransactionTemplate(user=user_name, balance=balance)
        self.db_session.add(account)
        self.db_session.commit()
        return account
    
    def get_account_by_user(self, user_name: str):
        """
        Получает аккаунт по имени пользователя.
        
        Args:
            user_name: Имя пользователя
            
        Returns:
            AccountTransactionTemplate или None: Найденный аккаунт или None
        """
        return self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first()
    
    def account_exists_by_user(self, user_name: str) -> bool:
        """
        Проверяет существование аккаунта по имени пользователя.
        
        Args:
            user_name: Имя пользователя
            
        Returns:
            bool: True если аккаунт существует, False иначе
        """
        return self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first() is not None
    
    def update_account_balance(self, user_name: str, new_balance: int):
        """
        Обновляет баланс аккаунта.
        
        Args:
            user_name: Имя пользователя
            new_balance: Новый баланс
        """
        account = self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first()
        if account:
            account.balance = new_balance
            self.db_session.commit()
        else:
            raise ValueError(f"Аккаунт с именем пользователя '{user_name}' не найден")
    
    def get_all_accounts(self):
        """
        Получает все аккаунты из базы данных.
        
        Returns:
            List[AccountTransactionTemplate]: Список всех аккаунтов
        """
        return self.db_session.query(AccountTransactionTemplate).all()
    
    def delete_account_by_user(self, user_name: str):
        """
        Удаляет аккаунт по имени пользователя.
        
        Args:
            user_name: Имя пользователя
            
        Returns:
            bool: True если аккаунт был удален, False если не найден
        """
        account = self.db_session.query(AccountTransactionTemplate).filter_by(user=user_name).first()
        if account:
            self.db_session.delete(account)
            self.db_session.commit()
            return True
        return False
