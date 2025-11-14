from playwright.sync_api import Page, expect


def test_slider_move(page: Page):
    """Тест движения слайдера: 0 → 100 → 55"""

    page.goto("https://demoqa.com/slider")

    slider = page.locator("input[type=range]")
    slider_value = page.locator("#sliderValue")

    # Стартовое значение — 50
    slider.focus()
    page.keyboard.press("Home")
    for _ in range(50):
        page.keyboard.press("ArrowRight")
    expect(slider_value).to_have_value("50")

    # Значение до 0
    page.keyboard.press("Home")
    expect(slider_value).to_have_value("0")

    # Значение до 100
    page.keyboard.press("End")
    expect(slider_value).to_have_value("100")

    # Значение до 55
    page.keyboard.press("Home")
    for _ in range(55):
        page.keyboard.press("ArrowRight")
    expect(slider_value).to_have_value("55")

    
    expect(page.get_by_role("slider")).to_be_visible()
    expect(page.get_by_role("slider")).to_have_value("55")
    # Значение в 0
    page.get_by_role("slider").fill("0")
    expect(slider_value).to_have_value("0")

    page.screenshot(path="screenshots/test_slider.png")