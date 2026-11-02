import json
import os
import pytest
from infra.graph_visualizer import ArchitectureGraphVisualizer

def test_architecture_dependency_graph_compilation():
    """
    Validates that the visualizer engine maps core infrastructure layers 
    and outputs a structured system tracking configuration profile.
    """
    test_identifier = "test_chaos_injection_suite"
    referenced_infra_modules = ["chaos_mutator.py", "security.py", "apm_tracer.py"]

    # Register the architecture dependencies into our tracking system
    ArchitectureGraphVisualizer.register_dependency(
        test_suite=test_identifier,
        core_modules=referenced_infra_modules
    )

    # Resolve target output path parameters
    target_report = ArchitectureGraphVisualizer.REPORT_PATH
    assert os.path.exists(target_report) is True, "Visualizer failed to compile graph report file."

    # Parse output values to confirm structural accuracy
    with open(target_report, "r", encoding="utf-8") as f:
        compiled_data = json.load(f)

    assert test_identifier in compiled_data, "Test suite identifier tracking miss."
    
    suite_meta = compiled_data[test_identifier]
    assert suite_meta["layer_classification"] == "E2E_Network_Interception_Grid"
    assert "security.py" in suite_meta["dependencies_mapped"]