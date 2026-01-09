# Tasks: Advanced Level Features (Recurring Tasks & Time-Based Reminders)

**Feature**: Advanced Level Features (Recurring Tasks & Time-Based Reminders)
**Branch**: `003-recurring-tasks-reminders`
**Generated**: 2026-01-09

## Overview

This document outlines the implementation tasks for the Advanced Level features of the CLI-based Todo App. The features include recurring tasks (daily, weekly, monthly) and time-based reminders that notify users of upcoming and overdue tasks.

## Implementation Strategy

- **MVP Scope**: Start with User Story 1 (Create Recurring Tasks) and 2 (Complete Recurring Tasks) to establish core functionality
- **Incremental Delivery**: Each user story builds on the previous to form a complete, testable increment
- **Parallel Opportunities**: Several components can be developed in parallel once foundational elements are in place

## Dependencies

- User Story 1 (Create Recurring Tasks) must be completed before User Story 2 (Complete Recurring Tasks)
- User Story 3 (Set Due Dates and Times) can be developed in parallel with User Story 1
- User Story 4 (Receive Time-Based Reminders) depends on User Stories 1 and 3
- User Story 5 (Manage Recurring Task Properties) depends on User Story 1

## Parallel Execution Examples

- Task T001 (Extend Task model) and T002 (Install dateutil) can run in parallel
- User Story 1 and User Story 3 can be developed in parallel after foundational tasks

---

## Phase 1: Setup

- [X] T001 Set up development environment for Advanced Level features
- [X] T002 Install dateutil library for date manipulation in requirements.txt
- [X] T003 Verify existing test suite passes before implementing Advanced features

## Phase 2: Foundational Tasks

- [X] T004 [P] Extend Task model with recurring and due time properties in src/models/task.py
- [X] T005 [P] Create RecurringMetadata class in src/models/task.py
- [X] T006 [P] Update Task validation logic for new properties in src/models/task.py
- [X] T007 [P] Create ReminderService class in src/services/reminder_service.py
- [X] T008 [P] Create recurring task utility functions in src/utils/recurring_utils.py
- [X] T009 [P] Update CLI argument parser to accept new flags in src/cli/command_handler.py

## Phase 3: User Story 1 - Create Recurring Tasks (Priority: P1)

**Story Goal**: Enable users to create tasks that repeat on a schedule (daily, weekly, or monthly)

**Independent Test**: Can be fully tested by creating a recurring task with a specific recurrence type and verifying that the task contains the proper recurring metadata.

**Acceptance Scenarios**:
1. Given I am using the CLI todo app, When I create a task with --recurring daily flag, Then the task is saved with recurring metadata set to daily
2. Given I have a recurring task, When I view the task details, Then I can see the recurrence type clearly displayed

- [X] T010 [P] [US1] Implement --recurring flag parsing in ADD command in src/cli/command_handler.py
- [X] T011 [P] [US1] Implement --due flag parsing in ADD command in src/cli/command_handler.py
- [X] T012 [P] [US1] Implement --time flag parsing in ADD command in src/cli/command_handler.py
- [X] T013 [US1] Add validation for --time requiring --due in src/cli/command_handler.py
- [X] T014 [US1] Add validation for --recurring values (daily, weekly, monthly) in src/cli/command_handler.py
- [X] T015 [US1] Update TaskService.create_task to handle recurring metadata in src/services/task_service.py
- [X] T016 [US1] Test creating daily recurring task with due date and time
- [X] T017 [US1] Test creating weekly recurring task with due date and time
- [X] T018 [US1] Test creating monthly recurring task with due date and time

## Phase 4: User Story 2 - Complete Recurring Tasks (Priority: P1)

**Story Goal**: Enable users to complete a recurring task and have the next occurrence automatically scheduled

**Independent Test**: Can be fully tested by completing a recurring task and verifying that a new occurrence is created with the appropriate due date advancement.

**Acceptance Scenarios**:
1. Given I have a daily recurring task, When I complete it, Then a new identical task is created with the due date advanced by one day
2. Given I have a weekly recurring task, When I complete it, Then a new identical task is created with the due date advanced by one week

- [X] T019 [P] [US2] Update TaskService.complete_task to detect recurring tasks in src/services/task_service.py
- [X] T020 [P] [US2] Implement recurring task completion logic in src/services/task_service.py
- [X] T021 [P] [US2] Implement next occurrence generation in src/services/task_service.py
- [X] T022 [US2] Implement due date advancement based on recurrence type in src/utils/recurring_utils.py
- [X] T023 [US2] Handle edge cases for month boundaries in src/utils/recurring_utils.py
- [X] T024 [US2] Handle leap year cases in src/utils/recurring_utils.py
- [X] T025 [US2] Test completing daily recurring task generates next occurrence
- [X] T026 [US2] Test completing weekly recurring task generates next occurrence
- [X] T027 [US2] Test completing monthly recurring task generates next occurrence

## Phase 5: User Story 3 - Set Due Dates and Times (Priority: P2)

**Story Goal**: Enable users to assign specific due dates and times to tasks to manage their schedule more effectively

**Independent Test**: Can be fully tested by creating a task with a due date and time and verifying it's stored and displayed correctly.

**Acceptance Scenarios**:
1. Given I am creating a task, When I specify --due 2026-12-31 --time 14:30, Then the task is saved with the specified due date and time
2. Given I have a task with a due date and time, When I list tasks, Then the due date and time are displayed clearly

