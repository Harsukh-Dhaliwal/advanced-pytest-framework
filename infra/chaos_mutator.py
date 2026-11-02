import json

class ChaosNetworkMutator:
    """
    Injects structural anomalies and modified status states into browser-level requests.
    Validates the resilient zero-trust recovery mechanisms of the client front-end.
    """
    
    @staticmethod
    def mutate_payload_schema(original_data: dict, drop_key: str) -> dict:
        """Deep-copies and corrupts a target dictionary by purging crucial data keys."""
        mutated_copy = dict(original_data)
        if drop_key in mutated_copy:
            del mutated_copy[drop_key]
        return mutated_copy