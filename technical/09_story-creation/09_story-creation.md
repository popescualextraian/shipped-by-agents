# Chapter 9: Automating User Story Creation

## Beyond Code

You've learned how to build skills (Chapter 7) and orchestrate multi-agent workflows (Chapter 8). Every example so far focused on writing code — testing, implementation, code review. But coding is only part of the development lifecycle.

Think about what else happens in a sprint:

- Writing user stories and acceptance criteria
- Gathering requirements from design specs, Confluence pages, meeting notes
- Estimating effort, linking to epics, filling out JIRA fields
- Reviewing and refining stories before they enter a sprint

These tasks are repetitive, template-driven, and context-heavy — exactly the kind of work an AI agent handles well. In this chapter, you'll see how to apply skill-building techniques to **user story creation**: a non-coding task that every development team does, and few do efficiently.

We'll walk through the design decisions behind a complete skill, explore how to bring external data into the agent's context, and then strip it all down to the simplest version that still works. The full skill implementation lives in this chapter's `user-stories/` folder; the minimal version lives in `user-stories-simple/`.

---

## The Data Advantage You Already Have

Before building anything new, consider what the agent already knows.

If you followed the earlier chapters, your project has instruction files — `CLAUDE.md`, `AGENTS.md`, maybe scoped `.claude/` configs. These files describe your project's architecture, conventions, folder structure, and team practices. They're not just instructions for the agent — they *are* your project's living documentation.

When you ask the agent to create a user story, it already has:

- **Project architecture** — from `CLAUDE.md` and instruction files
- **Code structure** — it can explore the repo with Glob, Grep, and Read
- **Naming conventions and patterns** — from the code itself
- **Public knowledge** — the agent can search the web for library docs, API references, and best practices

That's a significant head start. For many simple stories, this is enough — the agent can draft a story based on what it already sees in the codebase.

But enterprise work usually needs more:

| Source | Example | How to access |
|--------|---------|---------------|
| Local docs | Requirements markdown, design specs, meeting notes | Read tool — already available |
| Confluence pages | Architecture decisions, product specs, team agreements | Needs an external connector |
| JIRA | Existing stories, epics, sprint context | Needs an external connector |
| Templates | Company story format, required fields, custom JIRA fields | A file the skill provides |

The gap is clear: **local files and code are accessible out of the box, but Confluence and JIRA need a bridge.** That bridge is an MCP server — a lightweight plugin that gives the agent new tools for external systems.

---

## MCP in 30 Seconds

**Model Context Protocol (MCP)** is a standard that lets AI agents talk to external systems through a uniform interface. An MCP server exposes tools — like "search Confluence" or "create JIRA issue" — that the agent can call the same way it calls built-in tools like Read or Grep.

For this chapter, you only need to know three things:

1. **An MCP server is a plugin.** You configure it in `.mcp.json` at your project root. The agent discovers the tools automatically.
2. **Tools have a prefix.** Atlassian MCP tools show up as `mcp__mcp-atlassian__jira_*` and `mcp__mcp-atlassian__confluence_*`. The skill checks for this prefix to know if the connector is available.
3. **Graceful degradation.** If the MCP server isn't configured, the skill still works — you just can't read Confluence or push to JIRA directly. Everything local still functions.

We'll cover MCP architecture, how to build your own servers, and advanced integration patterns in the next chapter. For now, think of it as: **the agent gets new tools, and the skill decides when to use them.**

---

## Approaching the Problem

Regardless of how you implement it, you need three things to automate story creation:

1. **Inputs** — the codebase (already available), local docs, Confluence pages, and the user's direction
2. **A template** — the story format your team uses, with JIRA field mappings and defaults
3. **Connectivity** — a way to reach JIRA and Confluence (the Atlassian MCP server)

The question is: **how much infrastructure do you build around these three things?** We'll start with a full skill — the academic example — then strip it down to the bare minimum.

---

## The Full Skill — An Academic Example

