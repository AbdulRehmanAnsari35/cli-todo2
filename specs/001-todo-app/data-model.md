# Data Model: Todo Python Console App

## Task Entity

### Fields
- **id**: integer
  - Unique identifier for the task
  - Auto-generated using an incrementing counter
  - Required, non-nullable
- **title**: string
  - Title of the task
  - Required, non-empty
  - Maximum length: 500 characters
- **description**: string (optional)
  - Detailed description of the task
  - Optional, can be None/NULL
  - Maximum length: 2000 characters
- **completed**: boolean
  - Completion status of the task
  - Default value: False
  - Required, non-nullable

### Validation Rules
- **id**: Must be a positive integer
- **title**: Must be provided and not empty, minimum length 1 character
- **description**: Optional, if provided must not exceed 2000 characters
- **completed**: Must be a boolean value

### State Transitions
- A task starts with `completed = False`
- The `complete <id>` command toggles the `completed` status:
  - If `completed = False`, it becomes `True`
  - If `completed = True`, it becomes `False`

## TaskList Entity

### Fields
- **tasks**: dictionary
  - Stores tasks with ID as key and Task object as value
  - Maintains all tasks in memory during application session
- **next_id**: integer
  - Tracks the next available ID for new tasks
  - Starts at 1 and increments with each new task

### Validation Rules
- **tasks**: Must maintain unique IDs as keys
- **next_id**: Must be incremented after each new task creation

### Lifecycle
- The TaskList exists only during the application session
- All data is lost when the application terminates
- The next_id counter resets to 1 when the application restarts