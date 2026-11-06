import pytest
import allure
import os
from alfred_engine import AlfredCore

def test_alfred_cognitive_learning_thresholds():
    """
    Automated regression gate auditing Alfred's learning efficiency 
    and deterministic classification accuracy scores.
    """
    alfred = AlfredCore()
    
    with allure.step("Initialize Alfred's core cognitive modules"):
        alfred.initialize_logic_module(module_name="logic_gate_audit", input_size=2)
        assert "logic_gate_audit" in alfred.cognitive_modules
        
    training_set = [
        ([0, 0], 0),
        ([1, 0], 0),
        ([0, 1], 0),
        ([1, 1], 1)
    ]
    
    with allure.step("Execute neural backpropagation training loops"):
        alfred.train_module(module_name="logic_gate_audit", training_data=training_set, epochs=100)
        
    with allure.step("Assert Alfred processes deterministic boundary data with 100% accuracy"):
        assert alfred.process_logic("logic_gate_audit", [0, 0]) == 0, "Alfred failed false-negative evaluation"
        assert alfred.process_logic("logic_gate_audit", [1, 1]) == 1, "Alfred failed true-positive evaluation"
        
        module_metrics = alfred.cognitive_modules["logic_gate_audit"]
        allure.attach(
            f"Alfred's Learned Weights: {module_metrics['weights']}\nAlfred's Bias: {module_metrics['bias']}",
            name="ALFRED_NEURAL_METRICS",
            attachment_type=allure.attachment_type.TEXT
        )

def test_alfred_text_analytics_token_extraction():
    """
    Automated regression check validating Alfred's natural language token parsing,
    case normalization, and keyword ranking density metrics.
    """
    alfred = AlfredCore()
    
    sample_listing = """
    We are looking for a QA Automation Engineer. You must have strong experience 
    with Python and Pytest. The Python role requires experience building Playwright frameworks. 
    Our core automation stack utilizes Pytest and Playwright heavily alongside 
    automated scripts inside GitHub Actions CI/CD pipelines. We love Python!
    """
    
    with allure.step("Execute Alfred's text parsing and frequency ranking matrix"):
        extracted_keywords = alfred.analyze_text_keywords(sample_listing, top_n=5)
        
    with allure.step("Assert Alfred extracts correct high-density keyword tokens"):
        keyword_dict = dict(extracted_keywords)
        
        print(f"\n📊 Alfred's Extracted Technical Keywords Map: {keyword_dict}")
        
        assert "python" in keyword_dict, "Alfred failed to extract high-density token: python"
        assert "pytest" in keyword_dict, "Alfred failed to extract high-density token: pytest"
        assert "playwright" in keyword_dict, "Alfred failed to extract high-density token: playwright"
        
        allure.attach(
            str(extracted_keywords),
            name="ALFRED_TEXT_ANALYTICS_OUTPUT",
            attachment_type=allure.attachment_type.TEXT
        )

def test_alfred_file_system_bloat_orchestration(tmp_path):
    """
    Automated system gate auditing Alfred's capability to recursively parse
    directories and calculate accumulated byte size footprints safely.
    """
    alfred = AlfredCore()
    
    # Create a simulated workspace sandbox using Pytest's temporary directory fixture
    mock_project_root = tmp_path / "mock_project"
    mock_pytest_cache = mock_project_root / ".pytest_cache"
    mock_pytest_cache.mkdir(parents=True)
    
    dummy_cache_file = mock_pytest_cache / "v_cache_data.json"
    dummy_cache_file.write_text("X" * 1024)  # 1 KB footprint size
    
    with allure.step("Execute Alfred's workspace sweep analysis"):
        bytes_found, paths_found = alfred.calculate_and_purge_workspace_bloat(
            target_dir=str(mock_project_root), 
            dry_run=True
        )
        
    with allure.step("Assert Alfred detects byte weight and paths accurately with absolute user safety"):
        assert bytes_found >= 1024, "Alfred failed to aggregate cumulative storage size footprint"
        assert os.path.exists(dummy_cache_file), "Alfred executed a destructive write step!"
        
        allure.attach(
            f"Calculated Footprint: {bytes_found} Bytes\nAnalyzed Paths: {paths_found}",
            name="ALFRED_CLEANUP_METRICS",
            attachment_type=allure.attachment_type.TEXT
        )