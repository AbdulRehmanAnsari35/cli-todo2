---
id: "001"
title: "create-spec-advanced"
stage: "spec"
date_iso: "2026-01-09"
surface: "agent"
model: "Qwen"
feature: "recurring-tasks-reminders"
branch: "003-recurring-tasks-reminders"
user: "Mikasa"
command: "/sp.specify My Todo App has successfully completed both: - Basic Level (core CRUD + completion) - Intermediate Level (due dates, priorities, tags, search, filter, sorting) The application is a TERMINAL / CLI-BASED TODO APP. There is NO frontend, NO HTML, NO CSS, and NO browser UI. Now I want to implement ONLY the Advanced Level features. Do NOT modify or rebuild Basic or Intermediate features unless strictly required. ======================== ADVANCED LEVEL FEATURES ======================== 1. Recurring Tasks - Tasks can be marked as recurring - Supported recurrence types: - daily - weekly - monthly - When a recurring task is completed: - It automatically schedules the next occurrence - The next task keeps the same title, priority, and tags - Due date is advanced based on recurrence type - Recurring metadata must be stored with the task 2. Due Dates & Time-Based Reminders (CLI ONLY) - Tasks may optionally include: - due date (YYYY-MM-DD) - due time (HH:MM, 24-hour format) - Implement CLI-based reminders: - When the app starts, it checks for upcoming tasks - Show terminal notifications for: - Tasks due within the next X minutes - Overdue tasks with time - NO browser notifications - NO background daemon - Reminder checks occur: - On app startup - Before each command execution ======================== DATA MODEL UPDATE ======================== Extend the existing task object to include: { id: string, title: string, completed: boolean, dueDate: string | null, dueTime: string | null, priority: \"high\" | \"medium\" | \"low\", tags: string[], createdAt: string, recurring: { enabled: boolean, type: \"daily\" | \"weekly\" | \"monthly\" | null } } ======================== CLI COMMAND REQUIREMENTS ======================== - Add / Update commands must support: --recurring daily|weekly|monthly --due YYYY-MM-DD --time HH:MM - Completing a recurring task must: - Mark the current task as completed - Auto-generate the next occurrence - List command must: - Clearly show recurring tasks - Display due date + time - Show reminder-related warnings ======================== CONSTRAINTS ======================== - CLI / terminal only - No web UI - No background services - No cron jobs - No threads running when app is closed - All data persisted using existing storage mechanism ======================== SCOPE LIMITS ======================== Explicitly DO NOT implement: - Subtasks - Sync / cloud storage - Notifications outside the terminal - UI dashboards - AI suggestions ======================== OUTPUT EXPECTATION ======================== - This specification will be used for sp.plan - Do NOT generate code yet - Do NOT suggest additional features - Follow Spec-Driven Development strictly"
labels: ["specification", "cli", "todo-app", "recurring-tasks", "reminders"]
links: 
  spec: "../specs/003-recurring-tasks-reminders/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/003-recurring-tasks-reminders/spec.md"
  - "specs/003-recurring-tasks-reminders/checklists/requirements.md"
tests_yaml: []
prompt_text: "My Todo App has successfully completed both: - Basic Level (core CRUD + completion) - Intermediate Level (due dates, priorities, tags, search, filter, sorting) The application is a TERMINAL / CLI-BASED TODO APP. There is NO frontend, NO HTML, NO CSS, and NO browser UI. Now I want to implement ONLY the Advanced Level features. Do NOT modify or rebuild Basic or Intermediate features unless strictly required. ======================== ADVANCED LEVEL FEATURES ======================== 1. Recurring Tasks - Tasks can be marked as recurring - Supported recurrence types: - daily - weekly - monthly - When a recurring task is completed: - It automatically schedules the next occurrence - The next task keeps the same title, priority, and tags - Due date is advanced based on recurrence type - Recurring metadata must be stored with the task 2. Due Dates & Time-Based Reminders (CLI ONLY) - Tasks may optionally include: - due date (YYYY-MM-DD) - due time (HH:MM, 24-hour format) - Implement CLI-based reminders: - When the app starts, it checks for upcoming tasks - Show terminal notifications for: - Tasks due within the next X minutes - Overdue tasks with time - NO browser notifications - NO background daemon - Reminder checks occur: - On app startup - Before each command execution ======================== DATA MODEL UPDATE ======================== Extend the existing task object to include: { id: string, title: string, completed: boolean, dueDate: string | null, dueTime: string | null, priority: \"high\" | \"medium\" | \"low\", tags: string[], createdAt: string, recurring: { enabled: boolean, type: \"daily\" | \"weekly\" | \"monthly\" | null } } ======================== CLI COMMAND REQUIREMENTS ======================== - Add / Update commands must support: --recurring daily|weekly|monthly --due YYYY-MM-DD --time HH:MM - Completing a recurring task must: - Mark the current task as completed - Auto-generate the next occurrence - List command must: - Clearly show recurring tasks - Display due date + time - Show reminder-related warnings ======================== CONSTRAINTS ======================== - CLI / terminal only - No web UI - No background services - No cron jobs - No threads running when app is closed - All data persisted using existing storage mechanism ======================== SCOPE LIMITS ======================== Explicitly DO NOT implement: - Subtasks - Sync / cloud storage - Notifications outside the terminal - UI dashboards - AI suggestions ======================== OUTPUT EXPECTATION ======================== - This specification will be used for sp.plan - Do NOT generate code yet - Do NOT suggest additional features - Follow Spec-Driven Development strictly"
response_text: "The feature specification has been successfully created with all required elements. Here's the summary:\n\n**Branch Name**: `003-recurring-tasks-reminders`\n**Spec File Path**: `F:\\new_console_app\\specs\\003-recurring-tasks-reminders\\spec.md`\n**Checklist Path**: `F:\\new_console_app\\specs\\003-recurring-tasks-reminders\\checklists\\requirements.md`\n\nThe specification includes:\n- Comprehensive user scenarios with priorities (P1-P3)\n- Detailed functional requirements (FR-001 through FR-012)\n- Key entities definition\n- Measurable success criteria (SC-001 through SC-005)\n- Edge cases consideration\n- Quality validation checklist\n\nThe specification is ready for the next phase (`/sp.plan`) as all quality checklist items have been validated and meet the required standards."
outcome: "Specification created successfully with all required sections and validation"
evaluation: "The specification meets all requirements and is ready for the planning phase"
---

