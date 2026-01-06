# Quickstart Guide: Todo Python Console App

## Prerequisites
- Python 3.13+
- UV package manager

## Setup
1. Clone or create the project directory
2. Ensure UV is installed and available in your environment
3. Create the required directory structure:
   ```
   /src
     ├─ main.py
     ├─ models/
     │   └─ task.py
     ├─ services/
     │   └─ task_service.py
     ├─ cli/
     │   └─ command_handler.py
   ```

## Running the Application
Execute the application using UV:
```bash
uv run main.py
```

## Available Commands
Once the application is running, you can use the following commands:

### Add a Task
```
add "Task Title" [Optional Description]
```
Example:
```
add "Buy groceries" "Milk, eggs, bread"
```

### List All Tasks
```
list
```

### Update a Task
```
update <id> [New Title] [New Description]
```
Example:
```
update 1 "Updated title" "Updated description"
```

### Delete a Task
```
delete <id>
```
Example:
```
delete 1
```

### Mark Task Complete/Incomplete
```
complete <id>
```
Example:
```
complete 1
```

### Help and Exit
```
help  # Show available commands
exit  # Quit the application
```

## Example Workflow
1. Start the application: `uv run main.py`
2. Add a task: `add "Learn Python" "Complete the tutorial"`
3. List tasks: `list`
4. Mark task as complete: `complete 1`
5. Update task: `update 1 "Master Python"`
6. Exit: `exit`