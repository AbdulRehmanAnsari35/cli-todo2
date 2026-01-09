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
            return self.handle_list(args)
        elif command == "update":
            return self.handle_update(args)
        elif command == "delete":
            return self.handle_delete(args)
        elif command == "complete":
            return self.handle_complete(args)
        elif command == "filter":
            return self.handle_filter(args)
        elif command == "search":
            return self.handle_search(args)
        elif command == "sort":
            return self.handle_sort(args)
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
        Handle the 'add' command to create a new task with due date, due time, priority, tags, and recurring properties.

        Args:
            args: List of arguments [title, optional description, optional --due, optional due_date,
                  optional --time, optional due_time, optional --priority, optional priority_level,
                  optional --tags, optional tag1,tag2,..., optional --recurring, optional recurrence_type]

        Returns:
            A string response to display to the user
        """
        if len(args) < 1:
            return "Add command requires a title. Usage: add <title> [description] [--due YYYY-MM-DD] [--time HH:MM] [--priority high|medium|low] [--tags tag1,tag2,...] [--recurring daily|weekly|monthly]"

        title = args[0]
        description = None
        due_date = None
        due_time = None
        priority = ""
        tags = []
        recurring_enabled = False
        recurring_type = None

        i = 1
        while i < len(args):
            arg = args[i]
            if arg == "--due" and i + 1 < len(args):
                due_date = args[i + 1]
                i += 2
            elif arg == "--time" and i + 1 < len(args):
                due_time = args[i + 1]
                i += 2
            elif arg == "--priority" and i + 1 < len(args):
                priority = args[i + 1]
                i += 2
            elif arg == "--tags" and i + 1 < len(args):
                tags = [tag.strip() for tag in args[i + 1].split(",")]
                i += 2
            elif arg == "--recurring" and i + 1 < len(args):
                recurring_type_str = args[i + 1].lower()
                if recurring_type_str in ["daily", "weekly", "monthly"]:
                    from src.models.task import RecurrenceType
                    recurring_type = RecurrenceType(recurring_type_str)
                    recurring_enabled = True
                    i += 2
                else:
                    return f"Error: Invalid recurrence type '{recurring_type_str}'. Must be daily, weekly, or monthly."
            elif description is None:
                description = arg
                i += 1
            else:
                i += 1

        # Validate that due_time requires due_date
        if due_time and not due_date:
            return "Error: Due time requires a due date to be set."

        try:
            task_id = self.task_service.add_task(
                title, description, due_date, priority, tags,
                due_time=due_time,
                recurring_enabled=recurring_enabled,
                recurring_type=recurring_type
            )
            return f"Task added with ID: {task_id}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def handle_list(self, args: List[str] = None) -> str:
        """
        Handle the 'list' command to display all tasks with new fields and filtering options.

        Args:
            args: List of arguments for filtering and sorting

        Returns:
            A string response to display to the user
        """
        from src.utils.date_utils import is_today, is_overdue, format_date_for_display
        from src.utils.filter_utils import apply_filters
        from src.utils.sort_utils import apply_sorting

        # Parse arguments for filtering and sorting
        search_term = None
        status_filter = 'all'
        priority_filter = 'all'
        tag_filter = 'all'
        due_date_filter = 'all'
        sort_type = None
        sort_direction = 'asc'

        if args:
            i = 0
            while i < len(args):
                arg = args[i]

                # Search option
                if arg == "--search" and i + 1 < len(args):
                    search_term = args[i + 1].lower()
                    i += 2
                # Filter options
                elif arg == "--filter" and i + 1 < len(args):
                    filter_arg = args[i + 1]
                    if filter_arg.startswith("status="):
                        status_filter = filter_arg.split("=")[1]
                    elif filter_arg.startswith("priority="):
                        priority_filter = filter_arg.split("=")[1]
                    elif filter_arg.startswith("tag="):
                        tag_filter = filter_arg.split("=")[1]
                    elif filter_arg.startswith("due="):
                        due_date_filter = filter_arg.split("=")[1]
                    i += 2
                # Sort option
                elif arg == "--sort" and i + 1 < len(args):
                    sort_type = args[i + 1]
                    i += 2
                # Descending order
                elif arg == "--desc":
                    sort_direction = 'desc'
                    i += 1
                else:
                    i += 1

        # Get all tasks
        tasks = self.task_service.get_all_tasks()

        # Apply search if specified
        if search_term:
            tasks = [
                task for task in tasks
                if search_term in task.title.lower() or
                search_term in (task.description or "").lower() or
                any(search_term in tag.lower() for tag in task.tags)
            ]

        # Apply filters if not using search
        if not search_term:  # Only apply filters if not using search
            # Map status filter values
            if status_filter == "pending":
                status_filter = "active"
            elif status_filter == "completed":
                status_filter = "completed"
            elif status_filter not in ["all", "active", "completed"]:
                status_filter = "all"

            # Map due date filter values
            if due_date_filter == "today":
                due_date_filter = "today"
            elif due_date_filter == "overdue":
                due_date_filter = "overdue"
            elif due_date_filter not in ["all", "today", "overdue"]:
                due_date_filter = "all"

            # Map priority filter values
            if priority_filter not in ["all", "high", "medium", "low"]:
                priority_filter = "all"

            # Map tag filter values
            if tag_filter == "all":
                tag_filter = "all"
            # If tag_filter is not 'all', leave it as is (it could be a specific tag)

            tasks = apply_filters(tasks, status_filter, priority_filter, due_date_filter, tag_filter)

        # Apply sorting
        if sort_type:
            # Map the sort type to the expected values in sort_utils
            if sort_type == "title":
                sort_type = "alphabetical"
            elif sort_type == "created":
                sort_type = "creation_date"
            # For "priority", it's already correct
            tasks = apply_sorting(tasks, sort_type, sort_direction)

        if not tasks:
            return "No tasks found."

        # Create a formatted table of tasks
        result = f"{'ID':<4} {'Title':<20} {'Description':<25} {'Due Date':<15} {'Due Time':<10} {'Recurring':<12} {'Priority':<10} {'Tags':<20} {'Status':<12}\n"
        result += "-" * 120 + "\n"

        for task in tasks:
            status = "Complete" if task.completed else "Incomplete"
            description = task.description if task.description else ""

            # Format due date and add "Today" or "Overdue" indicators
            due_date_display = format_date_for_display(task.due_date) if task.due_date else ""
            if task.due_date and is_today(task.due_date):
                due_date_display += " (Today)"
            elif task.due_date and is_overdue(task.due_date, task.completed):
                due_date_display += " (Overdue)"

            # Format due time
            due_time_display = task.due_time if task.due_time else ""

            # Format recurring info
            recurring_info = ""
            if task.recurring and task.recurring.enabled and task.recurring.type:
                recurring_info = task.recurring.type.value
            else:
                recurring_info = "No"

            # Format tags as a comma-separated string
            tags_str = ", ".join(task.tags) if task.tags else ""

            result += f"{task.id:<4} {task.title[:19]:<20} {description[:24]:<25} {due_date_display:<15} {due_time_display:<10} {recurring_info:<12} {task.priority:<10} {tags_str:<20} {status:<12}\n"

        return result

    def handle_update(self, args: List[str]) -> str:
        """
        Handle the 'update' command to modify an existing task with new fields.

        Args:
            args: List of arguments [id, optional --title, optional new_title,
                  optional --description, optional new_description,
                  optional --due, optional new_due_date,
                  optional --time, optional new_due_time,
                  optional --priority, optional new_priority,
                  optional --tags, optional new_tags,
                  optional --recurring, optional new_recurrence_type]
                  OR [id, priority, high|medium|low]
                  OR [id, tags, tag1,tag2,...]

        Returns:
            A string response to display to the user
        """
        if len(args) < 1:
            return "Update command requires an ID. Usage: update <id> [--title new_title] [--description new_desc] [--due YYYY-MM-DD] [--time HH:MM] [--priority high|medium|low] [--tags tag1,tag2,...] [--recurring daily|weekly|monthly|none] OR update <id> priority <high|medium|low> OR update <id> tags <tag1,tag2,...>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Task ID must be a number"

        # Check if task exists
        task = self.task_service.get_task_by_id(task_id)
        if not task:
            return f"Error: Task with ID {task_id} does not exist"

        # Check for simplified syntax: update <id> priority <level>
        if len(args) == 3 and args[1] == "priority":
            priority = args[2]
            valid_priorities = ["high", "medium", "low"]
            if priority not in valid_priorities:
                return f"Error: Priority must be one of {valid_priorities}"

            success = self.task_service.update_task(task_id, priority=priority)
            if success:
                return f"Task {task_id} priority updated to {priority}"
            else:
                return f"Error: Failed to update task with ID {task_id}"

        # Check for simplified syntax: update <id> tags <tag1,tag2,...>
        if len(args) == 3 and args[1] == "tags":
            tags = [tag.strip() for tag in args[2].split(",")]

            success = self.task_service.update_task(task_id, tags=tags)
            if success:
                return f"Task {task_id} tags updated to {', '.join(tags)}"
            else:
                return f"Error: Failed to update task with ID {task_id}"

        # Parse arguments for updates using flag-based syntax
        title = None
        description = None
        due_date = None
        due_time = None
        priority = None
        tags = None
        recurring_enabled = None
        recurring_type = None

        i = 1
        while i < len(args):
            arg = args[i]
            if arg == "--title" and i + 1 < len(args):
                title = args[i + 1]
                i += 2
            elif arg == "--description" and i + 1 < len(args):
                description = args[i + 1]
                i += 2
            elif arg == "--due" and i + 1 < len(args):
                due_date = args[i + 1]
                i += 2
            elif arg == "--time" and i + 1 < len(args):
                due_time = args[i + 1]
                i += 2
            elif arg == "--priority" and i + 1 < len(args):
                priority = args[i + 1]
                i += 2
            elif arg == "--tags" and i + 1 < len(args):
                tags = [tag.strip() for tag in args[i + 1].split(",")]
                i += 2
            elif arg == "--recurring" and i + 1 < len(args):
                recurring_type_str = args[i + 1].lower()
                if recurring_type_str in ["daily", "weekly", "monthly"]:
                    from src.models.task import RecurrenceType
                    recurring_type = RecurrenceType(recurring_type_str)
                    recurring_enabled = True
                    i += 2
                elif recurring_type_str == "none":
                    recurring_enabled = False
                    recurring_type = None
                    i += 2
                else:
                    return f"Error: Invalid recurrence type '{recurring_type_str}'. Must be daily, weekly, monthly, or none"
            else:
                i += 1

        # Validate that due_time requires due_date
        if due_time and not due_date:
            return "Error: Due time requires a due date to be set."

        # At least one field must be provided for update
        if all(field is None for field in [title, description, due_date, due_time, priority, tags, recurring_enabled]):
            return "Error: At least one field (--title, --description, --due, --time, --priority, --tags, --recurring) must be provided for update"

        success = self.task_service.update_task(
            task_id, title, description, due_date, priority, tags,
            due_time=due_time,
            recurring_enabled=recurring_enabled,
            recurring_type=recurring_type
        )
        if success:
            return f"Task {task_id} updated successfully"
        else:
            return f"Error: Failed to update task with ID {task_id}"

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

    def handle_filter(self, args: List[str]) -> str:
        """
        Handle the 'filter' command to filter tasks by various criteria.

        Args:
            args: List of arguments for filtering [options]

        Returns:
            A string response to display to the user
        """
        from src.utils.filter_utils import apply_filters
        from src.utils.date_utils import is_today, is_overdue, format_date_for_display

        # Default filter values
        status_filter = 'all'
        priority_filter = 'all'
        due_date_filter = 'all'
        tag_filter = 'all'

        # Parse filter arguments
        i = 0
        while i < len(args):
            arg = args[i]
            if arg == "--status" and i + 1 < len(args):
                status_filter = args[i + 1]
                i += 2
            elif arg == "--priority" and i + 1 < len(args):
                priority_filter = args[i + 1]
                i += 2
            elif arg == "--due" and i + 1 < len(args):
                due_date_filter = args[i + 1]
                i += 2
            elif arg == "--tag" and i + 1 < len(args):
                tag_filter = args[i + 1]
                i += 2
            else:
                i += 1

        # Get all tasks and apply filters
        all_tasks = self.task_service.get_all_tasks()
        filtered_tasks = apply_filters(all_tasks, status_filter, priority_filter, due_date_filter, tag_filter)

        if not filtered_tasks:
            return "No tasks match the specified filters."

        # Create a formatted table of filtered tasks
        result = f"{'ID':<4} {'Title':<20} {'Description':<25} {'Due Date':<12} {'Priority':<10} {'Tags':<20} {'Status':<12}\n"
        result += "-" * 90 + "\n"

        for task in filtered_tasks:
            status = "Complete" if task.completed else "Incomplete"
            description = task.description if task.description else ""

            # Format due date and add "Today" or "Overdue" indicators
            due_date_display = format_date_for_display(task.due_date)
            if is_today(task.due_date):
                due_date_display += " (Today)"
            elif is_overdue(task.due_date, task.completed):
                due_date_display += " (Overdue)"

            # Format tags as a comma-separated string
            tags_str = ", ".join(task.tags) if task.tags else ""

            result += f"{task.id:<4} {task.title[:19]:<20} {description[:24]:<25} {due_date_display:<12} {task.priority:<10} {tags_str:<20} {status:<12}\n"

        return result

    def handle_search(self, args: List[str]) -> str:
        """
        Handle the 'search' command to search tasks by title or tags.

        Args:
            args: List of arguments [search_term]

        Returns:
            A string response to display to the user
        """
        if len(args) < 1:
            return "Search command requires a search term. Usage: search <term>"

        search_term = args[0].lower()

        # Get all tasks and filter based on search term
        all_tasks = self.task_service.get_all_tasks()
        matching_tasks = [
            task for task in all_tasks
            if search_term in task.title.lower() or
            search_term in (task.description or "").lower() or
            any(search_term in tag.lower() for tag in task.tags)
        ]

        if not matching_tasks:
            return f"No tasks match the search term '{search_term}'."

        # Create a formatted table of matching tasks
        from src.utils.date_utils import is_today, is_overdue, format_date_for_display

        result = f"{'ID':<4} {'Title':<20} {'Description':<25} {'Due Date':<12} {'Priority':<10} {'Tags':<20} {'Status':<12}\n"
        result += "-" * 90 + "\n"

        for task in matching_tasks:
            status = "Complete" if task.completed else "Incomplete"
            description = task.description if task.description else ""

            # Format due date and add "Today" or "Overdue" indicators
            due_date_display = format_date_for_display(task.due_date)
            if is_today(task.due_date):
                due_date_display += " (Today)"
            elif is_overdue(task.due_date, task.completed):
                due_date_display += " (Overdue)"

            # Format tags as a comma-separated string
            tags_str = ", ".join(task.tags) if task.tags else ""

            result += f"{task.id:<4} {task.title[:19]:<20} {description[:24]:<25} {due_date_display:<12} {task.priority:<10} {tags_str:<20} {status:<12}\n"

        return result

    def handle_sort(self, args: List[str]) -> str:
        """
        Handle the 'sort' command to sort tasks by various criteria.

        Args:
            args: List of arguments [options]

        Returns:
            A string response to display to the user
        """
        from src.utils.sort_utils import apply_sorting
        from src.utils.date_utils import is_today, is_overdue, format_date_for_display

        # Default sort values
        sort_type = 'creation_date'
        sort_direction = 'desc'

        # Parse sort arguments
        i = 0
        while i < len(args):
            arg = args[i]
            if arg == "--by" and i + 1 < len(args):
                sort_type = args[i + 1]
                i += 2
            elif arg == "--order" and i + 1 < len(args):
                sort_direction = args[i + 1]
                i += 2
            else:
                i += 1

        # Get all tasks and apply sorting
        all_tasks = self.task_service.get_all_tasks()
        sorted_tasks = apply_sorting(all_tasks, sort_type, sort_direction)

        if not sorted_tasks:
            return "No tasks to display."

        # Create a formatted table of sorted tasks
        result = f"{'ID':<4} {'Title':<20} {'Description':<25} {'Due Date':<12} {'Priority':<10} {'Tags':<20} {'Status':<12}\n"
        result += "-" * 90 + "\n"

        for task in sorted_tasks:
            status = "Complete" if task.completed else "Incomplete"
            description = task.description if task.description else ""

            # Format due date and add "Today" or "Overdue" indicators
            due_date_display = format_date_for_display(task.due_date)
            if is_today(task.due_date):
                due_date_display += " (Today)"
            elif is_overdue(task.due_date, task.completed):
                due_date_display += " (Overdue)"

            # Format tags as a comma-separated string
            tags_str = ", ".join(task.tags) if task.tags else ""

            result += f"{task.id:<4} {task.title[:19]:<20} {description[:24]:<25} {due_date_display:<12} {task.priority:<10} {tags_str:<20} {status:<12}\n"

        return result

    def handle_help(self) -> str:
        """
        Handle the 'help' command to display available commands.

        Returns:
            A string response to display to the user
        """
        help_text = """
Available commands:
  add <title> [description] [--due YYYY-MM-DD] [--time HH:MM] [--priority high|medium|low] [--tags tag1,tag2,...] [--recurring daily|weekly|monthly] - Add a new task
  list [--search keyword] [--filter status=pending|completed|priority=high|medium|low|tag=tagname|due=today|overdue] [--sort priority|title|created] [--desc] - List tasks with optional filters and sorting
  update <id> [--title new_title] [--description new_desc] [--due YYYY-MM-DD] [--time HH:MM] [--priority high|medium|low] [--tags tag1,tag2,...] [--recurring daily|weekly|monthly|none] - Update a task with specific fields
  update <id> priority <high|medium|low> - Update only the priority of a task
  update <id> tags <tag1,tag2,...> - Update only the tags of a task
  delete <id>                 - Delete a task
  complete <id>               - Toggle task completion status
  help                        - Show this help message
  exit                        - Quit the application
        """
        return help_text