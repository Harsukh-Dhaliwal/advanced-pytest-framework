import json
import pytest
from playwright.sync_api import Page
from infra.chaos_mutator import ChaosNetworkMutator

def test_network_chaos_injection_and_schema_corruption(page: Page):
    """
    Validates that the front-end safely captures corrupt response schemas 
    and handles security payload failures without throwing breaking runtime exceptions.
    """
    target_api_endpoint = "https://internal-app.local"
    
    # Define our pristine upstream data template
    healthy_backend_payload = {
        "status": "success",
        "user_id": "USR-90210",
        "token_authority": "OAUTH_SECURE_NODE"
    }

    def inject_chaos_route_handler(route):
        """Intercepts the backend pipe and strips away critical security keys."""
        corrupted_payload = ChaosNetworkMutator.mutate_payload_schema(
            original_data=healthy_backend_payload,
            drop_key="token_authority"
        )
        
        # Fulfill the API request with modified schema fields
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(corrupted_payload)
        )

    # Bind the routing mutation layer to the network pipeline
    page.route(target_api_endpoint, inject_chaos_route_handler)
    
    # Trigger an asynchronous client-side API look-up by injecting an execution handle
    page.goto("about:blank")
    evaluated_response = page.evaluate(f"""
        async () => {{
            const response = await fetch('{target_api_endpoint}');
            return await response.json();
        }}
    """)

    # Assert that our chaos injection layer modified the data block successfully
    assert evaluated_response is not None, "Failed to intercept or fetch API endpoint."
    assert evaluated_response["user_id"] == "USR-90210"
    
    # Confirm the key was completely purged by the chaos mutator
    assert "token_authority" not in evaluated_response, "Chaos injection failed to drop the secure token key."