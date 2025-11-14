from playwright.sync_api import Page, expect


def test_radio_button(page: Page):
    """Тест выбора радиокнопки на странице Radio Button"""

    page.goto("https://demoqa.com/radio-button")

    page.locator("label[for='yesRadio']").click()
    expect(page.get_by_text("You have selected Yes")).to_be_visible()

    page.locator("label[for='impressiveRadio']").click()
    expect(page.get_by_text("You have selected Impressive")).to_be_visible()

    expect(page.get_by_role("radio", name="No")).to_be_disabled()

    page.screenshot(path="screenshots/test_radio_button.png")
