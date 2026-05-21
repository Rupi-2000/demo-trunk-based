# Trunk-Based Development Demo Repository

## Purpose

This repository demonstrates Trunk-Based Development using a small Python FastAPI task management application.

## Application Scope

Initial version `v1.0.0` contains:

- task creation through REST API
- task completion through REST API
- listing all tasks
- listing open tasks
- SQLite database persistence
- version output
- automated tests
- CI workflow

Short-lived branches for priority, due dates, users, assignment, task status, and bugfixes will be added later.

## Branching Strategy

Trunk-Based Development keeps development close to `main`. Changes should be small, validated quickly, and merged frequently. Long-running feature branches are avoided.

## Branch Overview

Current initial setup:

- `main`

Planned later short-lived branches:

- `short/add-task-priority`
- `short/add-due-date`
- `short/add-user-service`
- `short/add-task-assignment`
- `short/add-task-status`
- `short/fix-task-completion`

## Integration Flow

The planned integration path is:

```text
short-lived branch -> CI check -> main -> delete branch
```

The initial version starts with only `main` and the `v1.0.0` tag.

## CI Setup

The CI workflow runs on `push` and `pull_request`.

It installs Python dependencies and runs the test suite with `python -m pytest`.

## Tags / Releases

- `v1.0.0`: initial base application

