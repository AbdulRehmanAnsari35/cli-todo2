---

description: "Task list for Todo Python Console App implementation"
---

# Tasks: Todo Python Console App

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure: /src, /src/models, /src/services, /src/cli
- [x] T002 Initialize pyproject.toml with Python 3.13+ requirement and UV configuration
- [x] T003 [P] Create placeholder files: src/main.py, src/models/task.py, src/services/task_service.py, src/cli/command_handler.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Task model with id, title, description, completed fields in src/models/task.py
- [x] T005 [P] Implement Task validation rules (title required, description optional, etc.)
- [x] T006 Create TaskService with in-memory storage using dictionary in src/services/task_service.py
- [x] T007 [P] Implement ID generation mechanism (auto-incrementing counter)
- [x] T008 Create basic REPL loop structure in src/main.py
- [x] T009 [P] Implement command parsing functionality in src/cli/command_handler.py
- [x] T010 Implement basic error handling infrastructure
- [x] T011 [P] Add startup banner display in src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Todo Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo tasks with a title and optional description

**Independent Test**: Can be fully tested by running the `add` command with a title and verifying that a task is created with a unique ID and displayed in the list.

### Implementation for User Story 1

- [x] T012 [P] [US1] Implement add command handler in src/cli/command_handler.py
- [x] T013 [US1] Implement add_task method in src/services/task_service.py
- [x] T014 [US1] Handle title and optional description parsing in command handler
- [x] T015 [US1] Validate that title is provided when adding tasks
- [x] T016 [US1] Return unique task ID when task is successfully added
- [x] T017 [US1] Test adding tasks with and without descriptions

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Todo Tasks (Priority: P1)

**Goal**: Enable users to view all their todo tasks with ID, title, description, and completion status

**Independent Test**: Can be fully tested by adding tasks and then running the `list` command to verify all tasks are displayed with their details.

### Implementation for User Story 2

- [x] T018 [P] [US2] Implement list command handler in src/cli/command_handler.py
- [x] T019 [US2] Implement get_all_tasks method in src/services/task_service.py
- [x] T020 [US2] Format task list output as a table with ID, Title, Description, and Status
- [x] T021 [US2] Handle case when no tasks exist (display "No tasks found.")
- [x] T022 [US2] Test listing tasks with various completion statuses

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Existing Todo Task (Priority: P2)

**Goal**: Enable users to update the title or description of an existing task

**Independent Test**: Can be fully tested by adding a task, updating it with the `update` command, and verifying the changes are reflected when listing tasks.

### Implementation for User Story 3

- [x] T023 [P] [US3] Implement update command handler in src/cli/command_handler.py
- [x] T024 [US3] Implement update_task method in src/services/task_service.py
- [x] T025 [US3] Handle ID, optional title, and optional description parsing
- [x] T026 [US3] Validate that task exists before updating
- [x] T027 [US3] Implement partial update logic (update only provided fields)
- [x] T028 [US3] Test updating tasks with various parameter combinations

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Todo Task (Priority: P2)

**Goal**: Enable users to delete tasks that they no longer need

**Independent Test**: Can be fully tested by adding a task, deleting it with the `delete` command, and verifying it no longer appears in the list.

### Implementation for User Story 4

- [x] T029 [P] [US4] Implement delete command handler in src/cli/command_handler.py
- [x] T030 [US4] Implement delete_task method in src/services/task_service.py
- [x] T031 [US4] Handle ID parsing for delete command
- [x] T032 [US4] Validate that task exists before deleting
- [x] T033 [US4] Confirm deletion and remove task from storage
- [x] T034 [US4] Test deleting tasks and verifying they no longer appear in list

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Enable users to mark tasks as complete or incomplete to track progress

**Independent Test**: Can be fully tested by adding a task, toggling its completion status with the `complete` command, and verifying the status changes when listing tasks.

### Implementation for User Story 5

- [x] T035 [P] [US5] Implement complete command handler in src/cli/command_handler.py
- [x] T036 [US5] Implement toggle_task_completion method in src/services/task_service.py
- [x] T037 [US5] Handle ID parsing for complete command
- [x] T038 [US5] Validate that task exists before toggling completion status
- [x] T039 [US5] Implement toggle logic (switch between complete/incomplete)
- [x] T040 [US5] Test toggling completion status and verifying changes in list

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Additional Commands & Error Handling

**Goal**: Implement remaining required commands and comprehensive error handling

- [x] T041 [P] Implement help command to display available commands
- [x] T042 Implement exit command to terminate the application cleanly
- [x] T043 Handle unknown commands with helpful error messages
- [x] T044 Implement case-insensitive command recognition
- [x] T045 Add comprehensive error handling for all commands
- [x] T046 Validate all functional requirements from specification

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T047 [P] Documentation updates in README.md
- [x] T048 Code cleanup and refactoring
- [x] T049 Performance validation (ensure sub-second execution)
- [x] T050 [P] Additional error handling validation
- [x] T051 Security hardening (input validation)
- [x] T052 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Implement add command handler in src/cli/command_handler.py"
Task: "Implement add_task method in src/services/task_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence