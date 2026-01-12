from playwright.sync_api import Page, expect
from utils.data_generator import DataGenerator


def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    user_email = DataGenerator.generation_random_email()

    page.get_by_placeholder("Имя Фамилия Отчество", exact=True).fill('Жмышенко Валерий Альбертович')
    page.get_by_placeholder("Email", exact=True).fill(user_email)
    page.get_by_placeholder("Пароль", exact=True).fill('qwerty123Q')
    page.get_by_placeholder("Повторите пароль", exact=True).fill('qwerty123Q')

    #page.get_by_role("button", name="Зарегистрироваться").click()
    page.locator("button:has-text('Зарегистрироваться')").click()

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)

    page.screenshot(path='screenshots/test_registration.png')
    