# CLI Command Contracts: Advanced Level Features

## Overview

This document defines the CLI command contracts for the Advanced Level features (Recurring Tasks & Time-Based Reminders) in the Todo application.

## Command Extensions

### ADD Command
```
add <title> [description] [--recurring daily|weekly|monthly] [--due YYYY-MM-DD] [--time HH:MM]
```

#### Parameters
- `title`: Required string, the task title
- `description`: Optional string, the task description
- `--recurring`: Optional flag, specifies recurrence type (daily, weekly, monthly)
- `--due`: Optional flag, specifies due date in YYYY-MM-DD format
- `--time`: Optional flag, specifies due time in HH:MM format (24-hour)

#### Response
- Success: "Task '<title>' added with ID: <id>"
- Error: Appropriate error message

#### Validation
- If --time is provided, --due must also be provided
- --due must be in valid YYYY-MM-DD format
- --time must be in valid HH:MM format
- --recurring must be one of daily, weekly, or monthly

### UPDATE Command
```
update <id> [title] [description] [--recurring daily|weekly|monthly|none] [--due YYYY-MM-DD] [--time HH:MM]
```

#### Parameters
- `id`: Required integer, the task ID
- `title`: Optional string, new task title
- `description`: Optional string, new task description
- `--recurring`: Optional flag, specifies recurrence type (daily, weekly, monthly, none)
- `--due`: Optional flag, specifies due date in YYYY-MM-DD format
- `--time`: Optional flag, specifies due time in HH:MM format (24-hour)

#### Response
- Success: "Task <id> updated successfully"
- Error: Appropriate error message

#### Validation
- Task with given ID must exist
- If --time is provided, --due must also be provided
- --due must be in valid YYYY-MM-DD format
- --time must be in valid HH:MM format
- --recurring must be one of daily, weekly, monthly, or none

### COMPLETE Command
```
complete <id>
```

#### Parameters
- `id`: Required integer, the task ID

#### Response
- Success: "Task <id> marked as complete"
- For recurring tasks: "Task <id> marked as complete. Next occurrence created with ID: <new_id>"
- Error: Appropriate error message

#### Special Behavior
- If the task is recurring, a new occurrence is automatically created after completion
- The new task inherits title, priority, tags, and recurrence settings
- Due date is advanced based on recurrence type

### LIST Command
```
list
```

#### Response
- Success: Formatted list of all tasks with:
  - ID
  - Title
  - Description (if present)
  - Completion status
  - Priority
  - Tags
  - Due date and time (if set)
  - Recurrence type (if recurring)

#### Special Behavior
- Recurring tasks are marked with their recurrence type (daily/weekly/monthly)
- Tasks with due dates/times are displayed with these values
- Overdue tasks are highlighted
- Tasks due within the next 30 minutes are highlighted

## Reminder System Contracts

### Pre-execution Checks
Before executing any command (except help and exit), the system will:
1. Check for tasks due within the next 30 minutes
2. Check for overdue tasks
3. Display appropriate notifications in the terminal

### Startup Checks
On application startup, the system will:
1. Perform the same checks as pre-execution
2. Display any relevant notifications before showing the command prompt