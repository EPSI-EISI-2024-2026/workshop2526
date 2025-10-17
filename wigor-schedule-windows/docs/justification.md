# Justification for Technology Choices and Design Decisions

## Overview
The "Wigor Schedule Windows" project aims to provide a user-friendly application for retrieving and displaying a user's schedule via the Wigor API. The choice of technologies and design decisions were made to ensure a robust, maintainable, and efficient application.

## Technology Choices

### Programming Language: Python
Python was chosen for its simplicity and readability, which facilitates rapid development and ease of maintenance. Its extensive libraries and frameworks support various functionalities, making it ideal for this project.

### GUI Framework: Tkinter
Tkinter was selected as the GUI framework due to its inclusion in the standard Python library, which eliminates the need for additional installations. It provides a straightforward way to create windows, buttons, and other UI elements, making it suitable for a desktop application.

### API Interaction: Requests Library
The Requests library was utilized for making HTTP requests to the Wigor API. It simplifies the process of sending requests and handling responses, allowing for cleaner and more readable code when interacting with the API.

### Unit Testing: pytest
pytest was chosen for unit testing due to its simplicity and powerful features. It allows for easy writing of tests and provides detailed output, which is beneficial for debugging and ensuring code quality.

### Packaging: PyInstaller
PyInstaller was selected for packaging the application into a standalone executable. It supports various platforms, including Windows, and simplifies the distribution process by bundling all dependencies into a single executable file.

## Design Decisions

### Modular Architecture
The application is designed with a modular architecture, separating concerns into different files (e.g., `gui.py`, `wigor_client.py`, `auth.py`). This promotes code reusability and maintainability, making it easier to update or replace individual components without affecting the entire application.

### Configuration Management
A dedicated configuration file (`config.py`) was created to manage API endpoints and other settings. This approach allows for easy adjustments to configuration parameters without modifying the core application logic.

### User Authentication
The authentication process is handled in a separate module (`auth.py`), which validates user credentials and manages sessions. This separation enhances security and allows for easier updates to the authentication logic if needed.

### Data Models
Data models for the application (defined in `models.py`) encapsulate the structure and behavior of the data being handled, such as schedules and users. This design choice promotes data integrity and simplifies data manipulation.

### Testing Strategy
A comprehensive testing strategy was implemented, with unit tests covering critical components of the application. The goal is to achieve over 80% code coverage, ensuring that the application is robust and reliable.

## Conclusion
The technology choices and design decisions made in the "Wigor Schedule Windows" project are aimed at creating a reliable, maintainable, and user-friendly application. By leveraging Python's capabilities and adhering to best practices in software design, the project is positioned for future enhancements and scalability.