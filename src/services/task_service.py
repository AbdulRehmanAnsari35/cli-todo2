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
            "due_time": task_data.get("due_time"),  # Can be None
            "priority": task_data.get("priority", ""),  # Default to no priority
            "tags": task_data.get("tags", []),  # Default to empty list
            "created_at": task_data.get("created_at") or datetime.now().isoformat(),  # Use current time if not set
        }

        # Handle recurring metadata
        recurring_data = task_data.get("recurring")
        if recurring_data:
            from src.models.task import RecurringMetadata, RecurrenceType
            recurring_enabled = recurring_data.get("enabled", False)
            recurring_type_str = recurring_data.get("type")
            if recurring_type_str:
                try:
                    recurring_type = RecurrenceType(recurring_type_str)
                except ValueError:
                    recurring_type = None
            else:
                recurring_type = None
            migrated_data["recurring"] = RecurringMetadata(enabled=recurring_enabled, type=recurring_type)
        else:
            migrated_data["recurring"] = None

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
                 priority: str = "", tags: List[str] = None, due_time: Optional[str] = None,
                 recurring_enabled: bool = False, recurring_type: Optional = None) -> int:
        """
        Add a new task with the given title and optional description, due date, due time, priority, tags, and recurring properties.

        Args:
            title: The title of the task
            description: Optional description of the task
            due_date: Optional due date in ISO format (YYYY-MM-DD)
            due_time: Optional due time in HH:MM format
            priority: Optional priority level ("high", "medium", "low", or "")
            tags: Optional list of tags
            recurring_enabled: Whether the task is recurring
            recurring_type: The type of recurrence (daily, weekly, monthly)

        Returns:
            The ID of the newly created task
        """
        if tags is None:
            tags = []

        # Create recurring metadata if needed
        from src.models.task import RecurringMetadata
        recurring_metadata = RecurringMetadata(enabled=recurring_enabled, type=recurring_type)

        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False,
            due_date=due_date,
            due_time=due_time,
            priority=priority,
            tags=tags,
            recurring=recurring_metadata
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
                    due_date: Optional[str] = None, priority: Optional[str] = None, tags: List[str] = None,
                    due_time: Optional[str] = None, recurring_enabled: Optional[bool] = None,
                    recurring_type: Optional = None) -> bool:
        """
        Update an existing task with new values.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)
            due_date: New due date (optional)
            due_time: New due time (optional)
            priority: New priority (optional)
            tags: New tags list (optional)
            recurring_enabled: New recurring enabled status (optional)
            recurring_type: New recurring type (optional)

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
        if due_time is not None:
            task.due_time = due_time
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if recurring_enabled is not None or recurring_type is not None:
            # Update recurring metadata
            if task.recurring is None:
                from src.models.task import RecurringMetadata
                task.recurring = RecurringMetadata()

            # Only update if the parameter was explicitly provided
            if recurring_enabled is not None:
                task.recurring.enabled = recurring_enabled
            if recurring_type is not None:
                task.recurring.type = recurring_type

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
        If the task is recurring and being marked as complete, generate the next occurrence.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if the task status was toggled, False if the task was not found
        """
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        was_completed = task.completed
        task.completed = not task.completed

        # If task was marked as complete and it's a recurring task, generate the next occurrence
        if not was_completed and task.completed and task.recurring and task.recurring.enabled and task.recurring.type:
            from src.utils.recurring_utils import generate_next_occurrence
            try:
                next_task = generate_next_occurrence(task)

                # Assign a new ID to the next occurrence
                next_task.id = self.next_id
                self.next_id += 1

                # Add the new task to the task list
                self.tasks[next_task.id] = next_task
            except Exception as e:
                # Log the error but don't prevent the original task from being marked as complete
                print(f"Warning: Could not generate next occurrence for recurring task {task_id}: {str(e)}")

        self.save_tasks()  # Save after toggling
        return True