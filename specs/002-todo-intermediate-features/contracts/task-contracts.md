# API Contracts: Todo App Intermediate Features

## Task Management Interface

### Task Object Schema
```json
{
  "id": "string",
  "title": "string",
  "completed": "boolean",
  "dueDate": "string | null",
  "priority": "\"high\" | \"medium\" | \"low\" | \"\"",
  "tags": "string[]",
  "createdAt": "string"
}
```

### Task Operations

#### Add Task
- **Method**: Internal function call
- **Input**: Partial task object with at minimum a title
- **Output**: Complete task object with generated id and createdAt
- **Side Effect**: Persists task to localStorage

#### Update Task
- **Method**: Internal function call
- **Input**: Task id and partial task object with fields to update
- **Output**: Updated task object
- **Side Effect**: Updates task in localStorage

#### Delete Task
- **Method**: Internal function call
- **Input**: Task id
- **Output**: Boolean indicating success
- **Side Effect**: Removes task from localStorage

#### Toggle Complete
- **Method**: Internal function call
- **Input**: Task id
- **Output**: Updated task object
- **Side Effect**: Updates completion status in localStorage

#### Get All Tasks
- **Method**: Internal function call
- **Input**: None
- **Output**: Array of all task objects
- **Side Effect**: Reads from localStorage

## Filter Interface

### Filter Object Schema
```json
{
  "status": "\"all\" | \"active\" | \"completed\"",
  "priority": "\"all\" | \"high\" | \"medium\" | \"low\"",
  "dueDate": "\"all\" | \"today\" | \"overdue\"",
  "tag": "string | \"all\""
}
```

### Filter Operations

#### Apply Filters
- **Method**: Internal function call
- **Input**: Array of tasks and filter object
- **Output**: Filtered array of tasks
- **Side Effect**: None

## Sort Interface

### Sort Option Schema
```json
{
  "type": "\"dueDate\" | \"priority\" | \"alphabetical\" | \"creationDate\"",
  "direction": "\"asc\" | \"desc\""
}
```

### Sort Operations

#### Apply Sort
- **Method**: Internal function call
- **Input**: Array of tasks and sort option
- **Output**: Sorted array of tasks
- **Side Effect**: None

## Search Interface

### Search Operation

#### Apply Search
- **Method**: Internal function call
- **Input**: Array of tasks and search term
- **Output**: Array of tasks matching the search term in title or tags
- **Side Effect**: None