The complete skill lives in `user-stories/` alongside this chapter. It has a SKILL.md, a Python CLI for reference management, templates, and detailed agent instructions. We'll walk through the design decisions and key components — not every line of code, but everything you need to understand the architecture.

### How It Fits Together

```mermaid
graph TB
    subgraph Inputs
        A[Project Codebase<br/>CLAUDE.md, source files]
        B[Local References<br/>markdown, design docs]
        C[Confluence Pages<br/>via MCP]
        D[User Input<br/>clarifications, priorities]
    end

    subgraph Skill["User Story Skill"]
        E[Reference Manager<br/>ref_manager.py]
        F[Story Template<br/>user-story.template.md]
        G[SKILL.md<br/>agent instructions]
    end

    subgraph Outputs
        H[Local Story Draft<br/>user-stories/stories/]
        I[JIRA Issue<br/>via MCP]
    end

    A --> G
    B --> E
    C -->|MCP read| E
    D --> G
    E -->|tracked refs| G
    F -->|structure + config| G
    G --> H
    G -->|MCP push| I

    style A fill:#0A2540,color:#fff
    style B fill:#0A2540,color:#fff
    style C fill:#00BFA5,color:#fff
    style D fill:#0A2540,color:#fff
    style E fill:#f7f9fb,color:#0A2540,stroke:#e0e6ed
    style F fill:#f7f9fb,color:#0A2540,stroke:#e0e6ed
    style G fill:#f7f9fb,color:#0A2540,stroke:#e0e6ed
    style H fill:#0A2540,color:#fff
    style I fill:#00BFA5,color:#fff
```

### Key Design Decisions

**Template-driven, not hardcoded.** The skill doesn't know anything about your project's JIRA setup. Field mappings, custom field IDs, default epics — all of it lives in the template's configuration block. Change the template, and the skill adapts. One skill serves multiple projects.

**Reference tracking with a CLI.** `ref_manager.py` (~430 lines of Python) manages a persistent `references.json` index. It handles init, add, remove, list, and tracks download state for Confluence pages. The agent calls it through Bash.

**Graceful degradation.** Every operation has a fallback. No MCP? Stories are created from local files and saved as markdown. No Confluence? Add the page manually as a local file. The skill never blocks on missing infrastructure.

### The Template

The template has two parts: a **configuration block** (an HTML comment the agent reads) and a **story body** with placeholders.

**Configuration block** — tells the agent how to map fields to JIRA:

```html
<!--
=== Template Configuration ===

Project: CYD
JIRA URL: https://your-org.atlassian.net/jira
Default epic: CYD-116

JIRA field mapping (markdown field → JIRA field):
  - "# title" heading        → summary
  - Body below metadata       → description
  - **Priority:** value       → priority
  - **Labels:** value         → labels (comma-separated → array)
  - **Story Points:** value   → story_points
  - **Epic:** value           → epic_link

Custom fields:
  - Epic Link: customfield_10001
  - AC Checklist: customfield_11100

=== End Configuration ===
-->
```

This is plain English, not a rigid schema. The agent reads it, understands the mappings, and applies them. If your project uses different custom fields or a different JIRA setup, you update this block — not the skill code.

**Story body** — uses `{{placeholder}}` markers and `{{#section}}...{{/section}}` optional blocks:

```markdown
# {{title}}

**Project:** {{project_key}}
**Epic:** {{epic_link}}
**Priority:** {{priority}}

---

## Current Situation
{{current_situation}}

## Desired Situation
{{desired_situation}}

{{#acceptance_criteria}}
## Acceptance Criteria
{{#acceptance_criteria_items}}
- [ ] {{item}}
{{/acceptance_criteria_items}}
{{/acceptance_criteria}}
```

Optional sections are wrapped in `{{#section}}...{{/section}}` blocks. If the story doesn't need a section, the agent removes the entire block.

### The SKILL.md

The SKILL.md tells the agent how to handle each operation step by step:

```
1. Read the template — parse config block and body structure
2. List references — show to user
3. Gather context — read every reference, explore the codebase
4. Synthesize — extract technical details, constraints, terminology
5. Fill the template — apply defaults, replace placeholders
6. Show draft to user — ask for approval
7. Save or push — local markdown, JIRA, or both
```

