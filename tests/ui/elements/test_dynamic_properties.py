from playwright.sync_api import Page, expect


def test_dynamic_properties(page: Page):
    """Тест проверяет динамические свойства элементов"""

    page.goto("https://demoqa.com/dynamic-properties")

    expect(page.get_by_role("heading", name="Dynamic Properties")).to_be_visible()
    expect(page.locator("#enableAfter")).to_be_enabled(timeout=10000)

    page.wait_for_selector("#visibleAfter", state="visible")  

    expect(page.locator("#visibleAfter")).to_be_visible()
    expect(page.get_by_role("button", name="Visible After 5 Seconds")).to_be_visible()

    page.screenshot(path="screenshots/test_dynamic_properties.png")
