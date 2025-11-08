import random
import string
import uuid
from datetime import datetime
from faker import Faker

faker = Faker()


class DataGenerator:
    """ Класс для генерации случайных тестовых данных """

    @staticmethod
    def generation_random_email():
        """ Генерация случайного email адреса для тестирования """

        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generation_random_name():
        """ Генерация случайного полного имени пользователя """

        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generation_random_password():
        """ Генерация пароля, соответствующего требованиям системы """

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
        """ Генерация случайного UUID для идентификации объектов """

        return str(uuid.uuid4())

    @staticmethod
    def generate_user_data() -> dict:
        """ Генерирует полный набор данных для создания тестового пользователя через БД """
        
        return {
            'id': f'{uuid.uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generation_random_email(),
            'full_name': DataGenerator.generation_random_name(),
            'password': DataGenerator.generation_random_password(),
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }
        