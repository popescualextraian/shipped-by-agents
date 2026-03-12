# REST API Testing Skill — Usage Guide

## Prerequisites

### 1. Python 3

Python 3.8+ is required to run `test_manager.py`.

```bash
python --version
# Python 3.8.0 or higher
```

**Install:**
- Windows: https://www.python.org/downloads/ or `winget install Python.Python.3.12`
- macOS: `brew install python3`
- Linux: `sudo apt install python3` (Ubuntu/Debian) or `sudo dnf install python3` (Fedora)

### 2. Hurl CLI

Hurl is the HTTP testing tool that runs `.hurl` test files.

```bash
hurl --version
# hurl 6.0.0 or higher
```

**Install:**

| Platform | Command |
|----------|---------|
| Windows (winget) | `winget install Orange.Hurl` |
| Windows (scoop) | `scoop install hurl` |
| Windows (choco) | `choco install hurl` |
| Windows (manual) | Download from https://github.com/Orange-OpenSource/hurl/releases |
| macOS | `brew install hurl` |
| Linux (Debian/Ubuntu) | `curl -LO https://github.com/Orange-OpenSource/hurl/releases/download/6.0.0/hurl_6.0.0_amd64.deb && sudo dpkg -i hurl_6.0.0_amd64.deb` |
| Linux (Arch) | `pacman -S hurl` |
| npm | `npm install -g @anthropic-ai/hurl` |
| Docker | `docker pull ghcr.io/orange-opensource/hurl:latest` |

Full installation guide: https://hurl.dev/docs/installation.html

### 3. Verify setup

```bash
python --version   # 3.8+
hurl --version     # 6.0.0+
```

---

## Getting Started

### Initialize a test suite

```bash
python .claude/skills/rest-api-testing/code/test_manager.py init https://your-api.com
```

This creates:
```
integration-tests/
├── smoke/
├── crud/
├── validation/
└── inventory.json
```

### Run the demo (JSONPlaceholder)

If you already have the demo tests set up:

```bash
# Run all tests
python .claude/skills/rest-api-testing/code/test_manager.py run-all

# Run just smoke tests
python .claude/skills/rest-api-testing/code/test_manager.py run-suite smoke

# Run a specific test
python .claude/skills/rest-api-testing/code/test_manager.py run get-posts

# List all tests
python .claude/skills/rest-api-testing/code/test_manager.py list
```

---

## Example Prompts

Use these prompts with Claude Code (or any AI coding agent) to interact with the skill. All examples target the JSONPlaceholder demo API (`https://jsonplaceholder.typicode.com`).

### Setting up the demo

> "Set up integration tests for https://jsonplaceholder.typicode.com. Create smoke tests for GET /posts and GET /users."

> "Initialize a test suite for JSONPlaceholder and create a full set of smoke, CRUD, and validation tests."

### Creating tests for JSONPlaceholder endpoints

> "Create a test that verifies POST /posts on JSONPlaceholder returns 201 and includes the new post's ID in the response."

> "Add a validation test that checks GET /posts/99999 returns 404 on JSONPlaceholder."

> "Create CRUD tests for JSONPlaceholder's /users endpoint — test create, read, update, and delete."

> "Add a smoke test that verifies GET /todos on JSONPlaceholder returns a JSON array with 200 items."

> "Create a test for GET /posts/1/comments — it should return 5 comments with valid email fields."

> "Add a test that verifies GET /albums returns 100 albums, each with a userId and title."

### Running and checking tests

> "Run all integration tests against JSONPlaceholder."

> "Run just the smoke suite."

> "Run the create-post and update-post tests to verify the /posts CRUD operations."

> "List all tests we have for JSONPlaceholder."

> "Show me only the GET tests."

### After test failures

> "Run all JSONPlaceholder tests. If any fail, show me what went wrong."

> "The create-post test is failing — can you analyze why and suggest a fix?"

> "Run the smoke suite and help me fix any failures."

### Managing the test inventory

> "Add a new test called get-comments to the smoke suite for GET /comments on JSONPlaceholder."

> "Remove the get-invalid-post test, we don't need it anymore."

> "What tests do we have in the crud suite?"

### Exploring JSONPlaceholder further

> "What other endpoints does JSONPlaceholder have? Create smoke tests for any we haven't covered yet."

> "Add tests for the nested routes — GET /posts/1/comments and GET /users/1/albums."

> "Create validation tests for edge cases: empty POST body, invalid user ID, non-existent album."

---

## Troubleshooting

### Hurl not found

```
Error: Hurl CLI not found. Install from https://hurl.dev
```

Install Hurl using one of the methods above, then verify with `hurl --version`.

### No inventory found

```
Error: No inventory.json found
```

Run `test_manager.py init <base_url>` first to initialize the test directory.

### Git Bash path mangling (Windows)

If endpoint paths like `/posts` get converted to `C:/Program Files/Git/posts`, prefix your command:

```bash
MSYS_NO_PATHCONV=1 python .claude/skills/rest-api-testing/code/test_manager.py add ...
```

This only affects Git Bash. PowerShell and cmd.exe work fine.

### Test timeout

If tests hang, the target API may be unreachable. Verify with:

```bash
curl -s -o /dev/null -w "%{http_code}" https://your-api.com/health
```
