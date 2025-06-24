import logging

from playwright.async_api import async_playwright, Page, Browser


logger = logging.getLogger(__name__)


class AsyncPlaywrightManager:
    def __init__(self):
        self._playwright = None
        self.browser: Browser | None = None
        self.page: Page | None = None

    async def __aenter__(self) -> Page:
        self._playwright = await async_playwright().start()
        self.browser = await self._playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()
        logger.info("Playwright браузер запущен")
        return self.page

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()
        logger.info("Playwright браузер закрыт")
