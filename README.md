# FastInventory: Inventory & Asset Tracking Service

[![CI Pipeline](https://github.com/abhishekabramaina/Inventory/actions/workflows/ci.yml/badge.svg)](https://github.com/abhishekabramaina/Inventory/actions)
[![Claude PR Review](https://github.com/abhishekabramaina/Inventory/actions/workflows/claude-review.yml/badge.svg)](https://github.com/abhishekabramaina/Inventory/actions)

High-performance, production-grade FastAPI microservice designed for asset ingest, product tracking, and stock level inventory management. Built on the CCAF architectural framework, this service enforces strict design standards, complete type safety, and robust isolated integration testing.

---

## 1. Architectural Highlights & Design Patterns

The service implements modern software engineering best practices to guarantee safety, portability, and rapid delivery:

*   **FastAPI & Asynchronous Core**: Built on the ASGI standard for maximum request throughput, utilizing modern lifespan context handlers and Pydantic validation.
*   **Database Strategy (Embedded to Distributed)**: Utilizes SQLite for local runs and test isolation. Database queries are fully parameterized, and schema creation is handled via transaction blocks.
*   **Strict Type-Safety**: 100% of the codebase features strict type annotations. Static validation is executed via `mypy --strict` to eliminate typing bugs.
*   **Built-in Ingest Sanitization**: Implements input sanitization utilities at the router interface to guard against XSS, HTML injection, and other script injections.
*   **Isolated Integration Testing**: Adheres to the real-database strategy. Mock database connectors are forbidden; all test fixtures spin up and teardown an isolated physical DB environment for execution.

---

## 2. Directory Structure

```
P_04_Sample_Project/
├── .claude/
│   ├── rules/
│   │   └── testing.md              # Scoped rules for test suite creation
│   └── skills/
│       ├── check-types/            # Modular skill for strict static typechecking
│       ├── lint-pr/                # Modular skill for checking pull requests
│       └── verify-coverage/        # Modular skill for test suite validation
├── .github/workflows/
│   ├── ci.yml                      # Automatic CI pipeline for linting/tests
│   └── claude-review.yml           # Automated AI-driven PR inline reviewer
├── src/
│   ├── __init__.py
│   ├── database.py                 # SQLite engine, schemas, and queries
│   └── main.py                     # API router, Pydantic schemas, and server startup
├── utils/
│   ├── __init__.py
│   └── helpers.py                  # Input sanitization and error formatters
├── tests/
│   ├── __init__.py
│   └── test_app.py                 # Pytest test cases using dynamic data builders
├── requirements.txt                # Python package list
└── config.json                     # Environment configuration defaults
```

---

## 3. Agentic Development & AI Collaboration

This repository is designed to optimize development collaboration with agentic coding assistants (such as Claude). Rather than relying on unstructured instructions, we use declarative rules files to guide the agent:

*   **`CLAUDE.md`**: Positioned at the repository root, this is the primary handbook for AI assistants. It maps the project structure, defines the correct setup and build commands, and links to specific sub-rules.
*   **Scoped Rules (`.claude/rules/`)**: Scopes guidelines to domain contexts. For example, `testing.md` instructs agents to use `pytest` classes, build data factories (`item_factory`), and drop SQLite database files between test runs to avoid state leakage.
*   **Modular Skills (`.claude/skills/`)**: Running runbooks (like `check-types` and `verify-coverage`) that define how an agent executes validation commands locally or inside CI/CD environments.

These agentic rules guarantee that AI contributions are reliable, style-compliant, and secure without manual review overhead.

---

## 4. Getting Started

### Local Installation
Prerequisites: Python 3.10+
1.  **Clone the Repository and Create a Virtual Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```
2.  **Install Package Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration Variables
The service supports runtime overrides using environment variables:
| Variable | Description | Default |
| :--- | :--- | :--- |
| `DATABASE_PATH` | File path for the SQLite database instance | `prod.db` |
| `PORT` | Local server port binding | `8080` |

### Running the API Server
Start the development server using the main package entrypoint:
```bash
python src/main.py
```
Interactive API documentation (Swagger UI) is available locally at: `http://localhost:8080/docs`.

---

## 5. API Reference

| Method | Endpoint | Description | Payload / Request Parameters |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Health check and system status | None |
| **POST** | `/items/` | Registers a new asset with input sanitization | `{"name": "string", "description": "string \| null"}` |
| **GET** | `/items/` | Fetches all registered inventory items | None |
| **GET** | `/items/count/` | Returns total item count in stock | None |
| **GET** | `/items/search/` | Filters database items by matching name | Query string: `?name=item_name` |
| **GET** | `/divide/` | Computes metrics division check | Query strings: `?numerator=x&denominator=y` |

---

## 6. Code Quality & Contribution Standards

To keep the codebase at high quality, all contributions must satisfy the following checks before merging:

### Static Type Analysis
Run typechecks with zero errors to pass static verification:
```bash
mypy . --strict
```

### Running the Test Suite
All unit and integration tests must exit with code `0`:
```bash
python -m pytest -v
```

### Contribution Rules
1.  **Strict Type Annotations**: All function signatures must contain explicit annotations for arguments and return types.
2.  **Real Database Testing**: Do not mock the database connectors. Let tests write to an isolated SQLite instance (`test.db`), which must be cleared and deleted during test teardown.
3.  **Data Builders**: Use dynamic generators (like `item_factory` in `test_app.py`) for test data payloads instead of static hardcoded files.
