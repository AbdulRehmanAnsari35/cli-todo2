# Quickstart Guide: Advanced Level Features (Recurring Tasks & Time-Based Reminders)

## Prerequisites

- Python 3.13+
- UV package manager
- Windows, macOS, or Linux operating system

## Setup

1. Clone or navigate to your todo app directory
2. Ensure you have the latest version with Advanced Level features
3. Install dependencies if needed: `uv sync`

## Creating Recurring Tasks

### Daily Recurring Task
```bash
uv run main.py add "Morning meditation" --recurring daily --due 2026-01-10 --time 07:00
```

### Weekly Recurring Task
```bash
uv run main.py add "Team meeting" --recurring weekly --due 2026-01-12 --time 10:00
```

### Monthly Recurring Task
```bash
uv run main.py add "Pay rent" --recurring monthly --due 2026-01-01 --time 09:00
```

## Managing Tasks with Due Dates and Times

### Adding a one-time task with due date and time
```bash
uv run main.py add "Doctor appointment" --due 2026-01-15 --time 14:30
```

### Updating an existing task
```bash
uv run main.py update 1 --due 2026-01-20 --time 15:00
```

## Completing Recurring Tasks

When you complete a recurring task, the system automatically generates the next occurrence:

```bash
uv run main.py complete 1
```

For a daily recurring task, this will:
- Mark the current task as completed
- Create a new task with the same properties
- Advance the due date by one day

## Viewing Tasks

List all tasks to see recurring indicators and due date/times:

```bash
uv run main.py list
```

The output will show:
- Recurring tasks with their recurrence type (daily/weekly/monthly)
- Due dates and times for all tasks with deadlines
- Visual indicators for overdue and upcoming tasks

## Reminder Notifications

When you start the application or run any command, the system will check for:

1. Tasks due within the next 30 minutes
2. Overdue tasks

These will be displayed as terminal notifications before your command executes.

## Example Workflow

1. **Start the app**:
   ```bash
   uv run main.py
   ```
   You'll see any reminder notifications for upcoming or overdue tasks.

2. **Add a recurring task**:
   ```bash
   uv run main.py add "Water plants" --recurring weekly --due 2026-01-17 --time 08:00
   ```

3. **View your tasks**:
   ```bash
   uv run main.py list
   ```

4. **Complete a recurring task**:
   ```bash
   uv run main.py complete 1
   ```
   The system will mark it complete and create the next occurrence.

5. **Exit the app**:
   ```bash
   exit
   ```