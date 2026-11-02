from playwright.sync_api import Page

class PerformanceAuditor:
    """
    Hooks into the client browser context to audit user-centric metrics.
    Captures native Core Web Vitals data points straight from execution pools.
    """
    
    @staticmethod
    def audit_core_vitals(page: Page) -> dict:
        """
        Queries browser performance entries to unpack metrics like 
        First Contentful Paint and total document processing overhead.
        """
        script = """
            (() => {
                const timings = window.performance.timing;
                const paintEntries = window.performance.getEntriesByType('paint');
                
                let fcp = 0;
                paintEntries.forEach((entry) => {
                    if (entry.name === 'first-contentful-paint') {
                        fcp = entry.startTime;
                    }
                });

                return {
                    "dom_interactive_ms": timings.domInteractive - timings.navigationStart,
                    "load_event_ms": timings.loadEventEnd - timings.navigationStart,
                    "first_contentful_paint_ms": fcp
                };
            })()
        """
        metrics = page.evaluate(script)
        return metrics if isinstance(metrics, dict) else {}