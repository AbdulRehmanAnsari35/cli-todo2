from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.models.task import Task, RecurrenceType


def advance_due_date(due_date_str: str, recurrence_type: RecurrenceType) -> str:
    """
    Advance the due date based on the recurrence type.

    Args:
        due_date_str: Original due date in YYYY-MM-DD format
        recurrence_type: Type of recurrence (daily, weekly, monthly)

    Returns:
        New due date in YYYY-MM-DD format
    """
    original_date = datetime.strptime(due_date_str, "%Y-%m-%d")

    if recurrence_type == RecurrenceType.DAILY:
        new_date = original_date + timedelta(days=1)
    elif recurrence_type == RecurrenceType.WEEKLY:
        new_date = original_date + timedelta(weeks=1)
    elif recurrence_type == RecurrenceType.MONTHLY:
        # Using relativedelta to handle month boundaries properly
        new_date = original_date + relativedelta(months=1)
        # Handle month boundary cases
        new_date_str = new_date.strftime("%Y-%m-%d")
        return handle_month_boundary(due_date_str, new_date_str)
    else:
        raise ValueError(f"Invalid recurrence type: {recurrence_type}")

    return new_date.strftime("%Y-%m-%d")


def generate_next_occurrence(task: Task) -> Task:
    """
    Generate the next occurrence of a recurring task.

    Args:
        task: The completed recurring task

    Returns:
        A new Task instance representing the next occurrence
    """
    if not task.recurring or not task.recurring.enabled or not task.recurring.type:
        raise ValueError("Task must be a recurring task with enabled status and type")

    # Get the next due date based on recurrence type
    next_due_date = advance_due_date(task.due_date, task.recurring.type)

    # Create a new task with the same properties but reset completion status
    next_task = Task(
        id=task.id + 1,  # This will be updated by the task service with a proper ID
        title=task.title,
        description=task.description,
        completed=False,  # Reset completion status
        due_date=next_due_date,
        due_time=task.due_time,  # Keep the same due time
        priority=task.priority,
        tags=task.tags.copy(),  # Copy the tags
        recurring=task.recurring  # Keep the same recurring metadata
    )

    return next_task


def handle_month_boundary(original_date_str: str, new_date_str: str) -> str:
    """
    Handle month boundary cases where advancing by a month results in a different day.
    For example, Jan 31 + 1 month could become Mar 3 (in Feb), but we want it to be Feb 28/29.

    Args:
        original_date_str: Original date in YYYY-MM-DD format
        new_date_str: New date after advancing by recurrence interval

    Returns:
        Adjusted date string in YYYY-MM-DD format
    """
    original_date = datetime.strptime(original_date_str, "%Y-%m-%d")
    new_date = datetime.strptime(new_date_str, "%Y-%m-%d")

    # If the day of the month is different and the original was at the end of the month,
    # adjust to the last day of the target month
    if original_date.day != new_date.day:
        # Get the last day of the target month
        next_month = new_date.replace(day=28) + timedelta(days=4)
        last_day_of_month = (next_month - timedelta(days=next_month.day)).day
        # Use the minimum of the calculated day and the last day of the month
        adjusted_day = min(original_date.day, last_day_of_month)
        return new_date.replace(day=adjusted_day).strftime("%Y-%m-%d")

    return new_date_str