The key is step 3: **read every reference**. The agent reads all registered references, explores relevant code, and synthesizes everything before writing. This produces stories that reflect your actual project — not generic filler.

### Example Prompts

```
"Initialize user stories for project MYPROJ with JIRA at https://myorg.atlassian.net"

"Add the requirements doc at docs/product-requirements.md as a reference"

"Create a high-priority story for the payment integration, 8 story points"

"Download all Confluence references for offline use"

"Update PROJ-42 — add error handling to acceptance criteria"
```

---

## Simplicity Is Power — The KISS Version

The full skill works. It's well-structured, it follows every best practice from Chapter 7, and it's a solid academic example of skill design. But do you actually need all of it?

Let's look at what the skill has and ask a brutal question for each piece:

| Component | What it does | Do you need it? |
|-----------|-------------|-----------------|
| `SKILL.md` | Agent instructions | A scoped `CLAUDE.md` does the same thing |
| `ref_manager.py` (~430 lines) | Tracks references in JSON | A bullet list in CLAUDE.md works just as well |
| `references.json` | Persistent reference index | The bullet list *is* persistent — it's a file |
| Slash command invocation | `/user-stories` trigger | You can just say "create a user story" |
| Template | Story structure + JIRA config | Yes — you need this either way |

The Python CLI is the main overhead. It manages references — but you could replace it with a section in your CLAUDE.md that says "read these files before creating a story" followed by a list. The agent already knows how to read files, search Confluence via MCP, and explore the codebase. You don't need a CLI to tell it where to look.

**The minimal version is three files:**

```
user-stories/
├── CLAUDE.md          # rules, references, JIRA config, MCP usage
├── template.md        # story template (same as the full skill)
└── stories/           # output folder
```

No Python. No JSON. No CLI. The `CLAUDE.md` carries all the instructions — the agent reads it automatically because it's a scoped instruction file (Chapter 6). The template stays exactly the same. Stories go into `stories/`.

### The CLAUDE.md

This single file replaces the SKILL.md, the reference manager, and the references.json. It tells the agent everything: how to create stories, where to find references, how to use MCP, and how to push to JIRA.

Here's an example (also available at [`user-stories-simple/CLAUDE.md`](./user-stories-simple/CLAUDE.md)):

```markdown
# User Story Creation

## How to create a story

1. Read `template.md` — understand the config block and the body structure
2. Read all references listed below
3. Explore the codebase for relevant context (Glob, Grep, Read)
4. If Atlassian MCP is available (tools with `mcp__mcp-atlassian__` prefix),
   fetch any Confluence references listed below
5. Fill in the template — apply defaults from the config block,
   replace placeholders with synthesized content
6. Show the draft to the user, ask for approval
7. Save to `stories/<slug>.md`
8. Ask: "Push to JIRA or keep as local draft?"
   - If JIRA push: use MCP tools to create the issue,
     map fields per the template config block
   - If no MCP: save locally and tell the user

## References

Read these before creating any story:

- `docs/requirements.md` — Product requirements
- `docs/api-design.md` — API design specification
- Confluence: https://org.atlassian.net/wiki/spaces/PROJ/pages/123 — Architecture decisions

## Project defaults

- Project key: PROJ
- Default epic: PROJ-42
- JIRA URL: https://your-org.atlassian.net
```

To add a reference, you add a line to the list. To change defaults, you edit the file. That's the entire management workflow.

### Why This Is Enough

The agent doesn't need a Python CLI to know which files to read — you can just tell it in plain English. It doesn't need `references.json` to track references — a bullet list in CLAUDE.md survives across sessions just as well. And since CLAUDE.md is a scoped instruction file, the agent picks it up automatically when the folder is in scope.

The MCP integration works identically. The CLAUDE.md tells the agent to check for Atlassian MCP tools and use them if available. The template's configuration block tells it how to map fields to JIRA. Nothing about the MCP workflow requires a Python CLI or a formal skill.

