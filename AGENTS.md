```markdown
# AGENTS.md - AI Coding Agent Guidelines

These guidelines outline the principles and rules for development of the AGENTS.md repository, focusing on maintainability, performance, and quality. Adherence to these principles is mandatory for all development activities.

## 1. DRY (Don't Repeat Yourself)

*   All code modules, functions, and classes should have single, well-defined responsibilities.
*   Avoid duplication of logic and data structures across multiple files.
*   Refactor code to eliminate redundancy whenever possible.
*   Document reusable components clearly.

## 2. KISS (Keep It Simple, Stupid)

*   Prioritize simplicity and readability.
*   Strive for the shortest possible code that achieves the desired functionality.
*   Avoid unnecessary complexity.
*   Refactor for clarity and maintainability.

## 3. SOLID Principles

*   **Single Responsibility Principle:** Each class/module should have one, and only one, reason to change.
*   **Open/Closed Principle:** The system should be extensible without modifying the existing code.  New features should be implemented as new classes/modules.
*   **Liskov Substitution Principle:**  Subclasses should be substitutable for their base classes without altering the correctness of the program.
*   **Interface Segregation Principle:**  Clients should not be forced to implement interfaces they do not use.
*   **Dependency Inversion Principle:**  High-level modules should be replaced by low-level modules.

## 4. YAGNI (You Aren't Gonna Need It)

*   Only implement functionality that is absolutely necessary at a given point in time.
*   Don’t add features or code that isn’t currently required.
*   Defer implementation of future requirements until they become necessary.

## 5. Code Structure & Formatting

*   **File Size Limit:** Each file must not exceed 180 lines of code.  Longer files are subject to stricter review.
*   **Naming Conventions:** Follow consistent naming conventions (e.g., camelCase, snake_case) throughout the codebase.
*   **Comments:**  Comments should explain *why* the code is written, not *what* it's doing.  Avoid redundant comments.
*   **Code Style:** Adhere to a consistent code style guide (e.g., PEP 8 for Python). Use a linter (e.g., flake8, pylint) to enforce the style.
*   **Indentation:**  Use 2 spaces for indentation. 4 spaces is acceptable, but consistency is key.
*   **Whitespace:**  Maintain consistent whitespace around operators and after commas.
*   **Blank Lines:**  Use blank lines to separate logical sections of code.

## 6. Testing (Productivity Focused)

*   **Unit Tests:** All code must be thoroughly tested with unit tests.
*   **Test Coverage:** Aim for at least 80% test coverage. Utilize existing test suites or create new ones.
*   **Test-Driven Development:** Write tests *before* writing code.  Refactor code to pass existing tests.
*   **Test Case Design:**  Tests should cover all critical scenarios and edge cases.
*   **Test Data Management:** Utilize realistic and well-defined test data.  Avoid generating test data dynamically.

## 7.  Specific Considerations for AGENTS.md

*   **Core Logic Modules:** All core logic related to agent behavior, data processing, and communication should reside in separate modules.
*   **Data Abstraction:** Use data abstractions to decouple data access from implementation details.
*   **Configuration Management:**  Utilize a clear and maintainable configuration mechanism.
*   **Error Handling:** Implement robust error handling and logging.
*   **API Design:** Design well-defined APIs for agent interactions.
*   **Documentation:** Provide clear and concise documentation for all modules and functions.

## 8.  General Best Practices

*   **Version Control:** Use Git for version control.
*   **Code Review:**  All code changes should be reviewed by at least one other developer.
*   **Documentation Updates:** Update documentation when changes to the code are made.
*   **Continuous Integration/Continuous Deployment (CI/CD):** Implement a CI/CD pipeline to automate testing and build processes.

## 9.  Code Generation & Automation

*   Automated code generation is encouraged for common tasks.
*   Use static analysis tools to identify potential problems early.
*   Document code generation logic clearly.

## 10.  Monitoring & Analysis

*   Log data to track usage and identify potential issues.
*   Regularly review log data to understand system behavior.
*   Establish metrics to measure code quality and performance.
```