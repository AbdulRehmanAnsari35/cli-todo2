# Detailed Implementation Plan: Todo App Intermediate Features

## 1. Data Model Update Plan

### 1.1 Exact Changes to Task Object Structure
- Current task object: `{ id: string, title: string, completed: boolean }`
- New task object: 
```javascript
{
  id: string,                    // unchanged
  title: string,                 // unchanged
  completed: boolean,            // unchanged
  dueDate: string | null,        // NEW: ISO string like "2025-08-15" or null
  priority: "high" | "medium" | "low" | "", // NEW: priority level or empty
  tags: string[],                // NEW: array of tag strings, e.g. ["work", "urgent"]
  createdAt: string              // NEW: ISO timestamp string
}
```

### 1.2 localStorage Migration Strategy
- On app initialization, when loading tasks from localStorage:
  - For each existing task, check if it has the new fields
  - If `dueDate` is missing, set to `null`
  - If `priority` is missing, set to `""`
  - If `tags` is missing, set to `[]`
  - If `createdAt` is missing, set to current timestamp
- This ensures existing tasks without new fields don't break the app

## 2. Component-Level Implementation Steps

### 2.1 AddTaskForm Component Updates
- Add date input field: `<input type="date" />` for due date
- Add priority dropdown: options for High, Medium, Low, None
- Add tag input functionality:
  - Text input for new tags
  - Button to add tag to temporary list
  - Display current tags as removable chips in the form
  - Remove tag functionality by clicking '×' on chip
- Update form submission to include new fields

### 2.2 TaskItem Component Updates
- Display due date if present, with visual indicator
- Show "Today" badge if due date is today
- Show "Overdue" badge if due date is in the past and task is not completed
- Display priority indicator (color-coded or icon-based)
- Display tags as removable chips inside the task card
- Add edit functionality for due date, priority, and tags
- Update UI to accommodate new information while maintaining clean layout

### 2.3 SearchBar Component (New)
- Create new SearchBar component with:
  - Text input for search term
  - Live search functionality (updates results as user types)
  - Search across task titles and tags
  - Clear search button

### 2.4 FilterControls Component (New)
- Create new FilterControls component with:
  - Status filter: All | Active | Completed (radio buttons or dropdown)
  - Priority filter: All | High Priority (dropdown)
  - Date filter: All | Today | Overdue (dropdown)
  - Tag filter: All Tags | [dropdown with all existing tags] (dropdown)
  - Layout that works responsively on mobile and desktop

### 2.5 SortDropdown Component (New)
- Create new SortDropdown component with:
  - Options: Due Date, Priority, Alphabetically, Creation Date (dropdown)
  - Default to "Creation Date" newest first
  - Visual indication of current sort order

### 2.6 TaskList Component Updates
- Update to accept and apply filters, search term, and sort option
- Implement the filtering and sorting pipeline
- Update rendering to work with filtered/sorted tasks

## 3. State Management Plan

### 3.1 State Location
- **Main App Component**:
  - `tasks`: Array of all tasks (source of truth)
  - `filters`: Object containing current filter selections
  - `searchTerm`: String for current search input
  - `sortOption`: Object defining current sort criteria
- **Component-specific state** (managed within components):
  - AddTaskForm: temporary tag input, form values
  - FilterControls: temporary filter selections before applying
  - SearchBar: debounced search input

### 3.2 Data Flow Between Components
- App component manages all persistent state
- Child components receive props from App
- Child components call callback functions passed from App to update state
- TaskList receives filtered and sorted tasks from App
- Filter changes trigger recomputation in App which passes new task list to TaskList

## 4. Filtering Logic Order

### 4.1 Explicit Filter Application Sequence
1. **Status filter**: Apply first (All/Active/Completed)
2. **Date-based filters**: Apply second (Today/Overdue)
3. **Tag filter**: Apply third (specific tag selection)
4. **Text search**: Apply fourth (search term matching in title/tags)
5. **Sorting**: Apply last (order the final filtered results)

### 4.2 Filter Combination Logic
- All filters work together (AND logic)
- Each subsequent filter operates on the results of the previous filter
- Empty filter values (e.g., "All" options) mean no filtering for that category

## 5. Date Handling Plan

### 5.1 "Today" and "Overdue" Calculation
- "Today" tasks: dueDate === today's date (in YYYY-MM-DD format)
- "Overdue" tasks: dueDate < today's date AND completed === false
- Use JavaScript Date objects for comparisons
- Format dates consistently as YYYY-MM-DD strings

### 5.2 Null Due Date Handling
- Tasks with dueDate === null should not be marked as "Today" or "Overdue"
- In sorting by due date, null dates should appear last

## 6. UI Integration Steps

### 6.1 Control Placement
- **SearchBar**: At the top of the task list, full-width
- **FilterControls**: Below search bar, arranged horizontally on desktop, stacked on mobile
- **SortDropdown**: Top-right of task list area, aligned with search bar
- **AddTaskForm**: Above the task list, with new fields integrated
- **TaskItem**: New information displayed in a clean, organized way within existing card

### 6.2 Mobile Responsiveness
- Use CSS media queries for responsive layouts
- Stack filter controls vertically on small screens
- Ensure tag chips wrap appropriately
- Make sure date inputs are usable on touch devices
- Maintain adequate touch target sizes (minimum 44px)

## 7. Testing & Validation Checklist

### 7.1 Manual Test Cases for Each Feature
- **Due Dates**:
  - Add task with due date
  - Verify "Today" badge appears for today's date
  - Verify "Overdue" badge appears for past dates on incomplete tasks
  - Edit due date
  - Remove due date

- **Priorities**:
  - Add task with priority
  - Verify priority indicator displays correctly
  - Change priority level
  - Verify priority filtering works

- **Tags**:
  - Add tags to task
  - Verify tags display as removable chips
  - Remove tags from task
  - Verify tag filtering works
  - Test adding duplicate tags (should not allow)

- **Search**:
  - Search by task title
  - Search by tags
  - Verify live search updates results
  - Clear search returns all tasks

- **Filters**:
  - Test each filter individually
  - Test filter combinations
  - Reset filters

- **Sorting**:
  - Test each sort option
  - Verify sort order is correct

### 7.2 Edge Cases
- **No due date**: Task should not show "Today" or "Overdue" badge
- **Completed overdue task**: Should not show "Overdue" badge
- **Empty tag list**: Should not break UI
- **Many tags on one task**: Ensure layout doesn't break
- **Very long tag names**: Ensure they're handled gracefully
- **Tasks with special characters in title**: Should be searchable

## 8. Clear Step-by-Step Execution Order

### Phase 1: Data Layer
1. Update task data model in code
2. Implement localStorage migration logic
3. Create utility functions for date calculations
4. Create utility functions for filtering and sorting

### Phase 2: Core Components
5. Update AddTaskForm with new fields
6. Update TaskItem to display new information
7. Create SearchBar component
8. Create FilterControls component
9. Create SortDropdown component

### Phase 3: Integration
10. Update TaskList to handle filtering and sorting
11. Integrate all components in App component
12. Connect state management between components
13. Implement the filtering pipeline in the correct order

### Phase 4: Polish
14. Add responsive design adjustments
15. Implement visual indicators (Today/Overdue badges)
16. Test all functionality together
17. Fix any UI/UX issues
18. Verify localStorage persistence works with new fields

### Phase 5: Validation
19. Test all manual test cases
20. Verify edge cases are handled
21. Confirm backward compatibility with existing tasks
22. Performance test with larger number of tasks