import random
import math
from typing import Dict, List, Tuple

class AlfredCore:
    def __init__(self):
        self.identity = "Alfred"
        self.version = "2.0.0-Conversational"
        self.cognitive_modules: Dict[str, dict] = {}

        # Conversational Memory Buffer: Keeps track of recent dialogue interactions
        self.conversation_history: list[dict] = []
        
        self.portfolio_skills = {
            "python", "pytest", "playwright", "docker", "git", "github", "actions", 
            "cicd", "allure", "automation", "framework", "database", "sql", "sqlite",
            "encryption", "fernet", "conftest", "pom", "mocking", "api", "json", "rest",
            "multithreading", "mutex", "lock", "screenshot", "logs", "trace", "har"
        }

        # Conversational Core: Mapping commands to a matrix of semantic synonyms
        self.intent_training_matrix = {
            "diagnose": ["diagnose", "scan", "check disk", "folder footprint", "workspace bloat", "clean system", "check cache", "storage space"],
            "analyze": ["analyze text", "parse keywords", "density matrix", "extract terms", "word count", "analyze posting", "check tokens"],
            "audit": ["audit resume", "match portfolio", "ats check", "compatibility score", "missing keywords", "evaluate job", "resume alignment"],
            "exit": ["exit", "quit", "power down", "goodnight alfred", "shutdown", "close session", "bye"]
        }

    def _text_to_vector(self, text: str) -> Dict[str, int]:
        """Converts raw text into a frequency coordinate vector mapping."""
        clean = text.lower().strip()
        for char in [".", ",", "!", "?", "-", "_"]:
            clean = clean.replace(char, " ")
        words = clean.split()
        vector = {}
        for word in words:
            vector[word] = vector.get(word, 0) + 1
        return vector

    def _calculate_cosine_similarity(self, vec1: Dict[str, int], vec2: Dict[str, int]) -> float:
        """
        Mathematical Cosine Similarity Node.
        Calculates the angular dot-product distance between two text vectors 
        to measure semantic meaning proximity from 0.0 (unrelated) to 1.0 (identical).
        """
        intersection = set(vec1.keys()) & set(vec2.keys())
        if not intersection:
            return 0.0
            
        dot_product = sum(vec1[x] * vec2[x] for x in intersection)
        
        sum1 = sum(vec1[x]**2 for x in vec1.keys())
        sum2 = sum(vec2[x]**2 for x in vec2.keys())
        magnitude = math.sqrt(sum1) * math.sqrt(sum2)
        
        return float(dot_product) / magnitude if magnitude else 0.0

    def resolve_conversational_intent(self, user_sentence: str) -> str:
        """
        Alfred's Central Intent Classifier (v2.1.0-Memory Enhanced).
        Evaluates sentences using vector math while checking the conversation history
        buffer to catch task corrections dynamically.
        """
        user_vector = self._text_to_vector(user_sentence)
        clean_input = user_sentence.lower().strip()
        
        # 1. CONVERSATIONAL CORRECTION GUARD: Catch negation adjustments on-the-fly
        if any(negation in clean_input for negation in ["no not", "instead", "wrong", "wait"]):
            # Inspect what task Alfred just executed previously
            if self.conversation_history:
                last_interaction = self.conversation_history[-1]
                if last_interaction["intent"] == "diagnose" and any(word in clean_input for word in ["audit", "resume", "job"]):
                    return "audit"
                if last_interaction["intent"] == "audit" and any(word in clean_input for word in ["diagnose", "folder", "scan"]):
                    return "diagnose"

        # 2. Standard Mathematical Vector Resolution
        highest_score = 0.0
        matched_intent = "unknown"

        for intent, expressions in self.intent_training_matrix.items():
            for expression in expressions:
                expression_vector = self._text_to_vector(expression)
                score = self._calculate_cosine_similarity(user_vector, expression_vector)
                
                if score > highest_score:
                    highest_score = score
                    matched_intent = intent

        return matched_intent if highest_score >= 0.15 else "unknown"

    def initialize_logic_module(self, module_name: str, input_size: int):
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
            "experience", "knowledge", "skills", "job", "position", "preferred", "required",
            "or", "in", "on", "to", "of", "as", "by", "at", "be", "such", "like", "using"
        }
        clean_text = raw_text.lower()
        for char in [".", ",", "!", "?", "(", ")", ":", ";", "-", "*", '"', "'", "\n"]:
            clean_text = clean_text.replace(char, " ")
        tokens = clean_text.split()
        keyword_counts = {}
        for token in tokens:
            if len(token) > 1 and not token.isdigit() and token not in stop_words:
                keyword_counts[token] = keyword_counts.get(token, 0) + 1
        sorted_keywords = sorted(keyword_counts.items(), key=lambda item: (-item[1], item[0]))
        return sorted_keywords[:top_n]

    def calculate_and_purge_workspace_bloat(self, target_dir: str = ".", dry_run: bool = True) -> tuple[int, list[str]]:
        import os
        bloat_targets = {".pytest_cache", "__pycache__", "allure-results", "logs/network_traces"}
        total_freed_bytes = 0
        purged_paths = []
        for root, dirs, files in os.walk(target_dir, topdown=True):
            matched_dirs = [d for d in dirs if d in bloat_targets]
            for target in matched_dirs:
                full_path = os.path.join(root, target)
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
            dirs[:] = [d for d in dirs if d not in matched_dirs]
        return total_freed_bytes, purged_paths

    def audit_resume_match(self, job_description: str) -> tuple[float, list[str], list[str]]:
        clean_text = job_description.lower()
        for char in [".", ",", "!", "?", "(", ")", ":", ";", "-", "*", '"', "'", "\n", "/"]:
            clean_text = clean_text.replace(char, " ")
        job_tokens = set(clean_text.split())
        matched_keywords = list(self.portfolio_skills.intersection(job_tokens))
        common_tech_requirements = {"java", "selenium", "aws", "jenkins", "kubernetes", "cucumber", "appium", "ci/cd", "sql"}
        required_by_job = common_tech_requirements.intersection(job_tokens)
        missing_keywords = list(required_by_job.difference(self.portfolio_skills))
        match_percentage = (len(matched_keywords) / (len(matched_keywords) + len(missing_keywords))) * 100 if (len(matched_keywords) + len(missing_keywords)) > 0 else 100.0
        return round(match_percentage, 2), sorted(matched_keywords), sorted(missing_keywords)

