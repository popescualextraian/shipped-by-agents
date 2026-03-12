---
name: rest-api-testing
description: Use when creating, managing, or running REST API integration tests, or when the user asks to test HTTP endpoints, verify API behavior, or set up integration test suites
---

# REST API Testing

## Overview

Create, manage, and run REST API integration tests using Hurl (declarative HTTP test files) and a Python CLI for inventory management. Tests are `.hurl` files organized by suite in `integration-tests/`.

## Prerequisites

- **Hurl CLI** installed (`hurl --version`). Install: https://hurl.dev
- **Python 3** available

## Quick Reference

| Action | Command |
|--------|---------|
| Initialize | `python <skill>/code/test_manager.py init <base_url>` |
| Add test to inventory | `python <skill>/code/test_manager.py add <name> <suite> <method> <endpoint> "<description>"` |
| Remove test | `python <skill>/code/test_manager.py remove <name>` |
| List all tests | `python <skill>/code/test_manager.py list` |
| List by suite | `python <skill>/code/test_manager.py list --suite smoke` |
| List by method | `python <skill>/code/test_manager.py list --method GET` |
| Run all tests | `python <skill>/code/test_manager.py run-all` |
| Run a suite | `python <skill>/code/test_manager.py run-suite smoke` |
| Run specific tests | `python <skill>/code/test_manager.py run get-posts get-users` |

Replace `<skill>` with the path to `.claude/skills/rest-api-testing`.

## Workflow

### First-time setup

1. Check prerequisites: `hurl --version` and `python3 --version`
2. Run `test_manager.py init <base_url>` to create `integration-tests/` with inventory and default suite folders (smoke, crud, validation)

### Creating tests

1. Ask the user which endpoints or scenarios to test
2. Pick the matching template from `templates/` (get.hurl, post.hurl, put.hurl, delete.hurl)
3. Customize the template: set endpoint, assertions, request body as needed
4. Write the `.hurl` file to `integration-tests/<suite>/<test-name>.hurl`
5. Register in inventory: `test_manager.py add <name> <suite> <method> <endpoint> "<description>"`
6. Run the new test to verify: `test_manager.py run <name>`

### Running tests

- **All tests:** `test_manager.py run-all`
- **One suite:** `test_manager.py run-suite <suite>`
- **Specific tests:** `test_manager.py run <name1> <name2>` (by inventory name or file path)

**Output rule:** When running a single test, do not summarize or reformat successful output — the CLI output speaks for itself. Only add commentary when tests fail or the user asks a question.

### Handling failures

When tests fail:
1. Show the failure output to the user (status code, expected vs actual, response body)
2. Ask: "Would you like me to analyze the failure and suggest a fix?"
3. If yes: read relevant project source files and suggest a fix
4. If no: move on

## Hurl File Format

```hurl
# Test: get-posts
# Suite: smoke
# Endpoint: GET /posts

GET {{base_url}}/posts
HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
jsonpath "$" count > 0
```

- `{{base_url}}` is injected at runtime by test_manager.py from inventory
- Comments at the top are metadata (test name, suite, endpoint)
- `HTTP 200` is the expected status code
- `[Asserts]` section contains explicit assertions

## Common Assertions

| Assertion | Example |
|-----------|---------|
| Status code | `HTTP 200` |
| Header value | `header "Content-Type" contains "application/json"` |
| JSON field exists | `jsonpath "$.id" exists` |
| JSON field value | `jsonpath "$.title" == "foo"` |
| Array count | `jsonpath "$" count == 10` |
| Array not empty | `jsonpath "$" count > 0` |
| Regex match | `jsonpath "$.email" matches /\S+@\S+/` |
| Field is string | `jsonpath "$.name" isString` |
| Field is integer | `jsonpath "$.id" isInteger` |

## Test Organization

```
integration-tests/
├── smoke/          # Quick health checks (GET endpoints, basic connectivity)
├── crud/           # Full CRUD operations (create, read, update, delete)
├── validation/     # Error cases, edge cases, invalid inputs
└── inventory.json  # Test registry (managed by test_manager.py)
```

Create new suite folders as needed for your project's testing needs.

## Windows / Git Bash Note

Git Bash auto-converts arguments starting with `/` to Windows paths (e.g., `/posts` becomes `C:/Program Files/Git/posts`). When calling `test_manager.py add` with endpoint arguments, prefix the command:

```bash
MSYS_NO_PATHCONV=1 python <skill>/code/test_manager.py add get-posts smoke GET /posts "description"
```

This is only needed in Git Bash. PowerShell, cmd.exe, and programmatic calls are unaffected.
