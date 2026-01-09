from datetime import datetime, timedelta
from typing import List
from src.models.task import Task
from dateutil.parser import parse


class ReminderService:
    """
    Service for handling time-based reminders for tasks.
    """
    
    def __init__(self, task_service):
        """
        Initialize the reminder service with a task service.
        """
        self.task_service = task_service

    def check_upcoming_and_overdue_tasks(self, time_threshold_minutes: int = 30) -> tuple:
        """
        Check for upcoming and overdue tasks.
        
        Args:
            time_threshold_minutes: Number of minutes to consider as 'upcoming'
            
        Returns:
            A tuple containing (upcoming_tasks, overdue_tasks)
        """
        all_tasks = self.task_service.get_all_tasks()
        current_datetime = datetime.now()
        
        upcoming_tasks = []
        overdue_tasks = []
        
        for task in all_tasks:
            if task.completed:
                continue  # Skip completed tasks
            
            if task.due_date:
                # Construct full datetime from due_date and due_time
                try:
                    if task.due_time:
                        # Combine date and time
                        due_datetime = parse(f"{task.due_date} {task.due_time}")
                    else:
                        # Use just the date with time as 00:00
                        due_datetime = parse(f"{task.due_date} 00:00")
                    
                    # Check if task is overdue
                    if due_datetime < current_datetime:
                        overdue_tasks.append(task)
                    else:
                        # Check if task is upcoming within the threshold
                        time_diff = due_datetime - current_datetime
                        if time_diff <= timedelta(minutes=time_threshold_minutes):
                            upcoming_tasks.append(task)
                except ValueError:
                    # If parsing fails, skip this task
                    continue
        
        return upcoming_tasks, overdue_tasks

    def format_reminder_message(self, upcoming_tasks: List[Task], overdue_tasks: List[Task]) -> str:
        """
        Format a reminder message for upcoming and overdue tasks.
        
        Args:
            upcoming_tasks: List of upcoming tasks
            overdue_tasks: List of overdue tasks
            
        Returns:
            Formatted reminder message string
        """
        message_parts = []
        
        if upcoming_tasks:
            message_parts.append(f"🔔 {len(upcoming_tasks)} upcoming task(s):")
            for task in upcoming_tasks:
                due_info = f"{task.due_date}"
                if task.due_time:
                    due_info += f" at {task.due_time}"
                message_parts.append(f"  - [{task.id}] {task.title} (due: {due_info})")
        
        if overdue_tasks:
            message_parts.append(f"⚠️ {len(overdue_tasks)} overdue task(s):")
            for task in overdue_tasks:
                due_info = f"{task.due_date}"
                if task.due_time:
                    due_info += f" at {task.due_time}"
                message_parts.append(f"  - [{task.id}] {task.title} (due: {due_info})")
        
        return "\n".join(message_parts)

    def check_and_display_reminders(self, time_threshold_minutes: int = 30) -> str:
        """
        Check for reminders and return a formatted message.
        
        Args:
            time_threshold_minutes: Number of minutes to consider as 'upcoming'
            
        Returns:
            Formatted reminder message string, or empty string if no reminders
        """
        upcoming_tasks, overdue_tasks = self.check_upcoming_and_overdue_tasks(time_threshold_minutes)
        
        if not upcoming_tasks and not overdue_tasks:
            return ""
        
        return self.format_reminder_message(upcoming_tasks, overdue_tasks)