if __name__ == "__main__":
    import sys
    alfred = AlfredCore()
    print("\n" + "="*60)
    print(f"🤖 [System Boot Complete]: Hello! I am {alfred.identity} (v{alfred.version}).")
    print("🧠 Semantic Intent Engine is live. Speak to me naturally, sir.")
    print("="*60)

    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            if not user_input: 
                continue
            
            intent = alfred.resolve_conversational_intent(user_input)

            # Log the current dialogue state into Alfred's memory buffer
            alfred.conversation_history.append({"user_input": user_input, "intent": intent})
            
            if intent == "exit":
                print(f"\n🤖 {alfred.identity}: Goodnight, sir. Powering down memory matrix modules.")
                print("="*60 + "\n")
                sys.exit(0)
                
            elif intent == "diagnose":
                print(f"\n🤖 {alfred.identity}: Scanning workspace folder footprints safely...")
                bytes_found, targets = alfred.calculate_and_purge_workspace_bloat(target_dir=".", dry_run=True)
                print(f"📊 Framework Report: Located {len(targets)} active cache trees.")
                print(f"💾 Accumulated size footprint: {bytes_found / 1024:.2f} KB")
                
            elif intent == "analyze":
                print(f"\n🤖 {alfred.identity}: Understood. Paste text below (Press Enter twice when finished):")
                lines = []
                while True:
                    line = input()
                    if line == "": 
                        break
                    lines.append(line)
                raw_text = "\n".join(lines)
                if not raw_text.strip(): 
                    continue
                keywords = alfred.analyze_text_keywords(raw_text, top_n=5)
                print("\n📊 Top 5 High-Density Technical Keywords Extracted:")
                for rank, (word, count) in enumerate(keywords, start=1):
                    print(f"   [{rank}] {word} -> Mentioned {count} time(s)")
                    
            elif intent == "audit":
                print(f"\n🤖 {alfred.identity}: Ready to audit. Paste the job text description below")
                print("📝 (Press Enter twice when finished):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                target_job_text = "\n".join(lines)
                if not target_job_text.strip():
                    continue
                score, matched, missing = alfred.audit_resume_match(target_job_text)
                print("\n" + "-"*40)
                print(f"📊 ALFRED ATS MATCH SCORE: {score}%")
                print("-"*40)
                print(f"✅ Portfolio Strengths Identified: {', '.join(matched) if matched else 'None'}")
                print(f"🚨 Missing Keywords Flagged by ATS: {', '.join(missing) if missing else 'None'}")
                print("-"*40)
                
            else:
                print(f"\n🤖 {alfred.identity}: I can hear you, sir, but my semantic confidence threshold was not met.")
                print("💡 Try phrases like: 'check my folder footprint', 'parse text', or 'audit a job description'.")
                
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n🤖 {alfred.identity}: Session interrupted. Powering down safely.")
            break
