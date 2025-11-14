from playwright.sync_api import Page, expect


def test_webtables(page: Page):
    """Тест работы с веб-таблицей на странице Web Tables"""
    
    page.goto("https://demoqa.com/webtables")
    
    page.locator("button#addNewRecordButton").click()
    expect(page.locator(".modal-title#registration-form-modal:has-text('Registration Form')")).to_be_visible()
    expect(page.locator(".modal-body #userForm")).to_be_visible()

    page.locator("input[placeholder='First Name']").fill("Ivan")
    page.fill("#lastName", "Ivanov")
    page.fill("#userEmail", "tester@gmail.com")
    page.fill("#age", "30")
    page.fill("#salary", "150000")
    page.fill("#department", "IT")

    page.locator("button#submit").click()

    expect(page.get_by_role("gridcell", name="Ivan", exact=True)).to_be_visible()
    expect(page.get_by_role("gridcell", name="Ivanov", exact=True)).to_be_visible()
    expect(page.get_by_role("gridcell", name="tester@gmail.com", exact=True)).to_be_visible()
    expect(page.get_by_role("gridcell", name="30", exact=True)).to_be_visible()
    expect(page.get_by_role("gridcell", name="150000", exact=True)).to_be_visible()
    expect(page.get_by_role("gridcell", name="IT", exact=True)).to_be_visible()

    page.screenshot(path="screenshots/test_webtables.png")