# Feature Specification: Advanced Level Features (Recurring Tasks & Time-Based Reminders)

**Feature Branch**: `003-recurring-tasks-reminders`
**Created**: 2026-01-09
**Status**: Draft
**Input**: User description: "My Todo App has successfully completed both: - Basic Level (core CRUD + completion) - Intermediate Level (due dates, priorities, tags, search, filter, sorting) The application is a TERMINAL / CLI-BASED TODO APP. There is NO frontend, NO HTML, NO CSS, and NO browser UI. Now I want to implement ONLY the Advanced Level features. Do NOT modify or rebuild Basic or Intermediate features unless strictly required. ======================== ADVANCED LEVEL FEATURES ======================== 1. Recurring Tasks - Tasks can be marked as recurring - Supported recurrence types: - daily - weekly - monthly - When a recurring task is completed: - It automatically schedules the next occurrence - The next task keeps the same title, priority, and tags - Due date is advanced based on recurrence type - Recurring metadata must be stored with the task 2. Due Dates & Time-Based Reminders (CLI ONLY) - Tasks may optionally include: - due date (YYYY-MM-DD) - due time (HH:MM, 24-hour format) - Implement CLI-based reminders: - When the app starts, it checks for upcoming tasks - Show terminal notifications for: - Tasks due within the next X minutes - Overdue tasks with time - NO browser notifications - NO background daemon - Reminder checks occur: - On app startup - Before each command execution ======================== DATA MODEL UPDATE ======================== Extend the existing task object to include: { id: string, title: string, completed: boolean, dueDate: string | null, dueTime: string | null, priority: \"high\" | \"medium\" | \"low\", tags: string[], createdAt: string, recurring: { enabled: boolean, type: \"daily\" | \"weekly\" | \"monthly\" | null } } ======================== CLI COMMAND REQUIREMENTS ======================== - Add / Update commands must support: --recurring daily|weekly|monthly --due YYYY-MM-DD --time HH:MM - Completing a recurring task must: - Mark the current task as completed - Auto-generate the next occurrence - List command must: - Clearly show recurring tasks - Display due date + time - Show reminder-related warnings ======================== CONSTRAINTS ======================== - CLI / terminal only - No web UI - No background services - No cron jobs - No threads running when app is closed - All data persisted using existing storage mechanism ======================== SCOPE LIMITS ======================== Explicitly DO NOT implement: - Subtasks - Sync / cloud storage - Notifications outside the terminal - UI dashboards - AI suggestions ======================== OUTPUT EXPECTATION ======================== - This specification will be used for sp.plan - Do NOT generate code yet - Do NOT suggest additional features - Follow Spec-Driven Development strictly"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Recurring Tasks (Priority: P1)

As a user, I want to create tasks that repeat on a schedule (daily, weekly, or monthly) so that I don't have to manually recreate routine tasks.

**Why this priority**: This is the core functionality of the feature - allowing users to set up recurring tasks that automatically generate new instances when completed.

**Independent Test**: Can be fully tested by creating a recurring task with a specific recurrence type and verifying that the task contains the proper recurring metadata.

**Acceptance Scenarios**:

1. **Given** I am using the CLI todo app, **When** I create a task with --recurring daily flag, **Then** the task is saved with recurring metadata set to daily
2. **Given** I have a recurring task, **When** I view the task details, **Then** I can see the recurrence type clearly displayed

---

