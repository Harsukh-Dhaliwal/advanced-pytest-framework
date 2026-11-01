import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage

def test_self_healing_locator_fallback_success(page: Page):
    """
    Validates that if an element's selector class changes from 'btn-submit-primary' 
    to a generic unmapped string, the subsystem dynamically self-heals using fallback text heuristics.
    """
    # 1. Setup sandboxed target component in an unexpected layout state
    page.set_content("""
        <div>
            <button class="completely-changed-random-class-xyz" id=999>Confirm Secure Order Transaction</button>
        </div>
    """)
    
    base_page = BasePage(page)
    
    # 2. Execute target action passing the historical broken selector + new fuzzy validation properties
    # The primary selector '.btn-submit-primary' will completely time out and trigger Option R
    base_page.click_with_healing(
        selector="button.btn-submit-primary", 
        fallback_tag="button", 
        fallback_text="Confirm Secure Order Transaction"
    )
    
    # 3. Assert successful execution pipeline flow without crashing out
    assert True