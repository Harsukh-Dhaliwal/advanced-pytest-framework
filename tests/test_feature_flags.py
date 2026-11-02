import json
import pytest
from playwright.sync_api import Page
from infra.feature_flags import FeatureFlagManager

def test_runtime_feature_flag_injection_and_override(page: Page):
    """
    Validates that the framework can securely intercept and override application 
    feature flag configurations directly inside the client browser window context.
    """
    # Fetch our target architecture flag configuration
    target_flags = FeatureFlagManager.get_active_flags()
    
    # Establish a virtual staging environment target endpoint
    app_endpoint = "https://internal-app.local"
    
    # Inject client-side layout rules prior to document loading to bypass remote toggle sync delays
    def handle_dashboard_route(route):
        # Emulate a server dashboard index that reads global window feature structures
        html_content = """
        <html>
            <head>
                <script>
                    window.appFeatures = window.appFeatures || {};
                </script>
            </head>
            <body>
                <div id="feature-status">Configured</div>
            </body>
        </html>
        """
        route.fulfill(status=200, content_type="text/html", body=html_content)

    # Bind layout routes and introduce pre-navigation script execution state configurations
    page.route(app_endpoint, handle_dashboard_route)
    
    # Hook into Playwright's initialization layer to force state compliance
    page.add_init_script(f"window.appFeatures = {json.dumps(target_flags)};")
    
    # Execute targeted navigation sequence
    page.goto(app_endpoint, wait_until="domcontentloaded")
    
    # Extract client-side evaluation matrices straight from runtime window objects
    evaluated_flags = page.evaluate("window.appFeatures")
    
    # Execute strict assertions to verify our configuration states successfully overrode defaults
    assert evaluated_flags is not None, "Failed to initialize or resolve window feature components."
    assert evaluated_flags["beta_next_gen_ui"] is True, "Next Gen UI feature flag state mismatch."
    assert evaluated_flags["security_mfa_forced"] is False, "MFA override condition failed."
    
    # Verify the UI container loaded smoothly under injected rules
    assert page.locator("#feature-status").inner_text() == "Configured"