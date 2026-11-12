
Hybrid UI & API Test Automation Framework

A modular QA automation framework built with Python, Pytest, and Playwright. This project demonstrates end-to-end web UI testing, API validation, database-driven test data generation, and performance load testing integrated into a containerized CI/CD pipeline.

Key Features

• Page Object Model (POM): Separates UI element locators from test logic to keep tests clean, readable, and easy to maintain.
• Cross-Browser Testing: Uses Playwright to run functional tests across Chromium, Firefox, and WebKit.
• Fallback Locator Handling: Includes string-similarity matching logic to help locate elements when minor UI attributes change, reducing flaky failures.
• API Mocking & Network Simulation: Intercepts browser network requests to mock API responses and verify how applications handle slow connections or invalid JSON payloads.
• Parallel Execution: Uses pytest-xdist with file-based locking to safely run tests across multiple workers and speed up execution time.
• Database-Driven Test Data: Generates dynamic test data using Faker and SQLAlchemy ORM backed by SQLite.
• Performance Testing: Includes Locust scripts to simulate concurrent user traffic and measure endpoint response times.
• CI/CD & Containerization: Configured with a multi-stage Dockerfile and GitHub Actions workflows to run headless test suites and generate Allure reports automatically.

Tech Stack

• Language: Python 3.12
• Test Frameworks: Pytest, pytest-xdist, Playwright
• API & Performance: Postman, Locust
• Database & Data: SQLite, SQLAlchemy, Faker
• DevOps & Reporting: Docker, GitHub Actions, Allure Report

Project Structure

The project is organized into core directories and configuration files:
• config/, infra/, and pages/ handle environment settings, framework utilities, and Page Object Model classes.
• tests/, .github/workflows/, and root files like Dockerfile, pytest.ini, and requirements.txt manage test suites, CI/CD pipelines, and dependencies.

Local Setup & Execution

1. Clone and Set Up Environment: Clone the repository, create and activate a Python virtual environment, install dependencies, and set up Playwright browsers. (On Windows, use venv\Scripts\activate).
2. Run the Tests: Execute the parallel test suite with Allure reporting, headlessly run UI tests, or launch Locust load tests.
