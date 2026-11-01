import time
import json
import os
import logging
import pytest

logger = logging.getLogger("AutomationSuite")

def load_expected_schema():
    file_path = os.path.join(os.path.dirname(__file__), "schema_match.json")
    with open(file_path, "r") as file:
        return json.load(file)

def test_backend_api_endpoint_validation(playwright, apm_tracer):
    """Directly targets back-end application layers to assert API compliance and log APM telemetry."""
    logger.info("Initializing background API Request Context...")
    api_context = playwright.request.new_context(base_url="https://httpbin.org")
    
    logger.info("Sending outbound POST request to validation endpoint...")
    expected_data = load_expected_schema()
    
    # --- Start Timer ---
    start_time = time.time()
    response = api_context.post("/post", data=expected_data)
    duration_ms = (time.time() - start_time) * 1000
    # --------------------

    # Track metrics inside our APM infrastructure module
    apm_tracer.log_transaction(
        transaction_name="POST /post endpoint validation matrix",
        status_code=response.status,
        duration_ms=duration_ms
    )
    
    logger.info(f"API Response intercepted. Status Code: {response.status}")
    assert response.status in [200, 429]

    if response.status == 200:
        response_body = response.json()
        returned_payload = response_body["json"]
        
        logger.info("Verifying payload data schema values and key types...")
        assert returned_payload["account_status"] == "active"
        assert isinstance(returned_payload["user_id"], int)
        assert "auth_token" in returned_payload
        logger.info("API Schema compliance check successfully passed.")
    else:
        logger.warning("Skipping payload schema checks because public endpoints are rate-limiting our parallel run (HTTP 429).")
    
    api_context.dispose()