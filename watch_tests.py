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
        self.cooldown = 2.0  # Settle time
        self.is_running = False  # Explicit execution lock guard

    def on_modified(self, event):
        # 1. INSTANT DROP: If a test suite is already running, completely ignore all file changes
        if self.is_running:
            return

        if event.is_directory:
            return

        file_path = event.src_path
        if not file_path.endswith(".py"):
            return

        # Explicitly skip internal caches, environment properties, and virtual environments
        if any(x in file_path for x in ["allure", ".pytest_cache", "venv", "__pycache__", "logs"]):
            return

        current_time = time.time()
        if current_time - self.last_run < self.cooldown:
            return
            
        # Activate the lock before entering the execution cycle
        self.is_running = True
        try:
            self.execute_target_test(file_path)
        finally:
            # Let the filesystem settle for half a second before unlocking
            time.sleep(0.5)
            self.last_run = time.time()
            self.is_running = False  # Release lock safely

    def execute_target_test(self, modified_file):
        print("\n" + "="*80)
        print(f"🔄 File Change Detected: {os.path.basename(modified_file)}")
        print("🚀 Executing Context-Aware Pytest Suite...")
        print("="*80 + "\n")

        # Smart Routing
        if "tests" in modified_file and "test_" in os.path.basename(modified_file):
            command = ["pytest", modified_file, "-v", "--tb=short"]
        else:
            command = ["pytest", "tests/", "-v", "--tb=short", "-q"]

        try:
            subprocess.run(command, check=False)
        except Exception as e:
            print(f"❌ Execution Engine Failure: {e}")

if __name__ == "__main__":
    path = "."
    event_handler = TestAutoRunnerHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    
    print("\n⚡ Smart Watcher Engine Online (Thread-Locked Edition)!")
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