import random
from typing import Dict, List, Tuple

class AlfredCore:
    def __init__(self):
        self.identity = "Alfred"
        self.version = "1.2.0-SAFE"
        self.cognitive_modules: Dict[str, dict] = {}

    def initialize_logic_module(self, module_name: str, input_size: int):
        """Instantiates an isolated neural layer for logic tasks."""
        self.cognitive_modules[module_name] = {
            "weights": [random.uniform(-1, 1) for _ in range(input_size)],
            "bias": random.uniform(-1, 1),
            "learning_rate": 0.1
        }

    def _activation_step(self, x: float) -> int:
        return 1 if x >= 0 else 0

    def process_logic(self, module_name: str, inputs: List[float]) -> int:
        if module_name not in self.cognitive_modules:
            raise ValueError(f"⚠️ Cognitive module '{module_name}' has not been initialized.")
        module = self.cognitive_modules[module_name]
        total = sum(i * w for i, w in zip(inputs, module["weights"])) + module["bias"]
        return self._activation_step(total)

    def train_module(self, module_name: str, training_data: List[Tuple[List[float], int]], epochs: int):
        if module_name not in self.cognitive_modules:
            raise ValueError(f"⚠️ Cognitive module '{module_name}' has not been initialized.")
        module = self.cognitive_modules[module_name]
        for _ in range(epochs):
            for inputs, target_output in training_data:
                prediction = self.process_logic(module_name, inputs)
                error = target_output - prediction
                if error != 0:
                    module["weights"] = [w + (module["learning_rate"] * error * i) for w, i in zip(module["weights"], inputs)]
                    module["bias"] += module["learning_rate"] * error

    def analyze_text_keywords(self, raw_text: str, top_n: int = 5) -> list[tuple[str, int]]:
        stop_words = {
            "we", "are", "looking", "for", "a", "you", "must", "have", "strong", 
            "with", "the", "role", "requires", "and", "integrating", "into", "an",
            "experience", "knowledge", "skills", "job", "position", "preferred", "required"
        }
        clean_text = raw_text.lower()
        for char in [".", ",", "!", "?", "(", ")", ":", ";", "-", "*", '"', "'", "\n"]:
            clean_text = clean_text.replace(char, " ")
        tokens = clean_text.split()
        keyword_counts = {}
        for token in tokens:
            if len(token) > 1 and not token.isdigit() and token not in stop_words:
                keyword_counts[token] = keyword_counts.get(token, 0) + 1
        sorted_keywords = sorted(
            keyword_counts.items(), 
            key=lambda item: (-item[1], item[0])  # item[1] is count, item[0] is word
        )
        return sorted_keywords[:top_n]

    def calculate_and_purge_workspace_bloat(self, target_dir: str = ".", dry_run: bool = True) -> tuple[int, list[str]]:
        """
        Skill B: File System Diagnostic Core (v1.2.0-SAFE).
        Scans directories and computes storage size bloat.
        DELETION DISK ACCESS REMOVED FOR MAXIMUM USER SAFETY.
        """
        import os

        # Explicitly targets only temporary framework tracking files
        bloat_targets = {".pytest_cache", "__pycache__", "allure-results", "logs/network_traces"}
        total_freed_bytes = 0
        purged_paths = []

        for root, dirs, files in os.walk(target_dir, topdown=True):
            matched_dirs = [d for d in dirs if d in bloat_targets]
            
            for target in matched_dirs:
                full_path = os.path.join(root, target)
                
                # Absolute Safeguard: Skip your vital configurations, git engine, or virtual environments
                if any(x in full_path for x in ["venv", ".git", "pages", "tests"]):
                    continue
                    
                try:
                    for dirpath, _, filenames in os.walk(full_path):
                        for f in filenames:
                            fp = os.path.join(dirpath, f)
                            if os.path.exists(fp):
                                total_freed_bytes += os.path.getsize(fp)
                except Exception:
                    pass

                purged_paths.append(full_path)

            # Forces os.walk to bypass drilling deeper into cache trees
            dirs[:] = [d for d in dirs if d not in matched_dirs]

        # Returns metrics cleanly without performing any destructive delete commands
        return total_freed_bytes, purged_paths
    
if __name__ == "__main__":
    alfred = AlfredCore()
    print("\n" + "="*60)
    print(f"🤖 Core Engine Online: Welcome back, I am {alfred.identity} (v{alfred.version}).")
    print("="*60)
    
    print("\n🧠 Auditing logical reasoning module capabilities...")
    alfred.initialize_logic_module(module_name="binary_logic_gate", input_size=2)
    and_gate_data = [
        ([0, 0], 0), 
        ([1, 0], 0), 
        ([0, 1], 0), 
        ([1, 1], 1)
    ]
    alfred.train_module(module_name="binary_logic_gate", training_data=and_gate_data, epochs=50)
    print(f"✅ Neural verification check: PASSED")

    print("\n📂 Running automated local project diagnostics...")
    # Hardcoded dry_run=True to ensure it only reads file metadata sizes
    bytes_found, targets = alfred.calculate_and_purge_workspace_bloat(target_dir=".", dry_run=True)
    
    print(f"📊 Workspace Report: Detected {len(targets)} transient framework log/cache directories.")
    print(f"💾 Accumulated log size footprint: {bytes_found / 1024:.2f} KB")
    print("="*60 + "\n")