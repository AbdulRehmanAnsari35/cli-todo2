from typing import List
from src.models.task import Task
from src.utils.date_utils import is_today, is_overdue


def filter_by_status(tasks: List[Task], status: str) -> List[Task]:
    """Filter tasks by status (all/active/completed)."""
    if status == 'all':
        return tasks
    elif status == 'active':
        return [task for task in tasks if not task.completed]
    elif status == 'completed':
        return [task for task in tasks if task.completed]
    return tasks


def filter_by_priority(tasks: List[Task], priority: str) -> List[Task]:
    """Filter tasks by priority."""
    if priority == 'all':
        return tasks
    return [task for task in tasks if task.priority == priority]


def filter_by_due_date(tasks: List[Task], due_date_filter: str) -> List[Task]:
    """Filter tasks by due date status (today/overdue)."""
    if due_date_filter == 'all':
        return tasks
    elif due_date_filter == 'today':
        return [task for task in tasks if is_today(task.due_date)]
    elif due_date_filter == 'overdue':
        return [task for task in tasks if is_overdue(task.due_date, task.completed)]
    return tasks


def filter_by_tag(tasks: List[Task], tag: str) -> List[Task]:
    """Filter tasks by specific tag."""
    if tag == 'all':
        return tasks
    return [task for task in tasks if tag in task.tags]


def apply_filters(tasks: List[Task], status: str = 'all', priority: str = 'all', 
                 due_date_filter: str = 'all', tag: str = 'all') -> List[Task]:
    """Apply all filters in sequence."""
    filtered_tasks = tasks
    
    # Apply status filter first
    filtered_tasks = filter_by_status(filtered_tasks, status)
    
    # Apply priority filter
    filtered_tasks = filter_by_priority(filtered_tasks, priority)
    
    # Apply due date filter
    filtered_tasks = filter_by_due_date(filtered_tasks, due_date_filter)
    
    # Apply tag filter
    filtered_tasks = filter_by_tag(filtered_tasks, tag)
    
    return filtered_tasks