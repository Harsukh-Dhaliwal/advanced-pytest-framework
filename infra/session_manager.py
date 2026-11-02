import json
import os

class SessionStateManager:
    """
    Manages client storage state preservation profiles for multi-role workflows.
    Caches cookies and localStorage values into isolated JSON state snapshots.
    """
    CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".session_cache"))

    @classmethod
    def save_session_state(cls, role_name: str, state_data: dict) -> str:
        """Saves a user persona's storage state into an isolated cache block."""
        if not os.path.exists(cls.CACHE_DIR):
            os.makedirs(cls.CACHE_DIR, exist_ok=True)
            
        file_path = os.path.join(cls.CACHE_DIR, f"state_{role_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        return file_path

    @classmethod
    def load_session_state(cls, role_name: str) -> dict:
        """Retrieves a pre-cached storage profile map for injection."""
        file_path = os.path.join(cls.CACHE_DIR, f"state_{role_name}.json")
        if not os.path.exists(file_path):
            # Fallback placeholder matrix if cache is fresh or empty
            return {
                "cookies": [{"name": "session_token", "value": f"mock_token_{role_name}", "domain": "app.local", "path": "/"}],
                "origins": [{"origin": "https://app.local", "localStorage": [{"name": "user_role", "value": role_name}]}]
            }
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)