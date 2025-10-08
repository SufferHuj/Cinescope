from enum import Enum
import enum


class PaymentStatus(enum.Enum):
    """ Перечисление статусов платежа. Соответствует типу public."Status" в базе данных """

    SUCCESS = "SUCCESS"
    INVALID_CARD = "INVALID_CARD"
    ERROR = "ERROR"


class Roles(str, Enum):
    """Перечисление ролей пользователей в системе """
    
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


# URL-адреса API для различных сервисов
BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"  # Базовый URL для аутентификации
MOVIES_API_BASE_URL = "https://api.dev-cinescope.coconutqa.ru"  # API для работы с фильмами
PAYMENT_API_BASE_URL = "https://payment.dev-cinescope.coconutqa.ru"  # API для платежей

# Стандартные HTTP заголовки для API запросов
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Эндпоинты для аутентификации
LOGIN_ENDPOINT = "/login"  # Эндпоинт для входа в систему
REGISTER_ENDPOINT = "/register"  # Эндпоинт для регистрации пользователя

# Константы для цветов в логах
RED = '\033[31m'  # Красный цвет для ошибок
GREEN = '\033[32m'  # Зеленый цвет для успешных операций
PURPLE = '\033[35m'  # Фиолетовый цвет для информационных сообщений
RESET = '\033[0m'  # Сброс цвета к стандартному
