import os
import time

class DistributedMutexLock:
    """
    Manages thread-safe and process-safe cross-worker synchronization.
    Prevents parallel xdist file locking collisions and data corruption.
    """
    
    def __init__(self, lock_name: str, timeout_seconds: float = 10.0):
        self.lock_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", f".{lock_name}.lock"
        ))
        self.timeout = timeout_seconds
        self.is_locked = False

    def acquire(self) -> bool:
        """Attempts to atomically acquire the file system lock barrier."""
        start_time = time.time()
        while (time.time() - start_time) < self.timeout:
            try:
                # Atomically attempt exclusive file creation
                fd = os.open(self.lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                self.is_locked = True
                return True
            except FileExistsError:
                # Backoff slightly to clear thread pooling lanes
                time.sleep(0.05)
        return False

    def release(self):
        """Forcefully clears the lock file from the workspace explorer root."""
        if self.is_locked and os.path.exists(self.lock_file):
            try:
                os.remove(self.lock_file)
            except OSError:
                pass
            self.is_locked = False

    def __enter__(self):
        if not self.acquire():
            raise TimeoutError(f"Could not acquire distributed mutex lock within {self.timeout}s")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()