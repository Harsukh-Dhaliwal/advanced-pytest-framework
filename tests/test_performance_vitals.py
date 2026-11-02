import pytest
from playwright.sync_api import Page
from infra.performance_auditor import PerformanceAuditor

def test_client_side_performance_core_vitals_audit(page: Page):
    """
    Validates the framework's capability to profile client execution tracks,
    extracting performance metrics straight from browser navigation windows.
    """
    target_endpoint = "https://internal-app.local"
    
    # Establish a simulated UI index that includes heavy asset rendering delays
    def handle_performance_route(route):
        html_content = """
        <html>
            <head>
                <script>
                    // Simulate client-side paint entries inside the browser engine
                    setTimeout(() => {
                        window.performance.mark('first-contentful-paint');
                    }, 50);
                </script>
            </head>
            <body>
                <main id="app-container">
                    <h1>Enterprise Real-Time Analytics</h1>
                </main>
            </body>
        </html>
        """
        route.fulfill(status=200, content_type="text/html", body=html_content)

    # Route and load the targeted app layout
    page.route(target_endpoint, handle_performance_route)
    page.goto(target_endpoint, wait_until="load")
    
    # Extract client performance attributes via the auditor component
    vitals = PerformanceAuditor.audit_core_vitals(page)
    
    # Verify the telemetry data contains all structural performance tracks
    assert vitals is not None, "Performance auditor failed to extract data from window context."
    assert "dom_interactive_ms" in vitals, "DOM Interactive metric field missing."
    assert "load_event_ms" in vitals, "Load Event Completion metric field missing."
    assert "first_contentful_paint_ms" in vitals, "First Contentful Paint track missing."
    
    # Enforce basic sanity guardrails on the returned timings
    assert vitals["dom_interactive_ms"] >= 0, "Invalid negative DOM interaction time detected."