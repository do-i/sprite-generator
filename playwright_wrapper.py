from playwright.sync_api import sync_playwright, TimeoutError

# Your character URL (you can change parameters easily)
BASE_URL = "http://localhost:8000/#?body=Body_Color_fur_black&head=Skeleton_skeleton&hair=Bunches_purple&legs=Leggings_pink&facial_right=Right_Monocle_gold&prosthesis_hand=Hook_hand_hook&sex=male"
SPRITE_NAME = 'zombie1'
def generate_character(output_filename=f"generated_spritesheets/{SPRITE_NAME}.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)   # Change to True once everything is stable
        page = browser.new_page()

        page.goto(BASE_URL, wait_until="domcontentloaded")

        # Wait for canvas and rendering
        page.wait_for_selector('canvas', timeout=2000)
        page.wait_for_timeout(1000)   # Important for full compositing

        # Click download with robust selector

        with page.expect_download(timeout=5000) as download_info:
            page.locator('text=Spritesheet (PNG)').first.click()

        download = download_info.value
        download.save_as(output_filename)

        print(f"✅ Success! Saved as: {output_filename}")

        browser.close()

generate_character()