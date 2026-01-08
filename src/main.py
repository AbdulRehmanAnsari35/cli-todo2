#!/usr/bin/env python3
"""
Entry point for the Todo Python Console App.
This file contains the main REPL loop that processes user commands.
"""

import sys
import os

# Add the parent directory to sys.path so that we can import src modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.services.task_service import TaskService
from src.cli.command_handler import CommandHandler


def main():
    """
    Main entry point for the application.
    Initializes the service and starts the REPL loop.
    """
    print("Welcome to the Todo Python Console App! Type 'help' for available commands or 'exit' to quit.")

    # Initialize the task service and command handler
    task_service = TaskService(storage_file="tasks.json")  # Use JSON file for persistence
    command_handler = CommandHandler(task_service)

    # Start the REPL loop
    while True:
        try:
            # Get user input
            user_input = input("> ").strip()

            # Process the command
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            elif user_input.lower() == '':
                continue  # Ignore empty commands
            else:
                # Handle the command
                result = command_handler.handle_command(user_input)
                if result:
                    print(result)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()