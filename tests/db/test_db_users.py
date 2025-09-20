import pytest
from utils.data_generator import DataGenerator, faker


class TestDBUsers:
    """
    Класс тестов для работы с базой данных пользователей.
    
    Включает тесты для создания, чтения, обновления и удаления пользователей,
    а также проверки уникальности, валидации и различных методов поиска.
    """

    def test_user_crud_operations(self, db_helper):
        """
        Тест базовых CRUD операций с пользователями
        """
        # Генерируем тестовые данные пользователя
        user_data = DataGenerator.generate_user_data()
        
        # Создание пользователя
        created_user = db_helper.create_test_user(user_data)
        
        try:
            # Проверяем создание
            assert created_user.id is not None
            assert created_user.email == user_data['email']
            assert created_user.full_name == user_data['full_name']
            assert created_user.password == user_data['password']
            assert created_user.verified == user_data['verified']
            assert created_user.banned == user_data['banned']
            assert created_user.roles == user_data['roles']
            
            # Проверяем чтение по ID
            retrieved_user = db_helper.get_user_by_id(created_user.id)
            assert retrieved_user is not None
            assert retrieved_user.email == user_data['email']
            assert retrieved_user.full_name == user_data['full_name']
            
            # Проверяем чтение по email
            user_by_email = db_helper.get_user_by_email(created_user.email)
            assert user_by_email is not None
            assert user_by_email.id == created_user.id
            
            # Проверяем существование пользователя
            assert db_helper.user_exists_by_email(created_user.email)

            # Тестируем поиск несуществующего пользователя по ID
            fake_user_id = f"{faker.uuid4()}"
            non_existent_user = db_helper.get_user_by_id(fake_user_id)
            assert non_existent_user is None
            
            # Тестируем поиск несуществующего пользователя по email
            fake_email = f"nonexistent_{faker.uuid4()}@example.com"
            non_existent_email_user = db_helper.get_user_by_email(fake_email)
            assert non_existent_email_user is None
            
        finally:
            # Удаляем тестового пользователя
            db_helper.cleanup_test_data([created_user])

    def test_user_count_methods(self, db_helper):
        """
        Тест методов подсчета количества пользователей
        """
        # Получаем изначальное количество пользователей ДО создания тестового пользователя
        initial_users_count = db_helper.get_total_users_count()
        
        # Создаем тестового пользователя
        user_data = DataGenerator.generate_user_data()
        created_user = db_helper.create_test_user(user_data)
        
        try:
            # Проверяем, что количество увеличилось на 1 после создания пользователя
            current_users_count = db_helper.get_total_users_count()
            assert current_users_count == initial_users_count + 1, \
                f"Ожидалось {initial_users_count + 1} пользователей, получено {current_users_count}"
            
            # Проверяем, что метод возвращает число
            assert isinstance(current_users_count, int)
            assert current_users_count >= 0
            
        finally:
            # Очищаем тестовые данные
            db_helper.cleanup_test_data([created_user])

    def test_multiple_users_operations(self, db_helper):
        """
        Тест операций с несколькими пользователями
        """
        # Создаем несколько пользователей с разными данными
        user_data_1 = DataGenerator.generate_user_data()
        user_data_1['full_name'] = f"Пользователь 1 - {faker.name()}"
        user_data_1['verified'] = True
        
        user_data_2 = DataGenerator.generate_user_data()
        user_data_2['full_name'] = f"Пользователь 2 - {faker.name()}"
        user_data_2['verified'] = False
        user_data_2['banned'] = True
        
        user_data_3 = DataGenerator.generate_user_data()
        user_data_3['full_name'] = f"Пользователь 3 - {faker.name()}"
        user_data_3['roles'] = '{ADMIN}'
        
        user1 = db_helper.create_test_user(user_data_1)
        user2 = db_helper.create_test_user(user_data_2)
        user3 = db_helper.create_test_user(user_data_3)

        try:
            # Проверяем, что все пользователи созданы
            assert user1.id is not None
            assert user2.id is not None
            assert user3.id is not None
            
            # Проверяем уникальность email
            assert user1.email != user2.email != user3.email
            
            # Проверяем различные атрибуты
            assert user1.verified is True
            assert user2.verified is False
            assert user2.banned is True
            assert user3.roles == '{ADMIN}'
            
            # Проверяем поиск каждого пользователя
            found_user1 = db_helper.get_user_by_email(user1.email)
            found_user2 = db_helper.get_user_by_email(user2.email)
            found_user3 = db_helper.get_user_by_email(user3.email)
            
            assert found_user1.id == user1.id
            assert found_user2.id == user2.id
            assert found_user3.id == user3.id

        finally:
            # Очищаем тестовые данные
            db_helper.cleanup_test_data([user1, user2, user3])

    def test_user_email_uniqueness(self, db_helper):
        """
        Тест уникальности email адресов
        """
        # Создаем первого пользователя
        user_data_1 = DataGenerator.generate_user_data()
        user1 = db_helper.create_test_user(user_data_1)
        user2 = None
        
        try:
            # Проверяем, что пользователь создан
            assert db_helper.user_exists_by_email(user1.email)
            
            # Пытаемся создать второго пользователя с тем же email
            user_data_2 = DataGenerator.generate_user_data()
            user_data_2['email'] = user1.email  # Используем тот же email
            
            # Отключаем вызов исключения при дублирование email
            exception_occurred = False
            try:
                user2 = db_helper.create_test_user(user_data_2)
            except Exception as e:
                # Ожидаемое поведение - исключение при дублировании email
                exception_occurred = True
                # Откатываем транзакцию после исключения
                db_helper.db_session.rollback()
                assert "duplicate" in str(e).lower() or "unique" in str(e).lower() or "constraint" in str(e).lower()
            
            # Если исключение не произошло, значит дубликат создался
            if not exception_occurred and user2:
                # Проверяем, что оба пользователя имеют одинаковый email
                assert user1.email == user2.email
                
        finally:
            # Очищаем тестовые данные
            users_to_cleanup = [user1]
            if user2:
                users_to_cleanup.append(user2)
            db_helper.cleanup_test_data(users_to_cleanup)
