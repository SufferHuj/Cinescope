"""
Тесты для методов работы с платежами в базе данных.

Этот модуль содержит тесты для проверки корректности работы методов
DBHelper, связанных с операциями над платежами в базе данных.
"""

from utils.data_generator import DataGenerator
from db_models.db_payment_model import PaymentStatus


class TestDBPayments:
    """
    Класс тестов для работы с базой данных платежей.
    
    Включает тесты для создания, чтения и удаления платежей,
    а также проверки различных статусов платежей.
    """

    def test_create_payment_success(self, db_helper, movie_test_data, payment_test_data):
        """
        Тест успешного создания платежа
        """
        # Создаем тестового пользователя и фильм
        user_data = DataGenerator.generate_user_data()
        created_user = db_helper.create_test_user(user_data)
        created_movie = db_helper.create_test_movie(movie_test_data)
        
        # Создаем данные платежа с помощью фикстуры
        payment_data = payment_test_data(
            user_id=created_user.id,
            movie_id=created_movie.id
        )
        
        payment = db_helper.create_test_payment(payment_data)
        
        try:
            # Проверяем, что платеж создан
            assert payment.id is not None
            assert payment.user_id == payment_data['user_id']
            assert payment.movie_id == payment_data['movie_id']
            assert payment.status == payment_data['status']
            assert payment.amount == payment_data['amount']
            assert payment.total == payment_data['total']
        finally:
            # Удаляем тестовые данные
            db_helper.cleanup_test_data([payment, created_user, created_movie])

    def test_get_payment_by_id_existing(self, db_helper, movie_test_data, payment_test_data):
        """
        Тест получения существующего платежа по ID
        """
        # Создаем тестового пользователя и фильм
        user_data = DataGenerator.generate_user_data()
        created_user = db_helper.create_test_user(user_data)
        created_movie = db_helper.create_test_movie(movie_test_data)
        
        # Создаем данные платежа с помощью фикстуры
        payment_data = payment_test_data(
            user_id=created_user.id,
            movie_id=created_movie.id
        )
        
        created_payment = db_helper.create_test_payment(payment_data)
        
        try:
            # Получаем платеж по ID
            retrieved_payment = db_helper.get_payment_by_id(created_payment.id)
            
            # Проверяем, что платеж найден и данные совпадают
            assert retrieved_payment is not None
            assert retrieved_payment.id == created_payment.id
            assert retrieved_payment.user_id == created_payment.user_id
            assert retrieved_payment.movie_id == created_payment.movie_id
        finally:
            # Удаляем тестовые данные
            db_helper.cleanup_test_data([created_payment, created_user, created_movie])

    def test_create_payment_with_invalid_card_status(self, db_helper, movie_test_data, payment_test_data):
        """
        Тест создания платежа со статусом INVALID_CARD
        """
        # Создаем тестового пользователя и фильм
        user_data = DataGenerator.generate_user_data()
        created_user = db_helper.create_test_user(user_data)
        created_movie = db_helper.create_test_movie(movie_test_data)
        
        # Создаем данные платежа со статусом INVALID_CARD
        payment_data = payment_test_data(
            user_id=created_user.id,
            movie_id=created_movie.id,
            status=PaymentStatus.INVALID_CARD
        )
        
        try:
            # Создаем платеж
            created_payment = db_helper.create_test_payment(payment_data)
            
            # Проверяем, что платеж создан с правильным статусом
            assert created_payment is not None
            assert created_payment.status == PaymentStatus.INVALID_CARD
            assert created_payment.user_id == created_user.id
            assert created_payment.movie_id == created_movie.id
        finally:
            # Удаляем тестовые данные
            db_helper.cleanup_test_data([created_payment, created_user, created_movie])

    def test_create_payment_with_error_status(self, db_helper, movie_test_data, payment_test_data):
        """
        Тест создания платежа со статусом ERROR
        """
        # Создаем тестового пользователя и фильм
        user_data = DataGenerator.generate_user_data()
        created_user = db_helper.create_test_user(user_data)
        created_movie = db_helper.create_test_movie(movie_test_data)
        
        # Создаем данные платежа со статусом ERROR
        payment_data = payment_test_data(
            user_id=created_user.id,
            movie_id=created_movie.id,
            status=PaymentStatus.ERROR
        )
        
        try:
            # Создаем платеж
            created_payment = db_helper.create_test_payment(payment_data)
            
            # Проверяем, что платеж создан с правильным статусом
            assert created_payment is not None
            assert created_payment.status == PaymentStatus.ERROR
            assert created_payment.user_id == created_user.id
            assert created_payment.movie_id == created_movie.id
        finally:
            # Удаляем тестовые данные
            db_helper.cleanup_test_data([created_payment, created_user, created_movie])

    def test_delete_payment_success(self, db_helper, movie_test_data, payment_test_data):
        """
        Тест успешного удаления платежа
        """
        # Создаем тестового пользователя и фильм
        user_data = DataGenerator.generate_user_data()
        created_user = db_helper.create_test_user(user_data)
        created_movie = db_helper.create_test_movie(movie_test_data)
        
        # Создаем платеж с помощью фикстуры
        payment_data = payment_test_data(
            user_id=created_user.id,
            movie_id=created_movie.id
        )
        
        payment = db_helper.create_test_payment(payment_data)
        
        try:
            # Удаляем платеж
            db_helper.delete_payment(payment)
            
            # Проверяем, что платеж удален
            retrieved_payment = db_helper.get_payment_by_id(payment.id)
            assert retrieved_payment is None
        finally:
            # Удаляем оставшиеся тестовые данные
            db_helper.cleanup_test_data([created_user, created_movie])
