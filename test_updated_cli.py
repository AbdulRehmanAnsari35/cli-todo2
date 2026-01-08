#!/usr/bin/env python3
"""
Test script to verify the updated CLI application with Intermediate Level features.
"""
import os
import sys
import tempfile
from datetime import datetime

# Add the parent directory to sys.path so that we can import src modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.models.task import Task
from src.services.task_service import TaskService
from src.cli.command_handler import CommandHandler
from src.utils.date_utils import is_today, is_overdue, get_today_string


def test_command_handler():
    """Test the updated command handler functionality."""
    print("Testing updated command handler functionality...")
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create task service with temp file
        service = TaskService(storage_file=temp_filename)
        handler = CommandHandler(service)
        
        # Test adding a task with new fields
        add_result = handler.handle_add([
            "Test Task", 
            "Test Description", 
            "--due", get_today_string(), 
            "--priority", "high", 
            "--tags", "work,urgent"
        ])
        print(f"Add result: {add_result}")
        assert "Task added with ID:" in add_result
        
        # Test listing tasks
        list_result = handler.handle_list([])
        print(f"List result (first 200 chars): {list_result[:200]}...")
        
        # Test updating a task with specific fields
        update_result = handler.handle_update([
            "1", 
            "--priority", "medium"
        ])
        print(f"Update result: {update_result}")
        assert "updated successfully" in update_result
        
        # Test updating priority only
        update_priority_result = handler.handle_update([
            "1", 
            "priority", 
            "low"
        ])
        print(f"Update priority result: {update_priority_result}")
        assert "priority updated to low" in update_priority_result
        
        # Test updating tags only
        update_tags_result = handler.handle_update([
            "1", 
            "tags", 
            "personal,not-urgent"
        ])
        print(f"Update tags result: {update_tags_result}")
        assert "tags updated to" in update_tags_result
        
        # Test list with search
        search_result = handler.handle_list(["--search", "test"])
        print(f"Search result (first 200 chars): {search_result[:200]}...")
        
        # Test list with filter
        filter_result = handler.handle_list(["--filter", "priority=low"])
        print(f"Filter result (first 200 chars): {filter_result[:200]}...")
        
        # Test list with sort
        sort_result = handler.handle_list(["--sort", "title"])
        print(f"Sort result (first 200 chars): {sort_result[:200]}...")
        
        print("✓ All command handler tests passed")
    finally:
        # Clean up temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_task_model():
    """Test the updated task model."""
    print("Testing updated task model...")
    
    # Test creating a task with all new fields
    task = Task(
        id=1,
        title="Test Task",
        description="Test Description",
        due_date=get_today_string(),
        priority="high",
        tags=["work", "urgent"]
    )
    
    assert task.title == "Test Task"
    assert task.due_date == get_today_string()
    assert task.priority == "high"
    assert "work" in task.tags
    assert "urgent" in task.tags
    assert task.created_at is not None
    
    # Test duplicate tag removal
    task_with_dups = Task(
        id=2,
        title="Test Task",
        tags=["work", "urgent", "work", "personal", "urgent"]  # Duplicates
    )
    
    # Should have unique tags only
    expected_tags = {"work", "urgent", "personal"}
    actual_tags = set(task_with_dups.tags)
    assert actual_tags == expected_tags
    assert len(task_with_dups.tags) == 3  # Should have 3 unique tags
    
    print("✓ Task model tests passed")


def run_all_tests():
    """Run all tests."""
    print("Running tests for updated CLI application with Intermediate Level features...\n")
    
    test_task_model()
    test_command_handler()
    
    print("\n✓ All tests passed! The CLI application with Intermediate Level features is working correctly.")


if __name__ == "__main__":
    run_all_tests()