from enum import Enum


class Roles(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"
MOVIES_API_BASE_URL = "https://api.dev-cinescope.coconutqa.ru"
PAYMENT_API_BASE_URL = "https://payment.dev-cinescope.coconutqa.ru"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
