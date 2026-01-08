# Quickstart Guide: Todo App Intermediate Features

## Overview
This guide provides step-by-step instructions to implement the intermediate features for the todo app: due dates, priorities, tags, search, filtering, and sorting.

## Prerequisites
- Basic todo app with localStorage persistence already implemented
- React with functional components and hooks (useState, useEffect)
- Understanding of the existing task structure

## Step 1: Update Task Data Model
1. Modify the task object structure to include new fields:
   - `dueDate: string | null` - Optional due date in ISO format
   - `priority: "high" | "medium" | "low" | ""` - Priority level
   - `tags: string[]` - Array of tag strings
   - `createdAt: string` - Creation timestamp in ISO format

2. Update localStorage loading to handle existing tasks without new fields:
   - For tasks without dueDate, set to null
   - For tasks without priority, set to ""
   - For tasks without tags, set to []
   - For tasks without createdAt, set to current timestamp

## Step 2: Create New Components
1. Create `SearchBar.jsx` component:
   - Accept search input
   - Emit search term to parent component

2. Create `FilterControls.jsx` component:
   - Provide controls for status, priority, due date, and tag filters
   - Emit filter selections to parent component

3. Create `SortDropdown.jsx` component:
   - Provide sorting options
   - Emit sort selection to parent component

## Step 3: Update Existing Components
1. Update `AddTaskForm.jsx`:
   - Add due date input (using `<input type="date">`)
   - Add priority dropdown (high/medium/low)
   - Add tag input functionality

2. Update `TaskItem.jsx`:
   - Display due date with "Today" or "Overdue" badges
   - Show priority indicator
   - Display tags as removable chips
   - Add controls to edit new properties

3. Update `TaskList.jsx`:
   - Implement filtering logic based on multiple criteria
   - Implement sorting logic
   - Apply filters and sorting in the correct sequence

## Step 4: Implement Business Logic
1. Create `utils/dateUtils.js`:
   - Functions to determine if a task is "Today" or "Overdue"
   - Date comparison utilities

2. Create `utils/taskUtils.js`:
   - Filtering functions for each filter type
   - Sorting functions for each sort option
   - Utility functions for tag management

## Step 5: Integrate Components
1. In the main `App.jsx`:
   - Manage state for tasks, filters, search term, and sort option
   - Pass state and update functions to child components
   - Apply filtering and sorting to the task list before passing to TaskList

## Step 6: Apply Responsive Design
1. Ensure all new UI elements are responsive
2. Test on different screen sizes
3. Adjust layouts for mobile view

## Step 7: Testing
1. Test all new functionality:
   - Adding tasks with due dates, priorities, and tags
   - Searching tasks by title and tags
   - Filtering tasks by various criteria
   - Sorting tasks by different options
   - Editing existing tasks
   - Persistence in localStorage

2. Verify backward compatibility with existing tasks
3. Test edge cases (empty tags, null due dates, etc.)

## Expected Outcome
After completing these steps, your todo app will have:
- Ability to add due dates, priorities, and tags to tasks
- Visual indicators for "Today" and "Overdue" tasks
- Search functionality that works across titles and tags
- Multiple filter options to narrow down the task list
- Sorting options to organize tasks
- Full persistence of new data in localStorage
- Responsive design that works on mobile and desktop