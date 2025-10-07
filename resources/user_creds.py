import os
from dotenv import load_dotenv

load_dotenv()


class SuperAdminCreds:
    """ Учетные данные суперадминистратора для тестирования """
    
    USERNAME = os.getenv("SUPER_ADMIN_USERNAME")  # Имя пользователя суперадминистратора
    PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")  # Пароль суперадминистратора
