import re
from typing import List, Optional
from src.services.task_service import TaskService


class CommandHandler:
    """
    Handles command parsing and execution for the Todo Console App.
    """

    def __init__(self, task_service: TaskService):
        """
        Initialize the command handler with a task service.

        Args:
            task_service: The service to handle task operations
        """
        self.task_service = task_service

    def handle_command(self, user_input: str) -> Optional[str]:
        """
        Parse and execute the user command.

        Args:
            user_input: The raw input from the user

        Returns:
            A string response to display to the user, or None for no output
        """
        # Parse the command and arguments
        command, args = self.parse_command(user_input)

        # Execute the appropriate command
        if command == "add":
            return self.handle_add(args)
        elif command == "list":
            return self.handle_list()
        elif command == "update":
            return self.handle_update(args)
        elif command == "delete":
            return self.handle_delete(args)
        elif command == "complete":
            return self.handle_complete(args)
        elif command == "help":
            return self.handle_help()
        elif command == "exit":
            # Exit is handled in main.py
            return None
        else:
            return f"Unknown command: {command}. Type 'help' for available commands."

    def parse_command(self, user_input: str) -> tuple[str, List[str]]:
        """
        Parse the user input into a command and arguments.
        Handles quoted strings as single arguments.

        Args:
            user_input: The raw input from the user

        Returns:
            A tuple of (command, arguments list)
        """
        # Split the input by spaces, but preserve quoted strings
        pattern = r'"([^"]*)"|\'([^\']*)\'|(\S+)'
        matches = re.findall(pattern, user_input)

        # Extract the actual matched string from each match
        tokens = [match[0] or match[1] or match[2] for match in matches]

        if not tokens:
            return "", []

        command = tokens[0].lower()
        args = tokens[1:]

        return command, args

    def handle_add(self, args: List[str]) -> str:
        """
        Handle the 'add' command to create a new task.

        Args:
            args: List of arguments [title, optional description]

        Returns:
            A string response to display to the user
        """
        if len(args) < 1:
            return "Add command requires a title. Usage: add <title> [description]"

        title = args[0]
        description = args[1] if len(args) > 1 else None

        try:
            task_id = self.task_service.add_task(title, description)
            return f"Task added with ID: {task_id}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def handle_list(self) -> str:
        """
        Handle the 'list' command to display all tasks.

        Returns:
            A string response to display to the user
        """
        tasks = self.task_service.get_all_tasks()

        if not tasks:
            return "No tasks found."

        # Create a formatted table of tasks
        result = f"{'ID':<4} {'Title':<20} {'Description':<30} {'Status':<10}\n"
        result += "-" * 70 + "\n"

        for task in tasks:
            status = "Complete" if task.completed else "Incomplete"
            description = task.description if task.description else ""
            result += f"{task.id:<4} {task.title[:19]:<20} {description[:29]:<30} {status:<10}\n"

        return result

    def handle_update(self, args: List[str]) -> str:
        """
        Handle the 'update' command to modify an existing task.

        Args:
            args: List of arguments [id, optional title, optional description]

        Returns:
            A string response to display to the user
        """
        if len(args) < 2:
            return "Update command requires an ID and at least one field to update. Usage: update <id> [title] [description]"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Task ID must be a number"

        # Determine which fields to update
        title = args[1] if len(args) > 1 and args[1] != "" else None
        description = args[2] if len(args) > 2 and args[2] != "" else None

        # At least one field must be provided for update
        if title is None and description is None:
            return "Error: At least title or description must be provided for update"

        success = self.task_service.update_task(task_id, title, description)
        if success:
            return f"Task {task_id} updated successfully"
        else:
            return f"Error: Task with ID {task_id} does not exist"

    def handle_delete(self, args: List[str]) -> str:
        """
        Handle the 'delete' command to remove a task.

        Args:
            args: List of arguments [id]

        Returns:
            A string response to display to the user
        """
        if len(args) < 1:
            return "Delete command requires an ID. Usage: delete <id>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Task ID must be a number"

        success = self.task_service.delete_task(task_id)
        if success:
            return f"Task {task_id} deleted successfully"
        else:
            return f"Error: Task with ID {task_id} does not exist"

    def handle_complete(self, args: List[str]) -> str:
        """
        Handle the 'complete' command to toggle task completion status.

        Args:
            args: List of arguments [id]

        Returns:
            A string response to display to the user
        """
        if len(args) < 1:
            return "Complete command requires an ID. Usage: complete <id>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Task ID must be a number"

        success = self.task_service.toggle_task_completion(task_id)
        if success:
            task = self.task_service.get_task_by_id(task_id)
            status = "complete" if task.completed else "incomplete"
            return f"Task {task_id} marked as {status}"
        else:
            return f"Error: Task with ID {task_id} does not exist"

    def handle_help(self) -> str:
        """
        Handle the 'help' command to display available commands.

        Returns:
            A string response to display to the user
        """
        help_text = """
Available commands:
  add <title> [description]    - Add a new task
  list                        - List all tasks
  update <id> [title] [description] - Update a task
  delete <id>                 - Delete a task
  complete <id>               - Toggle task completion status
  help                        - Show this help message
  exit                        - Quit the application
        """
        return help_text