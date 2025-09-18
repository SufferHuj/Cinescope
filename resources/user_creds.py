import os
from dotenv import load_dotenv

load_dotenv()


class SuperAdminCreds:
    """
    Учетные данные суперадминистратора для тестирования.
    
    Получает логин и пароль суперадминистратора из переменных окружения
    для использования в автоматизированных тестах с повышенными правами.
    """
    USERNAME = os.getenv("SUPER_ADMIN_USERNAME")  # Имя пользователя суперадминистратора
    PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")  # Пароль суперадминистратора
