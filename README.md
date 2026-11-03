# Phase 1 — Modern Python Development

A collection of Python exercises and practical projects developed as part of my **AI Engineering Learning Roadmap**.

This repository documents my progression beyond Python fundamentals into modern Python development practices, including dependency management, type annotations, modular programming, data validation, object-oriented programming, automated testing, asynchronous programming, and code refactoring.

The objective of this phase was to learn how to organize Python applications, manage dependencies, validate data, and write maintainable code before moving into backend development with FastAPI and PostgreSQL.

**Status:** Completed — 10 Lessons

---

## Getting Started

### Prerequisites

- Python 3.13 or later
- [uv — Python Package Manager](https://docs.astral.sh/uv/)
- A code editor such as VS Code
- Git (optional)

Some lessons use third-party libraries such as Pydantic and pytest.

### 1. Clone the Repository

```bash
git clone https://github.com/rahul-connect/phase-1-modern-python-development.git
cd phase-1-modern-python-development
```

### 2. Check Python and uv

```bash
python3 --version
uv --version
```

### 3. Install Dependencies

Some lessons may contain their own `pyproject.toml` files.

For a lesson configured as a uv project, navigate into its directory:

```bash
cd lesson-05-pydantic
uv sync
```

This installs the dependencies declared by that lesson's project configuration.

If a lesson contains only standalone Python scripts, you can run those directly without creating a uv project.

### 4. Run a Python Exercise

Navigate into the relevant lesson folder and run its Python script:

```bash
uv run python <script_name>.py
```

Replace `<script_name>.py` with the actual filename.

For lessons that use pytest:

```bash
uv run pytest
```

Run pytest from the directory containing the relevant test files and project configuration.

---

## Curriculum — Lesson by Lesson

| Lesson | Topic | Key Concepts |
|---|---|---|
| 01 | [uv and Project Management](lesson-01-uv/) | Virtual environments, dependency management, project configuration |
| 02 | [Type Hints](lesson-02-type-hints/) | Type annotations, function signatures, collection types |
| 03 | [Modules and Packages](lesson-03-modules/) | Imports, modules, packages, code organization |
| 04 | [pathlib](lesson-04-pathlib/) | Filesystem paths, reading and writing files |
| 05 | [Pydantic](lesson-05-pydantic/) | Data models, field validation, serialization |
| 06 | [Classes and OOP](lesson-06-classes/) | Classes, objects, attributes, methods |
| 07 | [pytest](lesson-07-pytest/) | Automated tests, assertions, fixtures |
| 08 | [Asynchronous Python](lesson-08-async/) | `async`, `await`, coroutines, event loops |
| 09 | [Refactoring](lesson-09-refactor/) | Code organization, maintainability, separation of concerns |
| 10 | [Capstone Project](lesson-10-capstone/) | Applying Phase 1 concepts in a practical project |

---

## Lesson Concepts

### Lesson 01 — uv and Python Project Management

**Folder:** `lesson-01-uv/`

Introduction to modern Python project and dependency management.

**Concepts covered:**

- Managing Python versions
- Creating virtual environments
- Initializing Python projects
- Installing and managing dependencies
- Understanding `pyproject.toml`
- Working with uv commands
- Reproducible development environments

**Key tools:** Python, uv

### Lesson 02 — Type Hints

**Folder:** `lesson-02-type-hints/`

Using Python type annotations to make code easier to understand and maintain.

**Concepts covered:**

- Variable type annotations
- Function parameter types
- Function return types
- Built-in types such as `str`, `int`, `float`, and `bool`
- Collection types such as `list` and `dict`
- Optional values using `None`
- Understanding the role of static type checking

### Lesson 03 — Modules and Packages

**Folder:** `lesson-03-modules/`

Organizing Python programs across multiple files.

**Concepts covered:**

- Python modules
- Import statements
- Reusing functions across files
- Organizing code into packages
- Understanding module namespaces
- Separating application responsibilities
- Avoiding unnecessary code duplication

### Lesson 04 — pathlib and File Operations

**Folder:** `lesson-04-pathlib/`

Working with filesystem paths using Python's `pathlib` module.

**Concepts covered:**

- Creating `Path` objects
- Relative and absolute paths
- Joining paths
- Checking file and directory existence
- Reading and writing text files
- Working with directories
- Writing more portable filesystem code

### Lesson 05 — Pydantic

**Folder:** `lesson-05-pydantic/`

Introduction to structured data validation using Pydantic.

**Concepts covered:**

- Creating models with `BaseModel`
- Defining typed model fields
- Required and optional fields
- Field validation
- Handling invalid data
- Converting models to dictionaries
- JSON serialization
- Understanding validation errors

**Key library:** Pydantic

### Lesson 06 — Classes and Object-Oriented Programming

**Folder:** `lesson-06-classes/`

Understanding how classes can organize data and behavior.

**Concepts covered:**

- Defining classes
- Creating objects
- Constructors using `__init__`
- Instance attributes
- Instance methods
- Using `self`
- Encapsulating related data and functionality
- Understanding when classes are useful

### Lesson 07 — pytest

**Folder:** `lesson-07-pytest/`

Introduction to automated testing with pytest.

**Concepts covered:**

- Writing test functions
- Using assertions
- Running tests with pytest
- Testing expected behavior
- Testing edge cases
- Understanding test failures
- Fixtures and reusable test setup

**Key library:** pytest

### Lesson 08 — Asynchronous Python

**Folder:** `lesson-08-async/`

Introduction to asynchronous programming in Python.

**Concepts covered:**

- Synchronous versus asynchronous execution
- Defining functions with `async def`
- Using `await`
- Understanding coroutines
- Introduction to the event loop
- I/O-bound operations
- Understanding when asynchronous programming is useful

These concepts provide a foundation for asynchronous API development and external service integrations.

### Lesson 09 — Refactoring and Code Organization

**Folder:** `lesson-09-refactor/`

Improving existing Python programs through better code organization.

**Concepts covered:**

- Identifying repetitive code
- Extracting reusable functions
- Improving function responsibilities
- Separating program logic
- Improving naming and readability
- Reducing unnecessary complexity
- Making code easier to modify and maintain

### Lesson 10 — Capstone Project

**Folder:** `lesson-10-capstone/`

A practical capstone lesson focused on combining the concepts introduced throughout Phase 1.

**Concepts practiced:**

- Python project organization
- Type annotations
- Functions and classes
- Modular code
- Data validation
- File handling where applicable
- Error handling
- Maintainability and refactoring

The capstone represents the transition from isolated exercises toward building more structured Python applications.

---

## Key Engineering Skills

### Python Development

- Modern Python syntax and type annotations
- Functions and classes
- Modules and packages
- Working with the filesystem
- Handling structured data

### Development Tools

- uv dependency management
- Virtual environments
- `pyproject.toml` configuration
- Pydantic data validation
- pytest fundamentals

### Software Engineering

- Modular application design
- Separation of concerns
- Reusable code
- Code refactoring
- Error handling
- Automated testing concepts
- Asynchronous programming fundamentals

---

## Project Structure

```text
phase-1-modern-python-development/
│
├── lesson-01-uv/
├── lesson-02-type-hints/
├── lesson-03-modules/
├── lesson-04-pathlib/
├── lesson-05-pydantic/
├── lesson-06-classes/
├── lesson-07-pytest/
├── lesson-08-async/
├── lesson-09-refactor/
├── lesson-10-capstone/
│
├── .gitignore
└── README.md
```

Each lesson directory contains the exercises and project files associated with that topic.

---

## Learning Progression

This repository is **Phase 1 of my AI Engineering Learning Roadmap**.

**Phase 0 — Python Foundations**

Variables, control flow, data structures, functions, file handling, error handling, and command-line applications.

**Phase 1 — Modern Python Development**

Dependency management, type hints, modular programming, Pydantic, classes, testing, asynchronous programming, and refactoring.

**Next — Backend Development**

Building REST APIs using FastAPI, integrating relational databases, managing database sessions, and developing more structured backend applications.

These skills form the foundation for later work involving LLM integration, RAG, tool calling, and AI agents.

---

## Project Status

**Phase 1: Completed**

This repository documents my progress in learning modern Python development practices.

It serves as a record of practical exercises and the transition from Python fundamentals toward backend and AI engineering.