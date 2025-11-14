from playwright.sync_api import Page, expect


def test_checkbox_visibility(page: Page):
    """Тест проверки видимости чекбоксов на странице Check Box"""

    page.goto("https://demoqa.com/checkbox")

    expect(page.locator("span.rct-title").filter(has_text="Home")).to_be_visible()
    expect(page.locator("span.rct-title").filter(has_text="Desktop")).not_to_be_visible()

    page.get_by_role("button", name="Toggle").click()

    expect(page.locator("span.rct-title").filter(has_text="Desktop")).to_be_visible()
    expect(page.locator("span.rct-title").filter(has_text="Commands")).not_to_be_visible()

    page.screenshot(path="screenshots/test_checkbox_1.png")

def test_checkbox_select_all(page: Page):
    """Тест выбора всех чекбоксов"""

    page.goto("https://demoqa.com/checkbox")

    page.locator("span.rct-title").filter(has_text="Home").click()

    expected = [
        "home", "desktop", "notes", "commands",
        "documents", "workspace", "react", "angular", "veu",
        "office", "public", "private", "classified", "general",
        "downloads", "wordFile", "excelFile"
    ]

    expect(page.locator("#result")).to_be_visible()
    result_items = page.locator("#result .text-success")
    expect(result_items).to_have_text(expected)

    page.screenshot(path="screenshots/test_checkbox_2.png")

def test_checkbox_select_desktop(page: Page):
    """Тест выбора чекбоксов через Expand all"""

    page.goto("https://demoqa.com/checkbox")

    # Раскрываем все узлы дерева
    page.get_by_role("button", name="Expand all").click()

    page.locator("span.rct-title").filter(has_text="Desktop").click()

    expect(page.locator("#result")).to_be_visible()
    expect(page.locator("#result span")).to_have_text(["You have selected :", "desktop", "notes", "commands"])

    page.screenshot(path="screenshots/test_checkbox_3.png")


def test_checkbox_select_downloads_word(page: Page):
    """Тест выбора чекбокса Word File.doc через тогглы"""

    page.goto("https://demoqa.com/checkbox")
    # Вспомогательная функция: раскрыть узел дерева по заголовку
    def toggle(title: str):
        label = page.locator("label").filter(
            has=page.locator("span.rct-title", has_text=title)
        )
        label.locator(
            "xpath=preceding-sibling::button[contains(@class,'rct-collapse')]"
        ).click()

    # Раскрываем нужные узлы
    toggle("Home")
    toggle("Downloads")

    page.locator("span.rct-title").filter(has_text="Word File.doc").click()
    
    expect(page.locator("#result")).to_contain_text("wordFile")

    page.screenshot(path="screenshots/test_checkbox_4.png")
    