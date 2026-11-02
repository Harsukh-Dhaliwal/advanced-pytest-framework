import pytest
from playwright.sync_api import Browser, Page
from infra.session_manager import SessionStateManager

def test_multi_role_context_preservation_and_switching(browser: Browser):
    """
    Validates the framework's capability to provision separate user contexts,
    cache runtime session states, and restore them to completely bypass login screens.
    """
    # Define our target application routes
    app_url = "https://app.local"
    
    # --- PHASE 1: Capture Admin Persona Session State ---
    admin_context = browser.new_context()
    admin_page = admin_context.new_page()
    
    # Establish mock dashboard response matching the expected storage criteria
    def handle_auth_routes(route):
        html_content = "<html><body><div id='role-element'>Loaded</div></body></html>"
        route.fulfill(status=200, content_type="text/html", body=html_content)
        
    admin_page.route(app_url, handle_auth_routes)
    admin_page.goto(app_url, wait_until="commit")
    
    # Seed client-side states programmatically
    admin_page.evaluate("window.localStorage.setItem('user_role', 'Administrator');")
    
    # Extract and store the complete state profile map safely via the manager
    admin_state = admin_context.storage_state()
    SessionStateManager.save_session_state("admin_persona", admin_state)
    admin_context.close()
    
    # --- PHASE 2: Inject and Restore Pre-cached Admin Persona State ---
    restored_state = SessionStateManager.load_session_state("admin_persona")
    
    # Launch an entirely isolated browser context pre-seeded with the cached state map
    active_context = browser.new_context(storage_state=restored_state)
    active_page = active_context.new_page()
    active_page.route(app_url, handle_auth_routes)
    
    # Navigate instantly to secure paths
    active_page.goto(app_url, wait_until="domcontentloaded")
    
    # Validate the context successfully maintained injected state cookies/localStorage values
    extracted_role = active_page.evaluate("window.localStorage.getItem('user_role');")
    assert extracted_role == "Administrator", f"Expected 'Administrator' context state, but got: {extracted_role}"
    assert active_page.locator("#role-element").is_visible() is True
    
    active_context.close()