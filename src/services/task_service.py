import json
import os
from typing import Dict, List, Optional
from src.models.task import Task
from datetime import datetime


class TaskService:
    """
    Service class to handle all task operations including add, list, update, delete, and complete.
    Uses JSON file storage with migration support for existing tasks.
    """

    def __init__(self, storage_file: str = "tasks.json"):
        """
        Initialize the TaskService with JSON file storage and load existing tasks.
        """
        self.storage_file = storage_file
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1
        self.load_tasks()

    def migrate_task(self, task_data: dict) -> Task:
        """
        Migrate an existing task to include new fields if they don't exist.
        Ensures existing tasks without new fields don't break the app.
        """
        # Set default values for new fields if they don't exist
        migrated_data = {
            "id": task_data.get("id", 0),
            "title": task_data.get("title", ""),
            "description": task_data.get("description"),
            "completed": task_data.get("completed", False),
            "due_date": task_data.get("due_date"),  # Can be None
            "priority": task_data.get("priority", ""),  # Default to no priority
            "tags": task_data.get("tags", []),  # Default to empty list
            "created_at": task_data.get("created_at") or datetime.now().isoformat()  # Use current time if not set
        }

        # Create and return a new Task instance with migrated data
        return Task(**migrated_data)

    def load_tasks(self):
        """
        Load tasks from the JSON storage file.
        """
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)

                # Load and migrate tasks
                for task_data in data.get("tasks", []):
                    task = self.migrate_task(task_data)
                    self.tasks[task.id] = task

                # Set next_id to be one more than the highest ID
                if self.tasks:
                    self.next_id = max(self.tasks.keys()) + 1
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Error loading tasks from storage: {e}")
                # Initialize with empty tasks if loading fails
                self.tasks = {}
                self.next_id = 1

    def save_tasks(self):
        """
        Save tasks to the JSON storage file.
        """
        try:
            # Convert tasks to a serializable format
            tasks_data = [task.__dict__ for task in self.tasks.values()]

            # Save to file
            with open(self.storage_file, 'w') as f:
                json.dump({"tasks": tasks_data}, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks to storage: {e}")

    def add_task(self, title: str, description: Optional[str] = None, due_date: Optional[str] = None,
                 priority: str = "", tags: List[str] = None) -> int:
        """
        Add a new task with the given title and optional description, due date, priority, and tags.

        Args:
            title: The title of the task
            description: Optional description of the task
            due_date: Optional due date in ISO format (YYYY-MM-DD)
            priority: Optional priority level ("high", "medium", "low", or "")
            tags: Optional list of tags

        Returns:
            The ID of the newly created task
        """
        if tags is None:
            tags = []
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False,
            due_date=due_date,
            priority=priority,
            tags=tags
        )
        self.tasks[self.next_id] = task
        task_id = self.next_id
        self.next_id += 1
        self.save_tasks()  # Save after adding
        return task_id

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the system.

        Returns:
            A list of all tasks
        """
        return list(self.tasks.values())

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
                    due_date: Optional[str] = None, priority: Optional[str] = None, tags: List[str] = None) -> bool:
        """
        Update an existing task with new values.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)
            due_date: New due date (optional)
            priority: New priority (optional)
            tags: New tags list (optional)

        Returns:
            True if the task was updated, False if the task was not found
        """
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]

        # Update only the fields that were provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if due_date is not None:
            task.due_date = due_date
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags

        # Re-validate the task after updating
        task.validate()

        self.save_tasks()  # Save after updating
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if the task was not found
        """
        if task_id not in self.tasks:
            return False

        del self.tasks[task_id]
        self.save_tasks()  # Save after deleting
        return True

    def toggle_task_completion(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if the task status was toggled, False if the task was not found
        """
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        task.completed = not task.completed
        self.save_tasks()  # Save after toggling
        return True