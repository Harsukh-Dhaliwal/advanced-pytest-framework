import time
import json
import os
import logging

logger = logging.getLogger("AutomationSuite")

class APMPerformanceTracer:
    """Enterprise interceptor tracking network latency signatures and component metrics."""
    def __init__(self):
        self.trace_log_path = os.path.join("logs", "apm_distributed_traces.json")
        os.makedirs(os.path.dirname(self.trace_log_path), exist_ok=True)
        self.traces = []

    def log_transaction(self, transaction_name: str, status_code: int, duration_ms: float):
        """Records a specific network request execution block transaction footprint."""
        trace_entry = {
            "timestamp": time.time(),
            "transaction_name": transaction_name,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 2),
            "performance_rating": "OPTIMAL" if duration_ms < 500 else "DEGRADED"
        }
        self.traces.append(trace_entry)
        logger.info(f"[APM Trace] {transaction_name} executed in {duration_ms}ms | Status: {status_code}")

    def flush_trace_metrics(self):
        """Persists captured network metrics into a structured telemetry JSON file on execution teardown."""
        if not self.traces:
            return
            
        existing_data = []
        if os.path.exists(self.trace_log_path):
            try:
                with open(self.trace_log_path, "r") as file:
                    existing_data = json.load(file)
            except Exception:
                existing_data = []

        existing_data.extend(self.traces)
        
        with open(self.trace_log_path, "w") as file:
            json.dump(existing_data, file, indent=4)
        
        self.traces.clear()