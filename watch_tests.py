import os
import subprocess
import sys
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class TestAutoRunnerHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_run = 0
        self.cooldown = 2.0  # Prevents multiple rapid triggers on a single save file save

    def on_modified(self, event):
        # Ignore directories
        if event.is_directory:
            return

        # Explicitly target Python files inside tests/ or pages/
        file_path = event.src_path
        if not file_path.endswith(".py"):
            return

        # Skip temporary files or allure results folder modifications
        if "allure" in file_path or ".pytest_cache" in file_path or "venv" in file_path:
            return

        current_time = time.time()
        if current_time - self.last_run < self.cooldown:
            return
            
        self.last_run = current_time
        self.execute_target_test(file_path)

    def execute_target_test(self, modified_file):
        print("\n" + "="*80)
        print(f"🔄 File Change Detected: {os.path.basename(modified_file)}")
        print("🚀 Executing Context-Aware Pytest Suite...")
        print("="*80 + "\n")

        # Smart Routing Logic
        # If a specific test file was modified, execute ONLY that file to save time.
        if "tests" in modified_file and "test_" in os.path.basename(modified_file):
            command = ["pytest", modified_file, "-v", "--tb=short"]
        else:
            # If a base helper or Page Object was modified, run the rapid regression suite
            command = ["pytest", "tests/", "-v", "--tb=short", "-q"]

        # Run command directly inside your active framework shell environment
        try:
            subprocess.run(command, check=False)
        except Exception as e:
            print(f"❌ Execution Engine Failure: {e}")

if __name__ == "__main__":
    path = "."  # Monitor current directory tree
    event_handler = TestAutoRunnerHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    
    print("\n⚡ Smart Watcher Engine Online!")
    print("▶️ Listening for code modifications across tests/ and pages/ modules...")
    print("📌 Press Ctrl+C to terminate the watcher loop.\n")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Watcher Engine shutting down safely.")
        observer.stop()
    observer.join()