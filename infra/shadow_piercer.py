from playwright.sync_api import Page

class ShadowDomPiercer:
    """
    Evaluates and pierces web component Shadow DOM boundaries.
    Allows locator lookups to penetrate encapsulated shadow tree layers seamlessly.
    """
    
    @staticmethod
    def extract_closed_shadow_text(page: Page, host_id: str) -> str:
        """
        Executes a low-level JavaScript context evaluation to extract text data
        from modern components protected inside closed shadow root boundaries.
        """
        # Accesses the closed storage registry established during initialization
        script = f"""
            (() => {{
                if (window.__closedShadowRegistry && window.__closedShadowRegistry['{host_id}']) {{
                    const root = window.__closedShadowRegistry['{host_id}'];
                    const target = root.querySelector('#shadow-inner-target');
                    return target ? target.innerText : null;
                }}
                return null;
            }})()
        """
        result = page.evaluate(script)
        return str(result) if result else ""