from typing import Dict, List, Optional
from src.models.task import Task


class TaskService:
    """
    Service class to handle all task operations including add, list, update, delete, and complete.
    Uses in-memory storage with a dictionary to store tasks.
    """

    def __init__(self):
        """
        Initialize the TaskService with an empty task dictionary and ID counter.
        """
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> int:
        """
        Add a new task with the given title and optional description.

        Args:
            title: The title of the task
            description: Optional description of the task

        Returns:
            The ID of the newly created task
        """
        task = Task(id=self.next_id, title=title, description=description, completed=False)
        self.tasks[self.next_id] = task
        task_id = self.next_id
        self.next_id += 1
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

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update an existing task with new values.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

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

        # Re-validate the task after updating
        task.validate()

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
        return True