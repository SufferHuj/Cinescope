from api.api_manager import ApiManager


class User:
    """ Класс для представления пользователя в тестах.
    Инкапсулирует данные пользователя и предоставляет удобный интерфейс
    для работы с API через менеджер API """

    def __init__(self, email: str, password: str, roles: list, api_manager: ApiManager):
        """ Инициализация пользователя """

        self.email = email
        self.password = password
        self.roles = roles
        self.api = api_manager

    @property  # декоратор @property делает метод creds доступным как атрибут
    def creds(self):
        """ Возвращает учетные данные пользователя в виде кортежа. Returns: tuple (email, password) для аутентификации """
        
        return self.email, self.password
