from typing import List
from src.models.task import Task
from datetime import datetime


def sort_by_due_date(tasks: List[Task], direction: str = 'asc') -> List[Task]:
    """Sort tasks by due date (soonest first)."""
    def sort_key(task):
        # Handle null dates - put them last
        if task.due_date is None:
            # Return a far future date to sort nulls last
            return datetime.max if direction == 'asc' else datetime.min
        try:
            return datetime.strptime(task.due_date, "%Y-%m-%d")
        except ValueError:
            # If date format is invalid, treat as far future
            return datetime.max if direction == 'asc' else datetime.min

    return sorted(tasks, key=sort_key, reverse=(direction == 'desc'))


def sort_by_priority(tasks: List[Task]) -> List[Task]:
    """Sort tasks by priority (High -> Medium -> Low)."""
    priority_order = {
        'high': 1,
        'medium': 2,
        'low': 3,
        '': 4  # No priority comes last
    }

    return sorted(tasks, key=lambda task: priority_order.get(task.priority, 5))


def sort_alphabetically(tasks: List[Task], direction: str = 'asc') -> List[Task]:
    """Sort tasks alphabetically by title."""
    return sorted(tasks, key=lambda task: task.title.lower(), reverse=(direction == 'desc'))


def sort_by_creation_date(tasks: List[Task], direction: str = 'desc') -> List[Task]:
    """Sort tasks by creation date (newest first)."""
    def sort_key(task):
        try:
            return datetime.fromisoformat(task.created_at.replace("Z", "+00:00"))
        except ValueError:
            # If date format is invalid, treat as epoch
            return datetime.min

    return sorted(tasks, key=sort_key, reverse=(direction == 'desc'))


def apply_sorting(tasks: List[Task], sort_type: str, direction: str = 'asc') -> List[Task]:
    """Apply sorting based on the sort type."""
    if sort_type == 'due_date':
        return sort_by_due_date(tasks, direction)
    elif sort_type == 'priority':
        return sort_by_priority(tasks)
    elif sort_type == 'alphabetical':
        return sort_alphabetically(tasks, direction)
    elif sort_type == 'creation_date':
        return sort_by_creation_date(tasks, direction)
    else:
        return tasks