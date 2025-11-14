from playwright.sync_api import Page, expect


def test_links_open_new_tab(page: Page):
    """Тест проверяет возможность открытия ссылки в новой вкладке"""

    page.goto("https://demoqa.com/links")

    with page.expect_popup() as p1:
        page.get_by_role("link", name="Home", exact=True).click()
    new_tab1 = p1.value
    new_tab1.wait_for_load_state()
    expect(new_tab1).to_have_url("https://demoqa.com/")

    page.locator("#dynamicLink").scroll_into_view_if_needed()
    with page.expect_popup() as p2:
        page.locator("#dynamicLink").click()
    new_tab2 = p2.value
    new_tab2.wait_for_load_state()
    expect(new_tab2).to_have_url("https://demoqa.com/")


def test_links_api_responses(page: Page):
    """Тест проверяет коды ответа API для ссылок"""

    page.goto("https://demoqa.com/links")

    codes = {
        "Created": 201,
        "No Content": 204,
        "Moved": 301,
        "Bad Request": 400,
        "Unauthorized": 401,
        "Forbidden": 403,
        "Not Found": 404,
    }

    for link_name, code in codes.items():
        page.get_by_role("link", name=link_name).click()
        page.locator("#linkResponse").scroll_into_view_if_needed()
        expect(page.locator("#linkResponse")).to_be_visible()
        expect(page.locator("#linkResponse")).to_contain_text(str(code))

    page.screenshot(path='screenshots/test_links_api_responses.png')