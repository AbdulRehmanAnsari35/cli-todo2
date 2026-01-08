# Data Model: Todo App Intermediate Features

## Task Entity

### Properties
- **id**: `string` - Unique identifier for the task (UUID format)
- **title**: `string` - The task description/title
- **completed**: `boolean` - Whether the task is completed or not
- **dueDate**: `string | null` - Optional due date in ISO string format (e.g., "2025-08-15") or null if no due date is set
- **priority**: `"high" | "medium" | "low" | ""` - Priority level of the task, with empty string representing no priority set
- **tags**: `string[]` - Array of tag strings associated with the task (e.g., ["work", "urgent"])
- **createdAt**: `string` - Creation timestamp in ISO string format (e.g., "2025-07-20T10:30:00.000Z")

### Validation Rules
- **id**: Required, must be unique across all tasks
- **title**: Required, minimum 1 character
- **completed**: Required, boolean value
- **dueDate**: Optional, if provided must be a valid ISO date string
- **priority**: Required, must be one of the allowed values
- **tags**: Required, must be an array of strings, no duplicate tags allowed per task
- **createdAt**: Required, must be a valid ISO date string

### State Transitions
- A task can transition from incomplete to complete when the checkbox is toggled
- A task can transition from complete to incomplete when the checkbox is toggled
- Any property except id and createdAt can be modified after creation

## Filter Entity

### Properties
- **status**: `"all" | "active" | "completed"` - Filter by completion status
- **priority**: `"all" | "high" | "medium" | "low"` - Filter by priority level
- **dueDate**: `"all" | "today" | "overdue"` - Filter by due date status
- **tag**: `string | "all"` - Filter by specific tag, "all" means no tag filtering

### Validation Rules
- **status**: Required, must be one of the allowed values
- **priority**: Required, must be one of the allowed values
- **dueDate**: Required, must be one of the allowed values
- **tag**: Required, must be either "all" or a valid tag string

## SortOption Entity

### Properties
- **type**: `"dueDate" | "priority" | "alphabetical" | "creationDate"` - The sorting criterion
- **direction**: `"asc" | "desc"` - The sorting direction (not explicitly stored but used in implementation)

### Validation Rules
- **type**: Required, must be one of the allowed values
- **direction**: Required for implementation, defaults to appropriate direction for each type

## Data Relationships

### Task to Tags
- One task can have multiple tags (one-to-many relationship)
- Tags are stored as an array within each task object
- Tags can be shared across multiple tasks

### Task to Filters
- Each task can match zero or more active filters
- Filters are applied in sequence to determine which tasks to display
- Multiple filters can be active simultaneously