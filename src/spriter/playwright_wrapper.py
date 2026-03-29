from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError

DEFAULT_TIMEOUT = 6000
CANVAS_SELECTOR = "canvas"
DOWNLOAD_BUTTON = 'text=Spritesheet (PNG)'


class SpriteDownloader:
    def __init__(
        self,
        base_url,
        headless=True,
        timeout=DEFAULT_TIMEOUT,
        output_dir="generated_spritesheets"
    ):
        self.base_url = base_url
        self.headless = headless
        self.timeout = timeout
        self.output_dir = Path(output_dir)

        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    # context manager support
    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc, tb):
        self.close()

    # ---------- lifecycle ----------

    def start(self):
        """Start browser once"""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=self.headless
        )

        self._context = self._browser.new_context(
            accept_downloads=True
        )

        self._page = self._context.new_page()

        return self


    def close(self):
        """Clean shutdown"""
        if self._browser:
            self._browser.close()

        if self._playwright:
            self._playwright.stop()


    # ---------- core functionality ----------

    def download_sprite(self, url, filename):
        """
        download one sprite
        url should already contain parameters
        """

        output_path = self.output_dir / filename

        self._page.goto(
            url,
            wait_until="domcontentloaded"
        )

        # wait for rendering
        self._page.wait_for_selector(
            CANVAS_SELECTOR,
            timeout=self.timeout
        )

        self._page.wait_for_timeout(800)

        with self._page.expect_download(
            timeout=self.timeout
        ) as download_info:

            self._page.locator(DOWNLOAD_BUTTON).first.click()

        download = download_info.value
        download.save_as(output_path)

        return output_path


    # ---------- batch mode ----------

    def batch_download(self, urls, filenames=None):
        """
        urls: iterable[str]
        filenames: iterable[str] or None

        returns list[path]
        """

        results = []

        if filenames is None:
            filenames = [
                f"sprite_{i}.png"
                for i in range(len(urls))
            ]

        for url, name in zip(urls, filenames):

            try:
                path = self.download_sprite(url, name)
                results.append(path)

            except TimeoutError:
                print(f"timeout: {url}")

        return results


# ---------- convenience function ----------

def download_many(urls, filenames=None, **kwargs):

    with SpriteDownloader(**kwargs).start() as d:
        return d.batch_download(urls, filenames)