### User Story 2 - Complete Recurring Tasks (Priority: P1)

As a user, I want to complete a recurring task and have the next occurrence automatically scheduled so that I maintain continuity of my routine tasks.

**Why this priority**: This is the core behavior that makes recurring tasks valuable - automatic generation of the next occurrence when the current one is completed.

**Independent Test**: Can be fully tested by completing a recurring task and verifying that a new occurrence is created with the appropriate due date advancement.

**Acceptance Scenarios**:

1. **Given** I have a daily recurring task, **When** I complete it, **Then** a new identical task is created with the due date advanced by one day
2. **Given** I have a weekly recurring task, **When** I complete it, **Then** a new identical task is created with the due date advanced by one week

---

### User Story 3 - Set Due Dates and Times (Priority: P2)

As a user, I want to assign specific due dates and times to tasks so that I can manage my schedule more effectively.

**Why this priority**: This enhances the existing due date functionality by adding time precision, which is necessary for the reminder system.

**Independent Test**: Can be fully tested by creating a task with a due date and time and verifying it's stored and displayed correctly.

**Acceptance Scenarios**:

1. **Given** I am creating a task, **When** I specify --due 2026-12-31 --time 14:30, **Then** the task is saved with the specified due date and time
2. **Given** I have a task with a due date and time, **When** I list tasks, **Then** the due date and time are displayed clearly

---

### User Story 4 - Receive Time-Based Reminders (Priority: P2)

As a user, I want to receive terminal notifications about upcoming and overdue tasks when I use the app so that I stay aware of my commitments.

**Why this priority**: This provides the value proposition of the reminder system by notifying users of important upcoming tasks.

**Independent Test**: Can be fully tested by starting the app when there are upcoming tasks due within the threshold and verifying that appropriate notifications appear.

**Acceptance Scenarios**:

1. **Given** I have tasks due within the next X minutes, **When** I start the app, **Then** I see terminal notifications about these upcoming tasks
2. **Given** I have overdue tasks, **When** I start the app, **Then** I see terminal notifications about these overdue tasks

---

### User Story 5 - Manage Recurring Task Properties (Priority: P3)

As a user, I want to update or disable the recurring nature of existing tasks so that I can modify my routine tasks as needed.

**Why this priority**: This provides flexibility for users to modify recurring tasks when their routines change.

**Independent Test**: Can be fully tested by updating a recurring task to disable its recurrence or change its recurrence type.

**Acceptance Scenarios**:

1. **Given** I have a recurring task, **When** I update it with --recurring none, **Then** the task is no longer marked as recurring
2. **Given** I have a daily recurring task, **When** I update it to --recurring weekly, **Then** the task's recurrence type is changed to weekly

---

### Edge Cases

- What happens when a recurring task is completed but the system fails to create the next occurrence?
- How does the system handle tasks with past due dates when the app starts?
- What occurs when multiple recurring tasks are due at the same time?
- How does the system handle leap years and month-end dates for monthly recurring tasks?
- What happens if the user tries to set a due time without a due date?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create tasks with recurring properties (daily, weekly, monthly)
- **FR-002**: System MUST store recurring metadata with each task according to the specified data model
- **FR-003**: System MUST generate a new task when a recurring task is completed, inheriting title, priority, and tags
- **FR-004**: System MUST advance the due date appropriately based on the recurrence type when generating new tasks
- **FR-005**: System MUST allow users to specify due dates in YYYY-MM-DD format and due times in HH:MM 24-hour format
- **FR-006**: System MUST check for upcoming and overdue tasks on app startup and before command execution
- **FR-007**: System MUST display terminal notifications for tasks due within a configurable time threshold
- **FR-008**: System MUST display terminal notifications for overdue tasks with their due times
- **FR-009**: CLI commands ADD and UPDATE MUST support --recurring, --due, and --time flags
- **FR-010**: LIST command MUST clearly show recurring tasks with their recurrence type and due date/time
- **FR-011**: System MUST persist all task data using the existing storage mechanism
- **FR-012**: System MUST NOT run any background services or daemons for reminders

### Key Entities *(include if feature involves data)*

- **Task**: Represents a todo item with extended properties for due dates/times and recurring metadata
  - Properties: id, title, completed, dueDate, dueTime, priority, tags, createdAt, recurring
  - Relationships: None
- **Recurring Metadata**: Contains information about task recurrence
  - Properties: enabled, type (daily, weekly, monthly)
  - Relationships: Belongs to a Task entity

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create recurring tasks with daily, weekly, or monthly frequency in under 30 seconds
- **SC-002**: When completing a recurring task, the next occurrence is generated within 1 second
- **SC-003**: Terminal notifications for upcoming tasks appear consistently when tasks are due within the configured time threshold
- **SC-004**: 95% of users can successfully create and complete a recurring task on their first attempt
- **SC-005**: The system handles all edge cases related to recurring tasks (month boundaries, leap years, etc.) without errors