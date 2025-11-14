from pathlib import Path
from playwright.sync_api import Page, expect
from utils.tools import Tools


def test_download_file(page: Page):
    """Тест проверяет возможность скачивания файла с помощью кнопки Download"""

    page.goto("https://demoqa.com/upload-download")

    with page.expect_download() as d:
        page.locator("#downloadButton").click()
    download = d.value
    filename = download.suggested_filename
    dest = Tools.files_dir("downloads", f"{Tools.get_timestamp()}_{filename}")
    download.save_as(str(dest))

    assert Path(dest).exists()
    assert Path(dest).stat().st_size > 0


def test_upload_file(page: Page):
    """Тест проверяет возможность загрузки файла с помощью кнопки Upload"""

    page.goto("https://demoqa.com/upload-download")

    tmp_file = Tools.files_dir("upload_tmp", "sample_upload.txt")
    Path(tmp_file).write_text("sample content")

    page.set_input_files("#uploadFile", str(tmp_file))
    expect(page.locator("#uploadedFilePath")).to_be_visible()
    expect(page.locator("#uploadedFilePath")).to_contain_text("sample_upload.txt")

    page.screenshot(path="screenshots/test_upload_download.png")
    