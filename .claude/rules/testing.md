---
paths: ["tests/**/*.py", "**/test_*.py", "**/*_test.py"]
---
# Testing Rules and Conventions

These rules apply to all Python test files in this project.

## 1. Test Structure
- **Framework:** Use `pytest`. Write test functions named `test_*` and group related
  behaviors into classes named `Test*` (no `__init__`).
- **Organization:** Group related behaviors under a `Test*` class per unit under test
  (a specific function or user workflow).
- **Naming:** Use descriptive test names that state the expected behavior
  (e.g. `test_calculates_total_when_items_are_added`).

## 2. Test Data Generation
- **Data Factories:** Use factories/fixtures to generate dynamic test objects.
- **Anti-Pattern:** Do not hardcode static data objects directly into test files.
- **Maintainability:** Factories must allow overriding specific fields while providing
  sensible defaults.

## 3. Database Strategy
- **Real Database:** Do not mock the database layer or query builders.
- **Isolation:** Use a dedicated, isolated test database instance.
- **Lifecycle:** Clear tables or roll back transactions between tests to prevent state
  leakage.
