from playwright.sync_api import Page


class CsRegisterPage:
    def __init__(self, page: Page):
        self.page = page
        self.register_url = 'https://dev-cinescope.coconutqa.ru/register'

        self.home_button = page.get_by_role("link", name="Cinescope")
        self.all_movies_button = page.get_by_role("link", name="Все фильмы")

        self.full_name_button = page.get_by_role("textbox", name="Имя Фамилия Отчество")
        self.email_button = page.get_by_role("textbox", name="Email")
        self.password_button = page.get_by_role("textbox", name="Пароль")
        self.confirm_password_button = page.get_by_role("textbox", name="Повторите пароль")
        
        self.register_button = page.get_by_role("button", name="Зарегистрироваться")
        self.sign_in_button = page.get_by_role("link", name="Войти")
