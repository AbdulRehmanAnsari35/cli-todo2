# Project Constitution: Todo Python Console App

## Project Identity

**Project Name:** Todo Python Console App  
**Phase:** 1 – In-Memory Interactive Console Application  
**Mission:** To provide a clean, spec-driven, interactive command-line interface for managing todo tasks with in-memory storage.

## Core Objective

Build a clean, maintainable, and spec-driven command-line Todo application that stores tasks in memory, supports CRUD-style operations, follows clean code principles, uses a clear Python project structure, and is fully operable via interactive console commands.

## Technology Stack

- **Language:** Python 3.13+
- **Runner/Environment:** UV
- **Storage:** In-memory only (no files, no database)
- **Interface:** Interactive CLI (REPL style)

## Project Structure (Mandatory)

The project MUST adhere to the following directory structure:

```
/src
  ├─ main.py        # Entry point
  ├─ models/        # Task model(s)
  ├─ services/      # Business logic
  ├─ cli/           # Command parsing & handling
/specs
/history
/constitution
README.md
```

## Feature Requirements (Mandatory)

### 1. Add Task
- **Command:** `add <title> [description]`
- **Functionality:** Adds a new todo item to memory
- **Output:** Returns a unique numeric task ID
- **Validation:** Title must be provided

### 2. List Tasks
- **Command:** `list`
- **Functionality:** Displays all tasks with:
  - ID
  - Title
  - Description (if present)
  - Completion status
- **Output:** Formatted table or list view

### 3. Update Task
- **Command:** `update <id> [title] [description]`
- **Functionality:** Updates an existing task's data
- **Validation:** Task must exist, ID must be valid
- **Behavior:** Updates only provided fields (title or description)

### 4. Delete Task
- **Command:** `delete <id>`
- **Functionality:** Removes a task from memory
- **Validation:** Task must exist, ID must be valid
- **Output:** Confirmation message

### 5. Mark Task Complete/Incomplete
- **Command:** `complete <id>`
- **Functionality:** Toggles completion status of a task
- **Validation:** Task must exist, ID must be valid
- **Output:** Updated task status

## Development Principles

### Spec-Driven Development
- All features MUST be defined in specifications before implementation
- Code changes MUST reference specific spec items
- All functionality MUST be traceable to a spec requirement

### Code Quality
- **Separation of Concerns:** Clear boundaries between models, services, and CLI components
- **No Global Mutable State Abuse:** Use proper object-oriented design or dependency injection
- **Simple, Readable Python Code:** Follow PEP 8 standards and Python best practices
- **Explicit Error Handling:** All potential error conditions MUST be handled gracefully
- **Human-Friendly CLI Output:** Clear, concise, and informative messages
- **Graceful Command Failure:** Commands MUST fail gracefully with helpful error messages

### Architecture
- Models: Define data structures and validation
- Services: Contain business logic and data operations
- CLI: Handle user input, command parsing, and output formatting
- Main: Coordinate components and manage application lifecycle

## Runtime Requirements

### Startup Behavior
- Application MUST run with: `uv run main.py`
- On startup, MUST display: "Welcome to the Todo Python Console App! Type 'help' for available commands or 'exit' to quit."
- Application MUST enter interactive mode after startup message

### Command Interface
- All commands MUST be case-insensitive
- Commands MUST provide helpful error messages for invalid inputs
- Commands MUST validate all parameters before execution
- Command execution MUST NOT crash the application

## Quality Assurance

### Error Handling
- All user input MUST be validated
- Invalid commands MUST return helpful error messages
- Invalid parameters MUST return specific error messages
- Application MUST continue running after command errors

### Testing
- All core features MUST have associated test cases
- Edge cases MUST be considered and tested
- Error conditions MUST be verified through tests

## Deliverables

The project MUST include:

1. **Working Interactive Console App:** All five core features fully implemented
2. **Constitution File:** This document, stored at `.specify/memory/constitution.md`
3. **Specifications Folder:** Complete spec files in `/specs`
4. **Clean GitHub-Ready Structure:** Properly organized repository structure
5. **README:** Explaining usage, commands, and setup instructions

## Compliance Verification

All code submissions MUST:
- Reference this constitution
- Align with the defined project structure
- Implement only features defined in specifications
- Follow the development principles
- Pass all defined acceptance criteria

## Change Management

This constitution MAY only be modified through:
- Explicit specification changes
- Architectural decision records (ADRs)
- Team consensus and approval

Any changes to this constitution MUST be versioned and tracked.