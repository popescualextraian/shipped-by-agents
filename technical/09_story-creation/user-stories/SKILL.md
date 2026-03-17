---
name: user-stories
description: Use when creating, managing, or pushing user stories to JIRA, gathering context from local files or Confluence, or when the user asks to draft stories from requirements
---

# User Stories

## Overview

Create, manage, and push user stories to JIRA. Gather context from local markdown files and Confluence pages, draft stories by filling in a template, and optionally push them via the Atlassian MCP. Works in local-only mode when MCP is not configured.

The skill is **fully template-driven**. Each project defines its own template at `<skill>/templates/user-story.template.md`. The template contains:
- An HTML comment block (`<!-- ... -->`) with all project configuration — project key, default epic, JIRA field mappings, custom fields, issue type, and any other project-specific instructions
- The story body structure with `{{placeholder}}` markers and `{{#section}}...{{/section}}` optional blocks

**The agent reads the template's configuration block and follows it.** No field names, JIRA mappings, or defaults are hardcoded in this skill. If the template changes, the agent adapts.

## Prerequisites

- **Python 3** available
- **Atlassian MCP** (optional) — enables Confluence reads and JIRA push/update

## MCP Detection

Check for Atlassian MCP availability by looking for tools with the `mcp__atlassian` prefix. If available, Confluence and JIRA operations work fully. If not, all local operations still work — JIRA/Confluence ops print setup guidance instead.

## Quick Reference

| Action | Command / Tool |
|--------|---------------|
| Initialize | `python <skill>/code/ref_manager.py init <project-key> [--jira-url <url>]` |
| Add reference | `python <skill>/code/ref_manager.py add <type> <path\|url> "<title>" ["<desc>"]` |
| Remove reference | `python <skill>/code/ref_manager.py remove <id>` |
| List references | `python <skill>/code/ref_manager.py list [--type local-md\|confluence]` |
| Get reference | `python <skill>/code/ref_manager.py get-ref <id>` |
| Mark downloaded | `python <skill>/code/ref_manager.py mark-downloaded <id> <local-path>` |
| List story drafts | `python <skill>/code/ref_manager.py list-stories` |
| Create story | Read template → fill in → Write tool to `user-stories/stories/` |

Replace `<skill>` with the path to `.claude/skills/user-stories`.

## Template System

The template lives at `<skill>/templates/user-story.template.md`.

**Structure:**
1. **Configuration block** — an HTML comment at the top of the template containing project defaults, JIRA field mappings, custom fields, and any special instructions. Written in plain English — no rigid schema required.
2. **Story body** — the markdown structure with `{{placeholder}}` markers for simple fields and `{{#section}}...{{/section}}` blocks for optional sections and lists.

**How it works:**
1. Read the template file with the Read tool
2. Parse the configuration block — understand project defaults, field mappings, custom fields
3. Apply defaults from the configuration (e.g., default epic, project key) unless the user overrides them
4. Fill in each placeholder with content gathered from references and the user
5. Remove optional blocks the user doesn't need (delete the entire `{{#...}}...{{/...}}` block)
6. Write the filled markdown to `user-stories/stories/<slug>.md` using the Write tool

**The agent never hardcodes field names, JIRA mappings, or defaults.** Everything comes from the template's configuration block.

**Creating a template for a new project:** Copy an existing template, update the configuration block with the new project's details (project key, epic, JIRA URL, custom fields), and adjust the body sections as needed.

## Operations

### `init <project-key> [--jira-url <url>]`

First-time setup. Creates the `user-stories/` data directory with `references.json`, `refs/`, and `stories/` subfolders.

1. Run `ref_manager.py init <project-key> --jira-url <url>`
2. Confirm to user what was created

### `add-ref <path-or-url>`

Add a reference document that will inform story creation.

1. **Detect type:** If the location contains `confluence` or `atlassian` in the URL → `confluence`. Otherwise → `local-md`.
2. **Extract title:**
   - Local file: read the file, use the first H1 heading
   - Confluence URL with MCP: use MCP to fetch the page title
   - Fallback: ask the user for a title
3. **Ask for description** if not obvious from context
4. Run `ref_manager.py add <type> <path-or-url> "<title>" "<description>"`

### `list-refs`

Show the reference index.

1. Run `ref_manager.py list`
2. Display the output — no reformatting needed

### `download-refs`

Download Confluence references for offline use. **Requires Atlassian MCP.**

