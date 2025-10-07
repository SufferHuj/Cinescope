import os
from dotenv import load_dotenv

load_dotenv()


class MoviesDbCreds:
    """ Учетные данные для подключения к БД """
    
    HOST = os.getenv('DB_MOVIES_HOST')  # Хост базы данных
    PORT = os.getenv('DB_MOVIES_PORT')  # Порт базы данных
    DATABASE_NAME = os.getenv('DB_MOVIES_NAME')  # Имя базы данных
    USERNAME = os.getenv('DB_MOVIES_USERNAME')  # Имя пользователя БД
    PASSWORD = os.getenv('DB_MOVIES_PASSWORD')  # Пароль пользователя БД
