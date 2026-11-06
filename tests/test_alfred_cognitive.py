import pytest
import allure
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
        
        # Attach Alfred's learned variables straight to the Allure Dashboard
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
    
    # Updated text: Repeating 'python', 'pytest', and 'playwright' to give them true frequency weight
    sample_listing = """
    We are looking for a QA Automation Engineer. You must have strong experience 
    with Python and Pytest. The Python role requires experience building Playwright frameworks. 
    Our core automation stack utilizes Pytest and Playwright heavily alongside 
    automated scripts inside GitHub Actions CI/CD pipelines. We love Python!
    """
    
    with allure.step("Execute Alfred's text parsing and frequency ranking matrix"):
        # Requesting the top 5 highest density tokens
        extracted_keywords = alfred.analyze_text_keywords(sample_listing, top_n=5)
        
    with allure.step("Assert Alfred extracts correct high-density keyword tokens"):
        keyword_dict = dict(extracted_keywords)
        
        # Print directly to stdout console logs so you can check your work inside the terminal panel
        print(f"\n📊 Alfred's Extracted Technical Keywords Map: {keyword_dict}")
        
        assert "python" in keyword_dict, "Alfred failed to extract high-density token: python"
        assert "pytest" in keyword_dict, "Alfred failed to extract high-density token: pytest"
        assert "playwright" in keyword_dict, "Alfred failed to extract high-density token: playwright"
        
        allure.attach(
            str(extracted_keywords),
            name="ALFRED_TEXT_ANALYTICS_OUTPUT",
            attachment_type=allure.attachment_type.TEXT
        )