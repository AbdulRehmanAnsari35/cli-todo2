from datetime import datetime, date
from typing import Optional


def get_today_string() -> str:
    """Get today's date in YYYY-MM-DD format."""
    return date.today().strftime("%Y-%m-%d")


def is_today(due_date: Optional[str]) -> bool:
    """Check if a due date is today."""
    if not due_date:
        return False
    return due_date == get_today_string()


def is_overdue(due_date: Optional[str], completed: bool) -> bool:
    """Check if a task is overdue (due date is in the past and task is not completed)."""
    if not due_date or completed:
        return False
    
    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
    today = date.today()
    
    return due_date_obj < today


def format_date_for_display(date_string: Optional[str]) -> str:
    """Format date for display."""
    if not date_string:
        return ""
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return date_string