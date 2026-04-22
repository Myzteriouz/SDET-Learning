from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

class StealthBrowser:
    async def get_context(self, p, headless=False):
        # Using a persistent directory keeps you logged into LinkedIn
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./browser_session",
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        page = context.pages[0]
        await stealth_async(page)
        return context, page