**Start here.** If you later find yourself wanting slash command invocation, programmatic reference management, or CI integration — the full skill is in `user-stories/` and the upgrade path is smooth. The template and MCP config stay the same. But most teams never need to upgrade. The simple version just works.

### Full Skill vs. KISS — When to Choose What

| Situation | Use the simple approach | Use the full skill |
|-----------|------------------------|-------------------|
| Solo developer or small team | Yes | Overkill |
| Handful of stable references | Yes | Overkill |
| Team wants slash command invocation | No | Yes |
| Dozens of references that change often | No | Yes |
| CI/CD integration for story generation | No | Yes |
| You want to learn skill design patterns | Both — build the full one, then simplify |

---

## Skill-Building Best Practices — A Recap

This skill applies every pattern from Chapter 7. Here's a quick checklist you can use when building any skill:

### Structure

| Component | Purpose | This skill's example |
|-----------|---------|---------------------|
| `SKILL.md` | Agent instructions — the brain | Step-by-step operations: init, add-ref, create, update |
| Templates | Output structure + project config | `user-story.template.md` with config block and placeholders |
| Supporting code | Persistent state, complex logic | `ref_manager.py` — CLI for reference tracking |
| Data directory | Runtime artifacts, user content | `user-stories/` with `references.json`, `refs/`, `stories/` |

### Key Patterns

**Separate configuration from logic.** The template's HTML comment block holds all project-specific details — JIRA field mappings, custom field IDs, default values. The SKILL.md instructions are generic. To use this skill on a different project, you copy the template and update the configuration block. Nothing else changes.

**Use plain English for agent instructions.** The configuration block isn't YAML or JSON — it's structured English. The agent parses it naturally. This makes templates easy for anyone on the team to read and edit, even if they've never built a skill before.

**Persistent state through files, not memory.** References live in `references.json`, not in the agent's conversation context. This means references survive across sessions and are visible to the whole team through version control.

**CLI wrapping for complex operations.** The reference manager is a Python script the agent calls through Bash. This keeps complex logic (ID generation, JSON manipulation, file management) in testable code rather than in prompt instructions. The SKILL.md tells the agent *when* to call each command — the script handles the *how*.

**Graceful degradation by design.** Every operation in the skill has a fallback path. The SKILL.md explicitly documents what works with MCP and what works without it. The agent never hits a dead end — it always has something useful to offer.

**Templates over freeform generation.** Without a template, the agent would generate stories in a different format every time. The template enforces consistency: every story has the same sections, the same metadata fields, the same structure. This matters when stories go into JIRA — the field mappings need to be predictable.

---

## Configuring the Atlassian MCP

The user story skill works locally without any MCP setup. But to read Confluence pages and push stories to JIRA, you need the Atlassian MCP server. Here's how to set it up.

### 1. Get a Token

There are two authentication options depending on your Atlassian setup.

**Option A: Atlassian Cloud (API token + username)**

For Atlassian Cloud instances (e.g., `your-org.atlassian.net`):