1. Run `ref_manager.py list --type confluence` to find un-downloaded refs
2. For each Confluence reference:
   a. Fetch page content via MCP (`mcp__atlassian` Confluence tools)
   b. Write the content as markdown to `user-stories/refs/<slug>.md`
   c. Run `ref_manager.py mark-downloaded <id> refs/<slug>.md`
3. Show updated reference list
4. **If no MCP:** Tell the user to configure the Atlassian MCP or manually download pages and add them as `local-md` refs.

### `create`

Draft a new user story by filling in the template.

1. **Read the template** using the Read tool — parse both the configuration block and the body structure
2. Run `ref_manager.py list` — show references to user
3. Ask what the story should accomplish (if not clear from context)
4. **Gather context — read and analyse all available sources:**
   - **References:** Read every relevant reference. For `local-md` refs, use the Read tool on the file path. For `confluence` refs with MCP, fetch via MCP. Without MCP, tell the user to run `download-refs` first or provide local files.
   - **Local codebase:** If the story touches existing code, explore the repo (Glob, Grep, Read) to understand current implementation, file structure, naming conventions, and related modules. Use what you find to write accurate current-situation descriptions, realistic subtasks, and concrete acceptance criteria.
   - **Synthesise:** Extract technical details, constraints, terminology, and domain context from all sources. The story content should reflect what the references and code actually say — not generic placeholders.
5. **Fill in the template** using defaults from the configuration block and the context gathered above:
   - Apply default values (epic, project key, etc.) from the configuration
   - Replace each `{{placeholder}}` with the appropriate content
   - For optional `{{#section}}...{{/section}}` blocks: keep and fill if relevant, delete entirely if not
   - For list blocks (`{{#items}}...{{/items}}`): expand one line per item
6. Show the filled draft to the user and ask for approval
7. **Ask the user:** "Push to JIRA or save locally?"
   - **Save locally:** Write the filled markdown to `user-stories/stories/<slug>.md` using the Write tool. Confirm the path.
   - **Push to JIRA (requires MCP):** See [JIRA Push](#jira-push) below, then also save a local copy.
   - **No MCP available but user wants JIRA:** Save locally and provide manual copy instructions.

### `update <issue-key>`

Update an existing JIRA story. **Requires Atlassian MCP for JIRA interaction.**

1. Fetch current story from JIRA via MCP (`mcp__atlassian` get_issue or search)
2. Show current content to user, ask what to change
3. Read the template again if needed to understand the structure
4. **Gather context if new information is needed:**
   - Read relevant references (same as `create` step 4)
   - Explore the local codebase if changes touch existing code — understand what has changed since the story was written
   - Use gathered context to write accurate, specific updates — not vague rewrites
5. Produce the updated markdown following the template structure
6. Show diff between old and new content, ask for approval
7. **With MCP:** Push update via `mcp__atlassian` update_issue tool (see [JIRA Push](#jira-push))
8. **Without MCP:** Save updated draft locally, tell user to update JIRA manually
9. Write updated markdown to `user-stories/stories/<issue-key>.md`

## JIRA Push

When the user chooses to push to JIRA, read the template's configuration block to determine how markdown fields map to JIRA fields. Use that mapping to extract values from the filled story and pass them to the JIRA create/update MCP tools.

- **Field mapping:** The configuration block defines which markdown field maps to which JIRA field (standard or custom). Follow it exactly.
- **Custom fields:** The configuration block lists any custom field IDs and how to populate them. Use `additional_fields` in the MCP call for custom fields and epic links.
- **Subtasks:** If the configuration block describes subtask handling, follow those instructions (typically: create each subtask item as a separate Sub-task issue linked to the parent).

After push, save a local copy to `user-stories/stories/<issue-key>.md`.

## Graceful Degradation

| Operation | With MCP | Without MCP |
|-----------|----------|-------------|
| init | Full | Full |
| add-ref (local) | Full | Full |
| add-ref (Confluence) | Fetches title via MCP | Ask user for title |
| list-refs | Full | Full |
| download-refs | Fetches + saves locally | Prints setup guidance |
| create | Template → fill → save / push to JIRA | Template → fill → save locally |
| update | Fetches + updates JIRA | Local draft only |

## Windows / Git Bash Note

Git Bash auto-converts arguments starting with `/` to Windows paths. When calling `ref_manager.py` with URL arguments, prefix the command:

```bash
MSYS_NO_PATHCONV=1 python <skill>/code/ref_manager.py add confluence "https://..." "Title"
```

This is only needed in Git Bash. PowerShell, cmd.exe, and programmatic calls are unaffected.
