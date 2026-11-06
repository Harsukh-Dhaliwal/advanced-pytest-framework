import os
import pytest
import allure
from playwright.sync_api import Page

# Define a strict matrix of enterprise responsive layouts to trace
VIEWPORT_MATRIX = {
    "Desktop_1080p": {"width": 1920, "height": 1080},
    "Tablet_Portrait": {"width": 768, "height": 1024},
    "Laptop_Medium": {"width": 1366, "height": 768}
}

@pytest.mark.parametrize("viewport_name, dimensions", VIEWPORT_MATRIX.items())
def test_application_viewport_resilience(page: Page, viewport_name, dimensions):
    """
    Advanced verification loop evaluating visual layout scalability 
    and DOM element responsiveness across variable viewport matrices.
    """
    # 1. Force the browser context to dynamically resize at runtime
    page.set_viewport_size({"width": dimensions["width"], "height": dimensions["height"]})
    
    # 2. Navigate to your target application (using a stable sandbox for practice)
    page.goto("https://example.com")
    
    # 3. Inject an Allure step to dynamically log the current dimension phase
    with allure.step(f"Verifying UI responsiveness on {viewport_name} ({dimensions['width']}x{dimensions['height']})"):
        # Assert that core container layout endpoints are active and stable
        body_element = page.locator("body")
        assert body_element.is_visible(), f"Core DOM body failed to render on viewport: {viewport_name}"
        
        # 4. Extract and log runtime inner dimensions to prove compliance
        actual_width = page.evaluate("window.innerWidth")
        assert actual_width == dimensions["width"], f"Viewport width mismatch on layout: {viewport_name}"
        
        # 5. Capture a contextual visual footprint for the Allure dashboard
        screenshot_bytes = page.screenshot(full_page=False)
        allure.attach(
            screenshot_bytes,
            name=f"LAYOUT_FOOTPRINT_{viewport_name}",
            attachment_type=allure.attachment_type.PNG
        )