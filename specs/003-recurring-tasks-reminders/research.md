# Research Summary: Advanced Level Features (Recurring Tasks & Time-Based Reminders)

## Date Manipulation in Python

### Decision: Use Python's datetime and timedelta modules for recurring calculations
- **Rationale**: Python's datetime module provides robust methods for date arithmetic and handles edge cases like month boundaries and leap years automatically
- **Implementation**: Use `datetime.timedelta` for daily recurrences and `relativedelta` from `dateutil` for weekly/monthly recurrences

### Alternatives considered:
- Manual date calculation: Would require extensive logic to handle edge cases
- Third-party libraries: dateutil is the standard library for complex date operations

## CLI Argument Parsing

### Decision: Extend existing argparse or similar library to support new flags
- **Rationale**: Most Python CLI applications use argparse or similar libraries that support optional flags
- **Implementation**: Add optional arguments --recurring, --due, and --time to existing command parsers

### Alternatives considered:
- Positional arguments: Less flexible and harder to use
- Configuration files: Overkill for simple flag-based options

## Time Comparison Logic

### Decision: Use datetime objects for all time comparisons
- **Rationale**: Converting strings to datetime objects enables accurate time arithmetic and comparisons
- **Implementation**: Parse due date/time strings into datetime objects for comparison with current time

### Alternatives considered:
- String-based comparisons: Unreliable for time calculations
- Unix timestamps: More complex than necessary for this use case

## In-Memory Persistence

### Decision: Store recurring tasks in the same in-memory structure as regular tasks
- **Rationale**: Maintains consistency with existing architecture while adding required functionality
- **Implementation**: Extend the existing task list/dictionary with enhanced task objects containing recurring metadata

### Alternatives considered:
- Separate storage for recurring tasks: Would complicate the codebase unnecessarily
- File-based persistence: Against the constitution's in-memory requirement