1. Go to [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **Create API token**
3. Give it a name (e.g., "Claude Code MCP")
4. Copy the token — you won't see it again

You'll use your email address as the username and this token for both JIRA and Confluence.

**Option B: Enterprise / Data Center (personal access token)**

For self-hosted Atlassian instances (JIRA Data Center, Confluence Data Center):

1. Go to your **user profile** in JIRA or Confluence
2. Navigate to **Personal Access Tokens** (usually under Profile → Personal Access Tokens)
3. Click **Create token**, give it a name, and set an expiry
4. Copy the token

Personal access tokens authenticate as your user without needing a separate username. This is the standard approach for enterprise and Data Center deployments.

### 2. Configure `.mcp.json`

Create or update `.mcp.json` in your project root. Pick the config that matches your authentication method.

**Option A: Cloud (API token + username)**

```json
{
  "mcpServers": {
    "mcp-atlassian": {
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

**Option B: Enterprise / Data Center (personal access token)**

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://jira.your-company.com",
        "JIRA_PERSONAL_TOKEN": "your-personal-access-token",
        "CONFLUENCE_URL": "https://confluence.your-company.com",
        "CONFLUENCE_PERSONAL_TOKEN": "your-personal-access-token"
      }
    }
  }
}
```

Notice the difference: Cloud uses `_USERNAME` + `_API_TOKEN` pairs. Enterprise uses a single `_PERSONAL_TOKEN` per service — no username needed, the token carries your identity.

This file configures the MCP server as a local process. When you start a Claude Code session, the agent discovers the server and gains access to all its tools — JIRA search, issue creation, Confluence page reads, and more.

> **Note:** `.mcp.json` contains credentials. Add it to `.gitignore` so it doesn't end up in version control. Alternatively, store tokens in environment variables and reference them in the config.

### 3. Verify

Restart Claude Code (the agent picks up MCP config at session start), then ask:

> "What Atlassian MCP tools are available?"

You should see tools like `mcp__mcp-atlassian__jira_search`, `mcp__mcp-atlassian__confluence_get_page`, and others. If the tools don't appear, check that `uvx` is installed (`pip install uv`) and that your credentials are correct.

---

## Beyond Stories — What Else the Atlassian MCP Unlocks

Once the Atlassian MCP is configured, it's not just for user stories. The agent now has full access to JIRA and Confluence as tools — and you can use them from any conversation, any skill, or any workflow.

Here are tasks that become natural once the connector is in place:

### Pull a Confluence page into context

> "Find the architecture decision record for the payment service on Confluence and summarize it"

The agent searches Confluence, reads the page, and gives you a summary — all in the conversation. No browser tab, no copy-paste. This is useful when you're about to start coding and need to check what was decided months ago.

### Generate a sprint report from JIRA

> "Show me all stories completed in the last sprint for project CYD, grouped by epic"

The agent queries JIRA, filters by sprint and status, and presents a formatted report. You can ask follow-ups: "Which ones had subtasks?", "What's still in progress?"

### Bulk-update stories

> "Add the label 'tech-debt' to all stories in epic CYD-116 that don't have it"

The agent searches for matching issues, checks labels, and updates them one by one. This would take dozens of clicks in the JIRA UI.

### Cross-reference code and tickets

> "Find all JIRA issues that mention the PaymentService class and check if any are still open"

The agent searches JIRA for the class name, filters by status, and reports back. Useful for understanding whether known issues exist before you refactor.

### Bring Confluence docs into your project

> "Download the API design spec from Confluence and save it as a local markdown file in docs/"

The agent fetches the page, converts it to markdown, and writes it to disk. Now it's a local reference — available offline, trackable in git, and always in the agent's context.

The pattern is the same every time: **you describe what you need in natural language, and the agent uses MCP tools to get it done.** The Atlassian MCP turns JIRA and Confluence from browser-based manual tools into things your agent can query, update, and integrate into any workflow.

---

## Limitations and Rough Edges

This workflow isn't perfect. Here's what you'll run into and how to deal with it.

### Confluence pages can be huge

A detailed architecture page or a requirements document with embedded diagrams can easily run to thousands of words. When the agent reads a large Confluence page through MCP, all that content goes into the conversation context — eating up tokens fast. If you load three or four large pages as references, you may hit context limits before the agent even starts writing.

**Workarounds:**
- **Download and trim.** Use `download-refs` to save pages locally, then edit the local copy to keep only the sections you actually need. The agent reads the trimmed version.
- **Be selective.** Don't add every Confluence page as a reference. Add the ones that directly inform the story you're writing. You can always add more later.
- **Summarize first.** Ask the agent to summarize a Confluence page before adding it as a reference. Save the summary as a local markdown file and use that instead of the full page.

### JIRA formatting breaks on complex content

JIRA's description field uses its own markup format (Atlassian Document Format in Cloud, wiki markup in Data Center). Simple content — paragraphs, bullet lists, headings — translates fine from markdown. But complex formatting often breaks:

- **Tables** render inconsistently or lose their structure
- **Nested lists** may flatten or misalign
- **Code blocks** sometimes lose syntax highlighting or indentation
- **Embedded images** and attachments don't transfer through the API

To be fair, this isn't just an MCP problem — JIRA's formatting is fragile even when you create content manually through the UI. Tables in particular are notorious for breaking on paste.

**Workaround: markdown file + copy-paste.** For stories with complex formatting, use the skill to generate a polished markdown file locally (`user-stories/stories/<slug>.md`), then copy-paste the content into JIRA manually. You keep the well-formatted markdown in version control, and JIRA gets whatever it can render. This sounds like a step backward, but in practice it's the most reliable approach — and you still saved all the time the agent spent gathering context, synthesizing references, and drafting the content.

### MCP availability varies

Not every team can install MCP servers. Corporate environments may restrict what processes can run locally, or security policies may block API token creation. The skill handles this through graceful degradation, but it's worth setting expectations: **the full workflow (Confluence read → draft → JIRA push) requires MCP.** Without it, you get a powerful local drafting tool — which is still valuable, just not end-to-end automated.

---

## Key Takeaways

This chapter showed a pattern that extends well beyond user stories:

1. **Non-coding tasks follow the same skill structure.** Inputs, template, connectivity — whether you're creating stories, writing test plans, or generating release notes. The patterns from Chapter 7 apply directly.
2. **Your instruction files are already a data source.** `CLAUDE.md`, `AGENTS.md`, and scoped configs already describe your project architecture. The agent starts with more context than you think.
3. **External data needs a bridge.** MCP servers connect the agent to systems like JIRA and Confluence. Design for graceful degradation — the skill should work without the bridge, just with less automation.
4. **Templates carry the configuration.** Put project-specific details (JIRA field mappings, custom fields, defaults) in the template, not the skill code. One skill serves multiple projects — just swap the template.
5. **Simplicity is power.** A folder, a CLAUDE.md, and a template can replace hundreds of lines of Python. Start with the minimum that works. Add structure only when the simple version breaks down.
6. **Separate config from logic, use plain English, persist state in files.** When you do build a full skill, these best practices keep it readable, portable, and reliable across sessions and team members.
6. **MCP servers are force multipliers.** Once configured, the Atlassian MCP isn't just for story creation — it's available for any task that touches JIRA or Confluence. Sprint reports, bulk updates, pulling docs into context. One setup, many use cases.
7. **Know where the seams are.** Large Confluence pages eat context tokens. JIRA formatting breaks on complex content like tables. MCP may not be available in every environment. Design around these limits — download and trim, generate locally then copy-paste, degrade gracefully.

---

## What's Next

This skill lightly touched MCP — the Atlassian connector that lets the agent read Confluence and push to JIRA. In the next chapter, we'll go deeper: what MCP is, how it works, how to configure servers, and how to build your own. MCP is the bridge between your agent and the rest of your toolchain — CI/CD, databases, monitoring, communication platforms.

After that, we'll apply the same patterns to more tasks: UI testing, integration tests, log gathering. The skill-building techniques are the same. The templates change. The MCP servers change. But the approach stays consistent.

---

## Resources

- [User Story Skill — Full Implementation](./user-stories/) — The complete skill with SKILL.md, templates, reference manager, and usage guide
- [User Story Skill — Simple Version](./user-stories-simple/) — The KISS version: just a CLAUDE.md, a template, and a stories folder
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io) — Official MCP specification and documentation
- [mcp-atlassian](https://github.com/sooperset/mcp-atlassian) — Open-source Atlassian MCP server for JIRA and Confluence
- [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) — Generate API tokens for Atlassian Cloud authentication
- [Chapter 7: Creating Reusable Skills and Simple Agents](../07_skills-and-agents/07_skills-and-agents.md) — Skill-building foundations this chapter builds on
- [Chapter 8: Multi-Agent Workflows](../08_workflows/08_workflows.md) — Workflow orchestration patterns
