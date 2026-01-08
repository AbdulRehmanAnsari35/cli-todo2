from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Task:
    """
    Represents a todo task with id, title, description, completion status, due date, priority, tags, and creation timestamp.
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[str] = None  # ISO string like "2025-08-15" or None
    priority: str = ""  # "high", "medium", "low", or "" for no priority
    tags: List[str] = None  # List of tag strings, e.g. ["work", "urgent"]
    created_at: str = None  # ISO timestamp string

    def __post_init__(self):
        """
        Initialize default values and validate the task after initialization.
        """
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
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