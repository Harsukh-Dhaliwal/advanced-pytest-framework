import random
from typing import Dict, List, Tuple

class AlfredCore:
    def __init__(self):
        self.identity = "Alfred"
        self.version = "1.0.0"
        # A dictionary mapping to store Alfred's modular sub-neural networks
        self.cognitive_modules: Dict[str, dict] = {}

    def initialize_logic_module(self, module_name: str, input_size: int):
        """
        Instantiates an isolated, raw neural layer for a specific logic or classification task.
        """
        self.cognitive_modules[module_name] = {
            "weights": [random.uniform(-1, 1) for _ in range(input_size)],
            "bias": random.uniform(-1, 1),
            "learning_rate": 0.1
        }

    def _activation_step(self, x: float) -> int:
        """Internal step function for Alfred's decision binary thresholds."""
        return 1 if x >= 0 else 0

    def process_logic(self, module_name: str, inputs: List[float]) -> int:
        """
        Alfred's feed-forward processing node to calculate decisions based on learned weights.
        """
        if module_name not in self.cognitive_modules:
            raise ValueError(f"⚠️ Cognitive module '{module_name}' has not been initialized inside Alfred's brain.")

        module = self.cognitive_modules[module_name]
        total = sum(i * w for i, w in zip(inputs, module["weights"])) + module["bias"]
        return self._activation_step(total)

    def train_module(self, module_name: str, training_data: List[Tuple[List[float], int]], epochs: int):
        """
        Alfred's core learning loop (Backpropagation mechanism). 
        Allows Alfred to analyze mistakes, calculate error rates, and adjust weights on-the-fly.
        """
        if module_name not in self.cognitive_modules:
            raise ValueError(f"⚠️ Cognitive module '{module_name}' has not been initialized inside Alfred's brain.")

        module = self.cognitive_modules[module_name]
        
        for _ in range(epochs):
            for inputs, target_output in training_data:
                prediction = self.process_logic(module_name, inputs)
                error = target_output - prediction
                
                # If Alfred makes an error, dynamically adjust his neural connections
                if error != 0:
                    module["weights"] = [w + (module["learning_rate"] * error * i) for w, i in zip(module["weights"], inputs)]
                    module["bias"] += module["learning_rate"] * error

    def analyze_text_keywords(self, raw_text: str, top_n: int = 5) -> list[tuple[str, int]]:
        """
        Skill A: Natural Language Processing Module (v1.1.0).
        Parses raw text streams, strips structural punctuation/pronouns,
        and extracts keywords sorted by frequency density with alphabetical tie-breakers.
        """
        # Expanded enterprise stop-words list to filter out basic conversational pronouns
        stop_words = {
            "we", "are", "looking", "for", "a", "you", "must", "have", "strong", 
            "with", "the", "role", "requires", "and", "integrating", "into", "an",
            "experience", "knowledge", "skills", "job", "position", "preferred", "required"
        }
        
        # 1. Sanitize text: Convert case and strip standard terminal punctuation
        clean_text = raw_text.lower()
        for char in [".", ",", "!", "?", "(", ")", ":", ";", "-", "*", '"', "'", "\n"]:
            clean_text = clean_text.replace(char, " ")
            
        # 2. Tokenize: Split text into an array of isolated structural strings
        tokens = clean_text.split()
        
        # 3. Filter and Count: Filter out conversational filler and numeric characters
        keyword_counts = {}
        for token in tokens:
            if len(token) > 1 and not token.isdigit() and token not in stop_words:
                keyword_counts[token] = keyword_counts.get(token, 0) + 1
                
        # 4. Sorting Logic: Sort primarily by frequency (descending), 
        # then alphabetically (ascending) to maintain deterministic outputs
        sorted_keywords = sorted(
            keyword_counts.items(), 
            key=lambda item: (-item[1], item[0])
        )
        
        return sorted_keywords[:top_n]
    
if __name__ == "__main__":
    # Booting Alfred up locally
    alfred = AlfredCore()
    print(f"🤖 Core Framework Online: Welcome back, I am {alfred.identity} (v{alfred.version}).")
    
    # Initialize a module to teach Alfred the 'AND' gate classification rule
    print("🧠 Initializing Alfred's logical reasoning module...")
    alfred.initialize_logic_module(module_name="binary_logic_gate", input_size=2)
    
    and_gate_data = [
        ([0, 0], 0),
        ([1, 0], 0),
        ([0, 1], 0),
        ([1, 1], 1)
    ]
    
    print("⏳ Alfred is analyzing training data loops...")
    alfred.train_module(module_name="binary_logic_gate", training_data=and_gate_data, epochs=50)
    print("✅ Training complete. Alfred is fully optimized.")