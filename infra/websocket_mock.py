import json

class MockEventStreamingPayload:
    """Provides structured data mock payloads that mirror asynchronous reactive streaming frames."""
    
    @staticmethod
    def get_mock_frames() -> dict:
        """Returns standard event structures for validation."""
        return {
            "connection_status": "established",
            "socket_frames": [
                {"frame_id": 1, "action": "DATA_MUTATION", "payload_status": "synced"},
                {"frame_id": 2, "action": "TELEMETRY_FLUSH", "payload_status": "verified"},
                {"frame_id": 3, "action": "SECURITY_HANDSHAKE", "payload_status": "granted"}
            ]
        }