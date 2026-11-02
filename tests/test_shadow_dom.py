import pytest
from playwright.sync_api import Page
from infra.shadow_piercer import ShadowDomPiercer

def test_shadow_dom_element_piercing_and_extraction(page: Page):
    """
    Validates the framework's capability to pierce component boundaries 
    and extract metrics from encapsulated web component shadow trees.
    """
    target_endpoint = "https://internal-components.local"
    
    def handle_shadow_component_route(route):
        html_content = """
        <html>
            <body>
                <custom-input-component id="host-element"></custom-input-component>
                
                <script>
                    // Instantiate a global registry to simulate an enterprise closed shadow reference hook
                    window.__closedShadowRegistry = {};

                    class CustomInputComponent extends HTMLElement {
                        constructor() {
                            super();
                            // Attach an encapsulated CLOSED shadow root node boundary
                            const shadow = this.attachShadow({ mode: 'closed' });
                            const container = document.createElement('div');
                            container.id = 'shadow-inner-target';
                            container.innerText = 'Encapsulated Secure Token Data';
                            shadow.appendChild(container);
                            
                            // Save reference to the closed registry
                            window.__closedShadowRegistry['host-element'] = shadow;
                        }
                    }
                    customElements.define('custom-input-component', CustomInputComponent);
                </script>
            </body>
        </html>
        """
        route.fulfill(status=200, content_type="text/html", body=html_content)

    # Route and initialize the isolated rendering layout
    page.route(target_endpoint, handle_shadow_component_route)
    page.goto(target_endpoint, wait_until="domcontentloaded")
    
    # Assert that standard flat-DOM locator lookups return false/empty on closed shadow assets
    standard_locator = page.locator("#shadow-inner-target")
    assert standard_locator.is_visible() is False, "Standard flat locator incorrectly penetrated a closed shadow node."
    
    # Pierce the closed shadow root boundary programmatically via our custom registry hook
    extracted_text = ShadowDomPiercer.extract_closed_shadow_text(
        page=page, 
        host_id="host-element"
    )
    
    # Verify the deep text data matches architectural data properties perfectly
    assert extracted_text == "Encapsulated Secure Token Data", f"Expected shadow data, but captured: '{extracted_text}'"