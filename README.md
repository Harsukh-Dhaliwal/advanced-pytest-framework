Hybrid UI & API Test Automation Framework

A Python-based QA automation framework utilizing Pytest and Playwright for end-to-end web testing, API validation, database integration, and load testing.

Highlights

• QA & Resilience: Implements Page Object Model (POM), smart fallback locators to prevent flaky tests, and negative/edge-case testing.
• Core Features: Cross-browser execution (Chromium, Firefox, WebKit), API mocking, parallel testing (pytest-xdist), dynamic test data (Faker/SQLAlchemy), Locust load testing, and CI/CD via GitHub Actions and Docker.

Tech Stack

• Language & Frameworks: Python 3.12, Pytest, Playwright, pytest-xdist
• API, DB & Performance: Postman, Locust, SQLite, SQLAlchemy, Faker
• CI/CD & Reporting: GitHub Actions, Docker, Allure Report

Project Structure & Quick Start

The project organizes source files into modules for CI/CD workflows, configuration, page objects, and test suites, and can be initialized by cloning the repository and installing dependencies via pip and playwright.