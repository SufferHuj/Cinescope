from playwright.sync_api import Page, expect


def test_buttons(page: Page):
    """Тест работы с кнопками на странице Buttons"""
    
    page.goto("https://demoqa.com/buttons")

    page.get_by_role("button", name="Double Click Me").dblclick()
    expect(page.get_by_text("You have done a double click")).to_be_visible()

    page.get_by_role("button", name="Right Click Me").click(button="right")
    expect(page.get_by_text("You have done a right click")).to_be_visible()

    page.get_by_role("button", name="Click Me", exact=True).click()
    expect(page.get_by_text("You have done a dynamic click")).to_be_visible()

    page.screenshot(path="screenshots/test_buttons.png")
