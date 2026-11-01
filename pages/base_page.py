from playwright.sync_api import Page, Locator
from infra.self_healing import SelfHealingLocator

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.healer = SelfHealingLocator(page)

    def click_with_healing(self, selector: str, fallback_tag: str, fallback_text: str, timeout: int = 5000):
        """Attempts a standard explicit click; falls back to fuzzy healing on failure."""
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
        except Exception:
            healed_locator = self.healer.find_healed_element(
                target_tag=fallback_tag, 
                fallback_text=fallback_text, 
                broken_selector=selector
            )
            healed_locator.click()

    def fill_with_healing(self, selector: str, value: str, fallback_tag: str, fallback_text: str, timeout: int = 5000):
        """Attempts an input fill operation; runs fuzzy healing if target selectors change."""
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout)
            locator.fill(value)
        except Exception:
            healed_locator = self.healer.find_healed_element(
                target_tag=fallback_tag, 
                fallback_text=fallback_text, 
                broken_selector=selector
            )
            healed_locator.fill(value)