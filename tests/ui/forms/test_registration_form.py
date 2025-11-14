from playwright.sync_api import Page, expect
from utils.tools import Tools
from datetime import datetime

def test_registration_form(page: Page):
    """Тест проверяет работу формы регистрации"""

    page.goto("https://demoqa.com/automation-practice-form")

    expect(page.locator(".practice-form-wrapper")).to_be_visible()
    expect(page.get_by_role("heading", name="Practice Form", exact=True)).to_be_visible()
    
    # First Name
    page.locator("#firstName").type("Ivan")
    # Last Name
    page.locator("#lastName").type("Ivanov")

    # Email
    page.get_by_placeholder("name@example.com").type("tester@gmail.com")

    # Gender (радиокнопки)
    page.locator("#gender-radio-1").check(force=True)
    page.locator("#gender-radio-3").check(force=True)
    page.locator("#gender-radio-2").check(force=True)
    page.locator("#gender-radio-1").check(force=True)

    # Mobile Number
    page.get_by_placeholder("Mobile Number").fill("1234567890")

    # Date of Birth 
    value = page.get_attribute("#dateOfBirthInput", "value")
    today_str = datetime.today().strftime("%d %b %Y")
    assert value == today_str

    # Subjects
    page.locator("#subjectsInput").click()
    page.locator("#subjectsInput").type("Maths")
    page.locator("#subjectsInput").press("Enter")

    # Hobbies (чекбоксы)
    page.locator("#hobbies-checkbox-1").check(force=True)
    page.locator("#hobbies-checkbox-2").check(force=True)
    page.locator("#hobbies-checkbox-3").check(force=True)
    page.locator("#hobbies-checkbox-3").uncheck(force=True)
    expect(page.get_by_role("checkbox", name="Music")).not_to_be_checked()

    # Picture (загрузка файла)
    upload_file = Tools.files_dir("upload_tmp", "sampleFile.jpeg")
    page.set_input_files("#uploadPicture", str(upload_file))

    # Current Address
    page.locator("#currentAddress").type("123 Main St, Anywhere, USA")

    # State и City (выпадающие списки)
    page.locator("#state").click()
    page.get_by_text("NCR", exact=True).click()
    page.locator("#city").click()
    page.get_by_text("Delhi", exact=True).click()

    # Футер
    page.locator("footer").scroll_into_view_if_needed()
    expect(page.locator("footer span")).to_have_text("© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED.")

    # Submit
    page.locator("#submit").click()

    # Модальное окно: проверка успешного отправления формы
    expect(page.locator("div.modal-content")).to_be_visible()
    expect(page.locator("#example-modal-sizes-title-lg")).to_have_text("Thanks for submitting the form")

    page.screenshot(path="screenshots/test_registration_form.png")
