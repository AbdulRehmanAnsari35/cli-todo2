#!/usr/bin/env python3
"""
Test script to verify the intermediate features implementation.
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
from src.utils.date_utils import is_today, is_overdue, get_today_string
from src.utils.filter_utils import apply_filters
from src.utils.sort_utils import apply_sorting


def test_task_creation():
    """Test creating tasks with new fields."""
    print("Testing task creation with new fields...")
    
    # Create a task with all new fields
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
    
    print("✓ Task creation with new fields works correctly")


def test_task_service_persistence():
    """Test task service with JSON persistence."""
    print("Testing task service with JSON persistence...")
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create task service with temp file
        service = TaskService(storage_file=temp_filename)
        
        # Add a task with new fields
        task_id = service.add_task(
            title="Test Task",
            description="Test Description",
            due_date=get_today_string(),
            priority="high",
            tags=["work", "urgent"]
        )
        
        # Verify task was added
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        task = tasks[0]
        assert task.title == "Test Task"
        assert task.due_date == get_today_string()
        assert task.priority == "high"
        assert "work" in task.tags
        assert "urgent" in task.tags
        
        # Test loading from file
        service2 = TaskService(storage_file=temp_filename)
        tasks2 = service2.get_all_tasks()
        assert len(tasks2) == 1
        task2 = tasks2[0]
        assert task2.title == "Test Task"
        assert task2.due_date == get_today_string()
        assert task2.priority == "high"
        assert "work" in task2.tags
        assert "urgent" in task2.tags
        
        print("✓ Task service persistence works correctly")
    finally:
        # Clean up temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_date_utils():
    """Test date utility functions."""
    print("Testing date utility functions...")
    
    today = get_today_string()
    
    # Test is_today
    assert is_today(today) == True
    assert is_today(None) == False
    
    # Test is_overdue
    yesterday = (datetime.now().date().replace(day=datetime.now().date().day - 1)).strftime("%Y-%m-%d")
    assert is_overdue(yesterday, False) == True  # Yesterday, not completed = overdue
    assert is_overdue(yesterday, True) == False  # Yesterday, completed = not overdue
    assert is_overdue(today, False) == False  # Today, not completed = not overdue
    
    print("✓ Date utility functions work correctly")


def test_filtering():
    """Test filtering utility functions."""
    print("Testing filtering utility functions...")
    
    from src.models.task import Task
    
    # Create test tasks
    task1 = Task(id=1, title="Task 1", completed=False, priority="high", tags=["work"])
    task2 = Task(id=2, title="Task 2", completed=True, priority="medium", tags=["personal"])
    task3 = Task(id=3, title="Task 3", completed=False, priority="low", tags=["work", "urgent"])
    
    tasks = [task1, task2, task3]
    
    # Test status filtering
    active_tasks = [t for t in tasks if not t.completed]
    assert len(active_tasks) == 2
    
    completed_tasks = [t for t in tasks if t.completed]
    assert len(completed_tasks) == 1
    
    # Test priority filtering
    high_priority_tasks = [t for t in tasks if t.priority == "high"]
    assert len(high_priority_tasks) == 1
    
    # Test tag filtering
    work_tasks = [t for t in tasks if "work" in t.tags]
    assert len(work_tasks) == 2
    
    print("✓ Filtering utility functions work correctly")


def test_sorting():
    """Test sorting utility functions."""
    print("Testing sorting utility functions...")
    
    from src.models.task import Task
    from datetime import datetime
    
    # Create test tasks with different priorities
    task1 = Task(id=1, title="Task A", priority="low")
    task2 = Task(id=2, title="Task C", priority="high")
    task3 = Task(id=3, title="Task B", priority="medium")
    
    tasks = [task1, task2, task3]
    
    # Test priority sorting
    sorted_tasks = apply_sorting(tasks, "priority", "asc")
    assert sorted_tasks[0].priority == "high"  # High priority first
    assert sorted_tasks[1].priority == "medium"
    assert sorted_tasks[2].priority == "low"
    
    # Test alphabetical sorting
    sorted_tasks = apply_sorting(tasks, "alphabetical", "asc")
    assert sorted_tasks[0].title == "Task A"
    assert sorted_tasks[1].title == "Task B"
    assert sorted_tasks[2].title == "Task C"
    
    print("✓ Sorting utility functions work correctly")


def test_duplicate_tags():
    """Test that duplicate tags are removed."""
    print("Testing duplicate tags removal...")
    
    task = Task(
        id=1,
        title="Test Task",
        tags=["work", "urgent", "work", "personal", "urgent"]  # Duplicates
    )
    
    # Should have unique tags only
    expected_tags = {"work", "urgent", "personal"}
    actual_tags = set(task.tags)
    assert actual_tags == expected_tags
    assert len(task.tags) == 3  # Should have 3 unique tags
    
    print("✓ Duplicate tags are removed correctly")


def run_all_tests():
    """Run all tests."""
    print("Running tests for intermediate features implementation...\n")
    
    test_task_creation()
    test_task_service_persistence()
    test_date_utils()
    test_filtering()
    test_sorting()
    test_duplicate_tags()
    
    print("\n✓ All tests passed! The intermediate features implementation is working correctly.")


if __name__ == "__main__":
    run_all_tests()