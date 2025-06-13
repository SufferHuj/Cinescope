from api.api_manager import ApiManager


class User:

    def __init__(self, email: str, password: str, roles: list, api_manager: ApiManager):

        self.email = email
        self.password = password
        self.roles = roles
        self.api = api_manager

    @property #декоратор @property делает метод creds доступным как атрибут
    def creds(self):

        """
        Возвращает кортеж (email, password)
        """

        return self.email, self.password