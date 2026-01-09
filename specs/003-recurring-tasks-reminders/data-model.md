# Data Model: Advanced Level Features (Recurring Tasks & Time-Based Reminders)

## Task Entity Extension

### Enhanced Task Object

The existing Task object will be extended with additional properties to support recurring tasks and time-based reminders:

```python
class Task:
    id: str                    # Unique identifier for the task
    title: str                 # Title of the task
    completed: bool            # Completion status
    due_date: Optional[str]    # Due date in YYYY-MM-DD format (existing property)
    due_time: Optional[str]    # Due time in HH:MM format (new property)
    priority: Literal["high", "medium", "low"]  # Priority level (existing property)
    tags: List[str]            # Tags associated with the task (existing property)
    created_at: str            # Creation timestamp (existing property)
    recurring: RecurringMetadata  # Recurring task metadata (new property)
```

### RecurringMetadata Object

A nested object to store recurring task properties:

```python
class RecurringMetadata:
    enabled: bool              # Whether the task is recurring
    type: Optional[Literal["daily", "weekly", "monthly"]]  # Recurrence interval
```

## Validation Rules

### Due Date and Time Validation
- If due_time is specified, due_date must also be specified
- due_date must be in valid YYYY-MM-DD format
- due_time must be in valid HH:MM format (24-hour)
- Both due_date and due_time must represent a future moment

### Recurring Task Validation
- If recurring.enabled is True, recurring.type must be specified
- recurring.type must be one of "daily", "weekly", or "monthly"
- Recurring tasks must have a due_date specified

## State Transitions

### Task Completion with Recurrence
When a recurring task is completed:
1. The current task's completed status is set to True
2. A new task is created with:
   - Same title, priority, and tags
   - Due date advanced based on recurrence type
   - Completed status set to False
   - New unique ID
   - Same recurring metadata

### Recurring Task Modification
- Setting recurring.enabled to False stops future recurrences
- Changing recurring.type modifies the recurrence interval for future occurrences
- Updating due_date/time affects future occurrences but not past ones

## Backward Compatibility

### Existing Tasks
- Tasks created before this feature will have:
  - due_time: None
  - recurring: RecurringMetadata(enabled=False, type=None)
- These tasks will continue to function as before
- They will not be affected by recurring task logic

### Data Migration
- No migration needed for existing tasks
- New properties will be added as optional fields
- Default values will be applied for missing properties