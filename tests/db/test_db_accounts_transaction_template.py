import pytest
from sqlalchemy.orm import Session
from utils.data_generator import DataGenerator, faker


class TestDBAccountsTransactionTemplate:
    """
    Класс тестов для работы с базой данных accounts_transaction_template.
    
    Включает тесты для создания, чтения, обновления и удаления записей,
    а также тестирование транзакций и переводов между счетами.
    """
    
    def test_account_crud_operations(self, db_helper):
        """
        Тест базовых CRUD операций с аккаунтами
        """
        # Генерируем тестовые данные
        user_name = f"TestUser_{faker.uuid4()}"
        initial_balance = faker.random_int(min=1000, max=5000)
        
        # Создание аккаунта
        account = db_helper.create_test_account(user_name, initial_balance)
        
        try:
            # Проверяем создание
            assert account.user == user_name
            assert account.balance == initial_balance
            
            # Проверяем чтение по имени пользователя
            retrieved_account = db_helper.get_account_by_user(user_name)
            assert retrieved_account is not None
            assert retrieved_account.user == user_name
            assert retrieved_account.balance == initial_balance
            
            # Проверяем существование аккаунта
            assert db_helper.account_exists_by_user(user_name)
            
            # Тестируем поиск несуществующего аккаунта
            fake_user = f"NonExistent_{faker.uuid4()}"
            non_existent_account = db_helper.get_account_by_user(fake_user)
            assert non_existent_account is None
            assert not db_helper.account_exists_by_user(fake_user)
            
        finally:
            # Удаляем тестовый аккаунт
            db_helper.cleanup_test_data([account])

    def test_account_balance_operations(self, db_helper):
        """
        Тест операций с балансом аккаунта
        """
        user_name = f"BalanceUser_{faker.uuid4()}"
        initial_balance = 1000
        
        account = db_helper.create_test_account(user_name, initial_balance)
        
        try:
            # Проверяем начальный баланс
            assert account.balance == initial_balance
            
            # Обновляем баланс
            new_balance = 1500
            db_helper.update_account_balance(user_name, new_balance)
            
            # Проверяем обновленный баланс
            updated_account = db_helper.get_account_by_user(user_name)
            assert updated_account.balance == new_balance
            
        finally:
            db_helper.cleanup_test_data([account])

    def test_multiple_accounts_operations(self, db_helper):
        """
        Тест операций с несколькими аккаунтами
        """
        # Создаем несколько аккаунтов
        accounts_data = [
            (f"User1_{faker.uuid4()}", 1000),
            (f"User2_{faker.uuid4()}", 2000),
            (f"User3_{faker.uuid4()}", 500)
        ]
        
        accounts = []
        for user_name, balance in accounts_data:
            account = db_helper.create_test_account(user_name, balance)
            accounts.append(account)
        
        try:
            # Проверяем, что все аккаунты созданы
            assert len(accounts) == 3
            
            # Проверяем уникальность имен пользователей
            user_names = [acc.user for acc in accounts]
            assert len(set(user_names)) == 3
            
            # Проверяем балансы
            for i, (expected_user, expected_balance) in enumerate(accounts_data):
                assert accounts[i].balance == expected_balance
                
            # Проверяем поиск каждого аккаунта
            for account in accounts:
                found_account = db_helper.get_account_by_user(account.user)
                assert found_account is not None
                assert found_account.user == account.user
                assert found_account.balance == account.balance
                
        finally:
            db_helper.cleanup_test_data(accounts)

    def test_accounts_transaction_template(self, db_helper):
        """
        Тест транзакций между аккаунтами
        """
        # Создаем новые записи в базе данных
        stan_user = f"Stan_{faker.random_int(min=10000, max=99999)}"
        bob_user = f"Bob_{faker.random_int(min=10000, max=99999)}"
        
        stan = db_helper.create_test_account(stan_user, 1000)
        bob = db_helper.create_test_account(bob_user, 500)
        
        def transfer_money(from_user: str, to_user: str, amount: int):
            """
            Переводит деньги с одного счета на другой.
            """
            from_account = db_helper.get_account_by_user(from_user)
            to_account = db_helper.get_account_by_user(to_user)

            if not from_account or not to_account:
                raise ValueError("Один из аккаунтов не найден")

            # Проверяем, что на счете достаточно средств
            if from_account.balance < amount:
                raise ValueError("Недостаточно средств на счете")

            # Выполняем перевод
            new_from_balance = from_account.balance - amount
            new_to_balance = to_account.balance + amount
            
            db_helper.update_account_balance(from_user, new_from_balance)
            db_helper.update_account_balance(to_user, new_to_balance)

        try:
            # Проверяем начальные балансы
            assert stan.balance == 1000
            assert bob.balance == 500

            # Выполняем перевод 200 единиц от stan к bob
            transfer_money(from_user=stan.user, to_user=bob.user, amount=200)

            # Обновляем объекты из базы данных
            updated_stan = db_helper.get_account_by_user(stan.user)
            updated_bob = db_helper.get_account_by_user(bob.user)

            # Проверяем, что балансы изменились
            assert updated_stan.balance == 800
            assert updated_bob.balance == 700

            # Тестируем перевод с недостаточными средствами
            with pytest.raises(ValueError, match="Недостаточно средств"):
                transfer_money(from_user=stan.user, to_user=bob.user, amount=1000)

        except Exception as e:
            # Если произошла ошибка, откатываем транзакцию
            db_helper.db_session.rollback()
            pytest.fail(f"Ошибка при переводе денег: {e}")
            
        finally:
            # Удаляем данные для тестирования из базы
            db_helper.cleanup_test_data([stan, bob])

    def test_account_to_dict_method(self, db_helper):
        """
        Тест метода to_dict для аккаунта
        """
        user_name = f"DictUser_{faker.uuid4()}"
        balance = 750
        
        account = db_helper.create_test_account(user_name, balance)
        
        try:
            # Тестируем метод to_dict
            account_dict = account.to_dict()
            
            assert isinstance(account_dict, dict)
            assert account_dict['user'] == user_name
            assert account_dict['balance'] == balance
            assert len(account_dict) == 2  # Проверяем, что в словаре только 2 ключа
            
        finally:
            db_helper.cleanup_test_data([account])