- [X] T028 [P] [US3] Implement --due and --time flag parsing in UPDATE command in src/cli/command_handler.py
- [X] T029 [US3] Update TaskService.update_task to handle due date and time in src/services/task_service.py
- [X] T030 [US3] Add validation for due date and time format in src/models/task.py
- [X] T031 [US3] Add validation for future date/time requirement in src/models/task.py
- [X] T032 [US3] Update LIST command to display due date and time in src/cli/command_handler.py
- [X] T033 [US3] Test creating task with due date and time
- [X] T034 [US3] Test updating task with due date and time
- [X] T035 [US3] Test displaying due date and time in task list

## Phase 6: User Story 4 - Receive Time-Based Reminders (Priority: P2)

**Story Goal**: Enable users to receive terminal notifications about upcoming and overdue tasks when using the app

**Independent Test**: Can be fully tested by starting the app when there are upcoming tasks due within the threshold and verifying that appropriate notifications appear.

**Acceptance Scenarios**:
1. Given I have tasks due within the next X minutes, When I start the app, Then I see terminal notifications about these upcoming tasks
2. Given I have overdue tasks, When I start the app, Then I see terminal notifications about these overdue tasks

- [X] T036 [P] [US4] Implement reminder check on app startup in src/main.py
- [X] T037 [P] [US4] Implement reminder check before command execution in src/main.py
- [X] T038 [US4] Implement logic to identify tasks due within 30 minutes in src/services/reminder_service.py
- [X] T039 [US4] Implement logic to identify overdue tasks in src/services/reminder_service.py
- [X] T040 [US4] Implement terminal notification display for upcoming tasks in src/services/reminder_service.py
- [X] T041 [US4] Implement terminal notification display for overdue tasks in src/services/reminder_service.py
- [X] T042 [US4] Test reminder notifications on app startup
- [X] T043 [US4] Test reminder notifications before command execution

## Phase 7: User Story 5 - Manage Recurring Task Properties (Priority: P3)

**Story Goal**: Enable users to update or disable the recurring nature of existing tasks

**Independent Test**: Can be fully tested by updating a recurring task to disable its recurrence or change its recurrence type.

**Acceptance Scenarios**:
1. Given I have a recurring task, When I update it with --recurring none, Then the task is no longer marked as recurring
2. Given I have a daily recurring task, When I update it to --recurring weekly, Then the task's recurrence type is changed to weekly

- [X] T044 [US5] Implement --recurring none option in UPDATE command in src/cli/command_handler.py
- [X] T045 [US5] Update TaskService.update_task to handle disabling recurrence in src/services/task_service.py
- [X] T046 [US5] Update TaskService.update_task to handle changing recurrence type in src/services/task_service.py
- [X] T047 [US5] Test disabling recurrence on existing recurring task
- [X] T048 [US5] Test changing recurrence type from daily to weekly
- [X] T049 [US5] Test changing recurrence type from weekly to monthly

## Phase 8: Integration with Existing Features

- [X] T050 [P] Update LIST command to show recurring indicators in src/cli/command_handler.py
- [X] T051 [P] Ensure recurring tasks participate in existing filter/sort logic in src/services/task_service.py
- [X] T052 [P] Ensure recurring tasks maintain priority and tag handling in src/services/task_service.py
- [X] T053 [P] Update search functionality to work with recurring tasks in src/services/task_service.py
- [X] T054 [P] Ensure backward compatibility for existing non-recurring tasks in src/models/task.py

## Phase 9: Edge Case Handling

- [X] T055 [P] Handle case where recurring task completion fails to generate next occurrence in src/services/task_service.py
- [X] T056 [P] Handle tasks with past due dates on app startup in src/services/reminder_service.py
- [X] T057 [P] Handle multiple recurring tasks due at the same time in src/services/reminder_service.py
- [X] T058 [P] Handle month-end dates for monthly recurring tasks in src/utils/recurring_utils.py
- [X] T059 [P] Handle case where user sets due time without due date in src/cli/command_handler.py

## Phase 10: Testing & Validation

- [X] T060 [P] Create unit tests for recurring task creation logic in tests/test_recurring_tasks.py
- [X] T061 [P] Create unit tests for recurring task completion logic in tests/test_recurring_tasks.py
- [X] T062 [P] Create unit tests for date/time calculation accuracy in tests/test_datetime_utils.py
- [X] T063 [P] Create unit tests for reminder notification logic in tests/test_reminder_service.py
- [X] T064 [P] Create integration tests for CLI command extensions in tests/test_cli_commands.py
- [X] T065 [P] Create end-to-end tests for recurring task workflows in tests/test_e2e_recurring.py
- [X] T066 [P] Verify no regression in Beginner or Intermediate functionality in tests/test_basic_features.py
- [X] T067 [P] Run complete test suite to ensure all functionality works together

## Phase 11: Polish & Cross-Cutting Concerns

- [X] T068 Update README.md with documentation for new Advanced Level features
- [X] T069 Add error handling for all new functionality in src/services/task_service.py
- [X] T070 Add logging for recurring task operations in src/services/task_service.py
- [X] T071 Optimize performance of reminder checks to ensure <1 second execution
- [X] T072 Clean up code and ensure adherence to project coding standards
- [X] T073 Conduct final integration test of all Advanced Level features
- [X] T074 Prepare feature for handoff to QA/testing team