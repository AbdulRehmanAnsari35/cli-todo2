from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RecurrenceType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class RecurringMetadata:
    """
    Represents recurring task metadata with enabled status and recurrence type.
    """
    enabled: bool = False
    type: Optional[RecurrenceType] = None


@dataclass
class Task:
    """
    Represents a todo task with id, title, description, completion status, due date, due time, priority, tags, creation timestamp, and recurring metadata.
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[str] = None  # ISO string like "2025-08-15" or None
    due_time: Optional[str] = None  # Time string like "14:30" or None
    priority: str = ""  # "high", "medium", "low", or "" for no priority
    tags: List[str] = None  # List of tag strings, e.g. ["work", "urgent"]
    created_at: str = None  # ISO timestamp string
    recurring: RecurringMetadata = None  # Recurring task metadata

    def __post_init__(self):
        """
        Initialize default values and validate the task after initialization.
        """
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.recurring is None:
            self.recurring = RecurringMetadata()
        self.validate()

    def validate(self):
        """
        Validate the task fields according to the defined rules.
        """
        if not self.title or not self.title.strip():
            raise ValueError("Title is required and cannot be empty")
        if len(self.title) > 500:
            raise ValueError("Title cannot exceed 500 characters")
        if self.description and len(self.description) > 2000:
            raise ValueError("Description cannot exceed 2000 characters")

        # Validate priority
        valid_priorities = ["", "high", "medium", "low"]
        if self.priority not in valid_priorities:
            raise ValueError(f"Priority must be one of {valid_priorities}")

        # Validate due_date format if provided
        if self.due_date:
            try:
                datetime.fromisoformat(self.due_date.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError("Due date must be in ISO format (YYYY-MM-DD)")

        # Validate due_time format if provided
        if self.due_time:
            if not self.due_date:
                raise ValueError("Due time requires a due date to be set")
            try:
                # Validate HH:MM format
                time_parts = self.due_time.split(':')
                if len(time_parts) != 2:
                    raise ValueError("Due time must be in HH:MM format")
                hour, minute = int(time_parts[0]), int(time_parts[1])
                if not (0 <= hour <= 23) or not (0 <= minute <= 59):
                    raise ValueError("Hour must be 0-23 and minute must be 0-59")
            except ValueError:
                raise ValueError("Due time must be in HH:MM format (24-hour)")

        # Validate recurring metadata
        if self.recurring:
            if not isinstance(self.recurring, RecurringMetadata):
                raise ValueError("Recurring must be an instance of RecurringMetadata")
            if self.recurring.enabled and not self.recurring.type:
                raise ValueError("Recurring task must have a recurrence type when enabled")
            if self.recurring.type and self.recurring.type not in RecurrenceType:
                raise ValueError(f"Recurring type must be one of {list(RecurrenceType)}")

        # Validate tags
        if not isinstance(self.tags, list):
            raise ValueError("Tags must be a list")
        for tag in self.tags:
            if not isinstance(tag, str):
                raise ValueError("All tags must be strings")

        # Remove duplicate tags while preserving order
        unique_tags = []
        for tag in self.tags:
            if tag not in unique_tags:
                unique_tags.append(tag)
        self.tags = unique_tags