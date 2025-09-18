import random
import string
import uuid
from datetime import datetime
from faker import Faker

faker = Faker()


class DataGenerator:
    """
    Класс для генерации случайных тестовых данных.
    
    Предоставляет статические методы для создания различных типов
    тестовых данных, соответствующих требованиям системы.
    """

    @staticmethod
    def generation_random_email():
        """
        Генерация случайного email адреса для тестирования.
        
        Returns:
            str: Email адрес в формате kkkek{random_string}@gmail.com
        """
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kkkek{random_string}@gmail.com"

    @staticmethod
    def generation_random_name():
        """
        Генерация случайного полного имени пользователя.
        
        Returns:
            str: Полное имя в формате "Имя Фамилия"
        """
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generation_random_password():
        """
        Генерация пароля, соответствующего требованиям системы.
        
        Создает пароль с обязательными требованиями:
        - Минимум 1 буква
        - Минимум 1 цифра
        - Допустимые специальные символы: ?@#$%^&*|:
        - Длина от 8 до 20 символов
        
        Returns:
            str: Сгенерированный пароль, соответствующий всем требованиям
        """

        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_lowercase)  # одна буква
        digits = random.choice(string.digits)  # одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"

        all_chars = string.ascii_letters + string.digits + special_chars

        remaining_length = random.randint(6, 18)  # остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generation_random_uuid():
        """
        Генерация случайного UUID для идентификации объектов.
        
        Returns:
            str: UUID в строковом формате
        """
        return str(uuid.uuid4())

    @staticmethod
    def generate_user_data() -> dict:
        """
        Генерирует полный набор данных для создания тестового пользователя через БД.
        
        Создает словарь со всеми необходимыми полями для создания пользователя
        в базе данных, включая временные метки и настройки по умолчанию.
        
        Returns:
            dict: Словарь с данными пользователя для вставки в БД
        """
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generation_random_email(),
            'full_name': DataGenerator.generation_random_name(),
            'password': DataGenerator.generation_random_password(),
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }
        