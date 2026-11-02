import json
import pytest
from playwright.sync_api import Page
from infra.websocket_mock import MockEventStreamingPayload

def test_realtime_network_frame_interception(page: Page, streaming_network_service: str):
    """
    Validates the framework's ability to intercept, decode, and verify 
    asynchronous streaming frame metrics directly from the browser's network context layer.
    """
    intercepted_frames = []

    # Pull our structured schema payload
    mock_payload = MockEventStreamingPayload.get_mock_frames()

    def handle_network_route(route):
        """Intercepts the request, populates tracker arrays, and fulfills with mock payload."""
        intercepted_frames.append(mock_payload)
        
        # Serialize the payload on an independent line to maintain clean syntax compatibility
        payload_json = json.dumps(mock_payload)
        
        route.fulfill(
            status=200,
            content_type="application/json",
            body=payload_json
        )

    # Bind the routing interceptor directly to the browser network layer
    page.route(streaming_network_service, handle_network_route)

    # Dispatch request to the virtual streaming endpoint
    page.goto(streaming_network_service, wait_until="commit")

    # Assert that network layer hooks correctly captured and processed the frame
    assert len(intercepted_frames) > 0, "Network framework failed to hook or intercept real-time buffers."
    
    extracted_data = intercepted_frames[0]
    assert extracted_data["connection_status"] == "established"
    
    frames_list = extracted_data["socket_frames"]
    assert len(frames_list) == 3, f"Expected 3 network event layers, but extracted {len(frames_list)}"
    
    # Assert specific architectural constraints match downstream targets perfectly
    assert frames_list[0]["action"] == "DATA_MUTATION"
    assert frames_list[1]["action"] == "TELEMETRY_FLUSH"
    assert frames_list[2]["payload_status"] == "granted"