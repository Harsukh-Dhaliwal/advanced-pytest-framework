import json
import os
import pytest
from playwright.sync_api import Page, expect 

# 1. Helper function to load and parse the JSON dataset
def load_test_data():
    file_path = os.path.join(os.path.dirname(__file__), "test_data.json")
    with open(file_path, "r") as file:
        return json.load(file)

# 2. Injecting the JSON objects straight into the Pytest parametrizing loop
@pytest.mark.parametrize("data", load_test_data())
def test_user_login_scenarios(page: Page, data: dict):
    """
    Drives multiple login authentication verifications dynamically 
    using a completely decoupled external JSON configuration matrix.
    """
    print(f"\nExecuting Data-Driven Scenario: {data['scenario']}")
    
    # Navigate to a standard mock login testing interface
    page.goto("https://saucedemo.com")
    
    # Fill out the authentication parameters using the data matrix fields
    page.fill("input[data-test='username']", data["username"])
    page.fill("input[data-test='password']", "secret_sauce")
    
    # Execute submission action
    page.click("input[data-test='login-button']")
    
    # Assert that the application state matches our expected URL outcome parameter
    assert data["expected_url_keyword"] in page.url

def load_login_scenarios():
    """Reads test configurations by automatically scanning framework directories."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    
    # Candidate 1: Look inside the tests/ directory itself
    tests_path = os.path.join(current_dir, "test_data.json")
    # Candidate 2: Look in the absolute root folder directory
    root_path = os.path.join(root_dir, "test_data.json")
    
    # Determine which path actually contains your file
    if os.path.exists(tests_path):
        file_path = tests_path
    elif os.path.exists(root_path):
        file_path = root_path
    else:
        # Fail gracefully with a helpful message pinpointing where it checked
        raise FileNotFoundError(
            f"Could not locate 'test_data.json' file automatically. Checked:\n1. {tests_path}\n2. {root_path}"
        )
    
    with open(file_path, "r") as file:
        data = json.load(file)
        if isinstance(data, dict):
            return data.get("login_scenarios", [])
        return data

# Your parameterize decorator remains mapped to this function
@pytest.mark.parametrize("scenario_data", load_login_scenarios())
def test_user_login_scenarios(page: Page, scenario_data):
    # Rest of your functional assertions remain completely unchanged...
    pass
