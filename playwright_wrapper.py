from playwright.sync_api import sync_playwright, TimeoutError
def generate_character(BASE_URL):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.wait_for_selector('canvas', timeout=2000)
        page.wait_for_timeout(1000)
        with page.expect_download(timeout=5000) as download_info:
            page.locator('text=Spritesheet (PNG)').first.click()
        download = download_info.value
        download.save_as("output_filename.png")
        browser.close()
