# User Stories Skill — Usage Guide

## Prerequisites

### 1. Python 3

Python 3.8+ is required to run `ref_manager.py`.

```bash
python --version
# Python 3.8.0 or higher
```

**Install:**
- Windows: https://www.python.org/downloads/ or `winget install Python.Python.3.12`
- macOS: `brew install python3`
- Linux: `sudo apt install python3` (Ubuntu/Debian) or `sudo dnf install python3` (Fedora)

### 2. Atlassian MCP (Optional)

The Atlassian MCP enables Confluence page reads and JIRA push/update. Without it, all local operations work — you just can't read Confluence or push to JIRA directly.

**Recommended: `sooperset/mcp-atlassian`**

This server supports both JIRA and Confluence with local API token auth.

Add to `.mcp.json` at your project root:

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://your-org.atlassian.net",
        "JIRA_USERNAME": "your-email@example.com",
        "JIRA_API_TOKEN": "your-api-token",
        "CONFLUENCE_URL": "https://your-org.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "your-email@example.com",
        "CONFLUENCE_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

**Getting an API token:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Copy the token and paste it into the config above

**Alternative: Atlassian Rovo MCP Server**

Atlassian's official Rovo MCP server is another option. See the [Atlassian Rovo docs](https://developer.atlassian.com/cloud/rovo/) for setup instructions. The skill works with any MCP server that exposes `mcp__atlassian` tools.

### 3. Verify setup

```bash
python --version   # 3.8+
```

If using MCP, verify tools are available by asking Claude: "What Atlassian MCP tools are available?"

---

## Getting Started

### Initialize a project

```bash
python repository/solutions/user-stories/code/ref_manager.py init PROJ --jira-url https://your-org.atlassian.net
```

This creates:
```
user-stories/
├── references.json
├── refs/
└── stories/
```

### Add references

```bash
# Local markdown file
python repository/solutions/user-stories/code/ref_manager.py add local-md docs/requirements.md "Requirements Doc" "Main product requirements"

# Confluence page (works best with MCP configured)
python repository/solutions/user-stories/code/ref_manager.py add confluence "https://org.atlassian.net/wiki/spaces/PROJ/pages/123" "Design Spec" "UI design specification"
```

### List references

```bash
python repository/solutions/user-stories/code/ref_manager.py list
```

---

## Example Prompts

Use these prompts with Claude Code to interact with the skill.

### Setting up

> "Initialize user stories for project MYPROJ with JIRA at https://myorg.atlassian.net"

> "Add the requirements doc at docs/product-requirements.md as a reference for user stories"

> "Add this Confluence page as a reference: https://myorg.atlassian.net/wiki/spaces/PROJ/pages/12345"

### Creating stories

> "Create a user story for the login feature based on our references"

> "Draft a story about the search functionality. Use the design spec reference for context."

> "Create a high-priority story for the payment integration, 8 story points, labels: payments, backend"

### Managing references

> "List all references for user stories"

> "Download all Confluence references for offline use"

> "Remove reference ref-003"

### Updating stories

> "Update PROJ-42 — change the acceptance criteria to include error handling"

> "Fetch PROJ-15 from JIRA and update the technical notes with the new API design"

### Listing drafts

> "Show me all local story drafts"

> "What stories have we drafted so far?"

---

## Troubleshooting

### No references.json found

```
Error: No references.json found
```

Run `ref_manager.py init <project-key>` first to initialize the data directory.

### MCP not available

If you see messages about MCP not being configured:
1. Add the Atlassian MCP config to `.mcp.json` (see Prerequisites above)
2. Restart Claude Code to pick up the new MCP configuration
3. Verify with: "What Atlassian MCP tools are available?"

All local operations (init, add local refs, list, render stories) work without MCP.

### Git Bash path mangling (Windows)

If URLs get converted to Windows paths, prefix your command:

```bash
MSYS_NO_PATHCONV=1 python repository/solutions/user-stories/code/ref_manager.py add ...
```

This only affects Git Bash. PowerShell and cmd.exe work fine.

### Story rendering issues

If `render-story` fails, check that your JSON is valid:

```bash
echo '{"title":"test"}' | python -m json.tool
```

All fields except `title`, `project_key`, `role`, `goal`, `benefit`, and `acceptance_criteria` are optional.
