import json
import os

class ArchitectureGraphVisualizer:
    """
    Traces and maps structural dependencies across the testing ecosystem.
    Generates a structured map file of module-to-test interactions.
    """
    REPORT_PATH = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "logs", "framework_dependency_graph.json"
    ))

    @classmethod
    def register_dependency(cls, test_suite: str, core_modules: list):
        """Records an execution dependency map safely into a localized JSON payload."""
        os.makedirs(os.path.dirname(cls.REPORT_PATH), exist_ok=True)
        
        current_graph = {}
        if os.path.exists(cls.REPORT_PATH):
            try:
                with open(cls.REPORT_PATH, "r", encoding="utf-8") as f:
                    current_graph = json.load(f)
            except Exception:
                current_graph = {}

        # Append the tracked structural mapping array
        current_graph[test_suite] = {
            "dependencies_mapped": core_modules,
            "layer_classification": "E2E_Network_Interception_Grid"
        }

        with open(cls.REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(current_graph, f, indent=4)