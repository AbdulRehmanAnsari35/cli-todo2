# Implementation Plan: Advanced Level Features (Recurring Tasks & Time-Based Reminders)

**Branch**: `003-recurring-tasks-reminders` | **Date**: 2026-01-09 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Summary

Extend the existing CLI-based Todo application to support recurring tasks (daily, weekly, monthly) and time-based reminders. The implementation will enhance the existing task model with recurring metadata and due time properties, extend CLI commands to support new flags, and implement reminder logic that triggers on app startup and before command execution.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: In-memory storage (as per constitution), datetime module for date/time calculations
**Storage**: In-memory only (as per constitution, no files or database)
**Testing**: pytest (based on existing test files in repository)
**Target Platform**: Cross-platform CLI application
**Project Type**: Single console application extending existing structure
**Performance Goals**: <1 second for recurring task generation, <1 second for reminder checks
**Constraints**: CLI/terminal only, no background services, no cron jobs, all data in memory
**Scale/Scope**: Individual user application, single-threaded operation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Adheres to project structure (models, services, cli components)
- [x] Follows separation of concerns principle
- [x] Maintains in-memory storage approach
- [x] Preserves existing CLI interface while extending functionality
- [x] Includes proper error handling for new features

## Project Structure

### Documentation (this feature)

```text
specs/003-recurring-tasks-reminders/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   └── task.py          # Enhanced task model with recurring and due time properties
├── services/
│   ├── __init__.py
│   ├── task_service.py  # Extended service with recurring task logic
│   └── reminder_service.py  # New service for reminder checks
├── cli/
│   ├── __init__.py
│   └── cli_handler.py   # Extended CLI handler with new flags and reminder checks
└── main.py              # Entry point with reminder checks on startup
```

**Structure Decision**: Extending the existing single project structure by enhancing the task model, extending the task service with recurring logic, adding a dedicated reminder service, and updating the CLI handler to support new flags and reminder checks.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (None) | (None) | (None) |

## Phase 0: Outline & Research

### Research Tasks

1. **Date manipulation in Python**: Research how to properly handle date/time calculations for recurring tasks (daily, weekly, monthly) considering month boundaries and leap years.
2. **CLI argument parsing**: Research how to extend the existing CLI to support --recurring, --due, and --time flags.
3. **In-memory persistence**: Research how to maintain recurring task state within the existing in-memory storage approach.
4. **Time comparison logic**: Research how to implement time-based comparisons for reminders.

### Best Practices

1. **Python datetime handling**: Follow Python's recommended practices for date/time manipulation using the datetime module.
2. **CLI design patterns**: Follow established patterns for command-line argument design and validation.
3. **State management**: Implement proper state management for recurring tasks within the in-memory constraint.

## Phase 1: Design & Contracts

### Data Model Extension Plan

1. **Enhance Task model**: Add dueTime and recurring properties to the existing Task class
2. **Define RecurringMetadata**: Create a nested structure for recurring task properties
3. **Maintain backward compatibility**: Ensure existing tasks without new properties continue to work

### API Contract Extensions

1. **Extended CLI commands**: Add --recurring, --due, --time flags to ADD and UPDATE commands
2. **Reminder checks**: Integrate reminder notifications into existing command flow
3. **LIST command enhancements**: Display recurring info and due times in task listings

## Implementation Plan for Advanced Features

### 1. Scope Enforcement

- Beginner and Intermediate features remain unchanged
- Only extension points required for Advanced features will be implemented
- Existing CLI commands will be extended with new flags, not replaced

### 2. Data Model Extension Plan

- Extend the existing Task object with:
  - dueTime property (string, nullable) for storing time in HH:MM format
  - recurring property (nested object) containing:
    - enabled (boolean)
    - type (string: daily, weekly, monthly)
- Maintain backward compatibility by making new properties optional
- Update existing task creation and retrieval logic to handle new properties

### 3. CLI Command Extension Plan

- Extend ADD command with:
  - --recurring flag accepting daily|weekly|monthly values
  - --due flag accepting YYYY-MM-DD format
  - --time flag accepting HH:MM format
- Extend UPDATE command with same flags
- Modify COMPLETE command to handle recurring task completion logic
- Enhance LIST command to display recurring info and due date/time

### 4. Recurring Task Logic Plan

- Create a recurring task processor that:
  - Detects when a recurring task is completed
  - Generates a new task with the same title, priority, and tags
  - Advances the due date based on recurrence type (daily, weekly, monthly)
  - Sets the new task as incomplete
- Handle edge cases:
  - Month boundaries (e.g., Jan 31 recurring monthly becomes Feb 28)
  - Leap year handling
  - Missed occurrences

### 5. Reminder System Plan (CLI-only)

- Implement a reminder checker that:
  - Runs on app startup
  - Runs before each command execution
  - Identifies tasks due within a configurable time threshold (e.g., next 30 minutes)
  - Identifies overdue tasks
  - Displays terminal notifications for both cases
- No background processes will be created; checks happen synchronously

### 6. Integration Plan

- Integrate Advanced features with existing functionality:
  - Recurring tasks participate in existing list, filter, search, and sort logic
  - Priority and tag handling remains unchanged for recurring tasks
  - Due date handling extends to include due time
- Maintain all existing functionality without modification

### 7. Testing & Validation Plan

- Create unit tests for:
  - Recurring task creation and completion logic
  - Date/time calculation accuracy
  - Reminder notification logic
- Create integration tests for:
  - CLI command extensions
  - End-to-end recurring task workflows
- Verify no regression in Beginner or Intermediate functionality through existing tests