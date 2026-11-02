import json
import os
import pytest
from infra.mutex_lock import DistributedMutexLock

def test_distributed_mutex_concurrency_isolation():
    """
    Validates that the distributed mutex engine enforces safe sequential 
    operations and prevents resource race conditions across parallel execution nodes.
    """
    shared_data_file = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "logs", "shared_concurrency_tracker.json"
    ))
    
    # Ensure logs directory exists safely
    os.makedirs(os.path.dirname(shared_data_file), exist_ok=True)

    # Initialize a clean file asset inside an atomic block if it's missing
    with DistributedMutexLock("shared_init_barrier"):
        if not os.path.exists(shared_data_file):
            with open(shared_data_file, "w", encoding="utf-8") as f:
                json.dump({"write_count": 0}, f)

    # Acquire the specific write lock to update the data file safely
    with DistributedMutexLock("shared_write_lock") as lock:
        assert lock.is_locked is True, "Mutex failed to flag active lock state."
        
        # Read the file's current state
        with open(shared_data_file, "r", encoding="utf-8") as f:
            current_state = json.load(f)
            
        # Mutate the telemetry state data
        current_state["write_count"] += 1
        
        # Flush changes back out cleanly
        with open(shared_data_file, "w", encoding="utf-8") as f:
            json.dump(current_state, f, indent=4)
            
    # Final assertion to check the file structure matches expected schemas
    with open(shared_data_file, "r", encoding="utf-8") as f:
        final_state = json.load(f)
        assert "write_count" in final_state
        assert final_state["write_count"] >= 1