# Testing Strategy for Wigor Schedule Windows Application

## Overview
This document outlines the testing strategy for the Wigor Schedule Windows application. It includes details on unit tests, integration tests, and coverage goals to ensure the application is robust and reliable.

## Testing Framework
The project uses `pytest` as the testing framework due to its simplicity and powerful features, such as fixtures and plugins. This allows for easy writing and organization of tests.

## Unit Testing
Unit tests are written for individual components of the application to verify that each part functions correctly in isolation. The following files contain unit tests:

- **tests/test_wigor_client.py**: Tests for the `WigorClient` class, ensuring that API interactions (authentication and schedule retrieval) work as expected.
- **tests/test_auth.py**: Tests for the authentication functions in `auth.py`, verifying that user credentials are validated correctly.
- **tests/test_utils.py**: Tests for utility functions in `utils.py`, ensuring they perform as expected.

### Coverage Goals
The goal is to achieve a test coverage of over 80%. This will be measured using the `pytest-cov` plugin, which provides detailed coverage reports. The coverage should include:

- All public methods in the `WigorClient`, `auth`, and utility functions.
- Critical paths in the application logic.

## Integration Testing
Integration tests will be conducted to ensure that different components of the application work together as intended. These tests will focus on:

- The interaction between the GUI and the `WigorClient`.
- The flow of data from user input through authentication to schedule retrieval.

Integration tests will be added in a separate test file, such as `tests/test_integration.py`, to keep them organized.

## Continuous Integration
The project includes a CI workflow defined in `.github/workflows/ci.yml`. This workflow will automatically run tests on each commit and pull request, ensuring that new changes do not break existing functionality.

### CI Steps
1. Install dependencies from `requirements.txt`.
2. Run unit tests with coverage measurement.
3. Generate a coverage report and fail the build if coverage is below 80%.

## Conclusion
This testing strategy aims to ensure the reliability and maintainability of the Wigor Schedule Windows application. By focusing on unit and integration tests, along with a robust CI process, we can confidently deliver a high-quality product.