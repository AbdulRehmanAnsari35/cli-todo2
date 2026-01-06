from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a todo task with id, title, description, and completion status.
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """
        Validate the task after initialization.
        """
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