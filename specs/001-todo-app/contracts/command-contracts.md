# Interface Contracts: Todo Python Console App

## Command Interface Contracts

### Add Task Command
- **Command**: `add <title> [description]`
- **Input**: 
  - title (string, required): Task title, minimum 1 character
  - description (string, optional): Task description, max 2000 characters
- **Output**: Task ID (integer) of the newly created task
- **Success Response**: "Task added with ID: [id]"
- **Error Responses**:
  - "Error: Title is required for add command"
  - "Error: Task with ID [id] not found" (if relevant)

### List Tasks Command
- **Command**: `list`
- **Input**: None
- **Output**: Formatted table of all tasks with ID, Title, Description, and Status
- **Success Response**: Formatted task list or "No tasks found."
- **Error Responses**: None

### Update Task Command
- **Command**: `update <id> [title] [description]`
- **Input**:
  - id (integer, required): Task identifier
  - title (string, optional): New task title
  - description (string, optional): New task description
- **Output**: Confirmation of update
- **Success Response**: "Task [id] updated successfully"
- **Error Responses**:
  - "Error: Task with ID [id] does not exist"
  - "Error: At least title or description must be provided for update"

### Delete Task Command
- **Command**: `delete <id>`
- **Input**: id (integer, required): Task identifier
- **Output**: Confirmation of deletion
- **Success Response**: "Task [id] deleted successfully"
- **Error Responses**:
  - "Error: Task with ID [id] does not exist"

### Complete Task Command
- **Command**: `complete <id>`
- **Input**: id (integer, required): Task identifier
- **Output**: Updated task status
- **Success Response**: "Task [id] marked as [complete/incomplete]"
- **Error Responses**:
  - "Error: Task with ID [id] does not exist"

### Help Command
- **Command**: `help`
- **Input**: None
- **Output**: List of available commands with usage
- **Success Response**: Formatted help text
- **Error Responses**: None

### Exit Command
- **Command**: `exit`
- **Input**: None
- **Output**: Application termination
- **Success Response**: Application exits cleanly
- **Error Responses**: None

## Data Contracts

### Task Object
- **id**: integer (unique, auto-generated)
- **title**: string (required, non-empty)
- **description**: string (optional, can be null)
- **completed**: boolean (default: false)

## Error Contract
All commands follow the error format:
- Format: "Error: [specific error message]"
- Application continues running after errors
- Errors do not crash the application