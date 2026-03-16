# Chapter 4 — The Big Picture

**Time:** 45 min

In the previous chapters you zoomed in: what agents are, how to prompt them, how to code with them. Now step back. Look at the whole machine.

This chapter gives you a mental model of how an AI coding agent actually works — not the marketing version, but the architecture. Once you see the full picture, you stop guessing and start controlling.

---

## The Architecture at a Glance

Every AI coding agent — Claude Code, GitHub Copilot, Cursor — follows the same basic architecture. Four layers, one loop.

```mermaid
flowchart TD
    subgraph YOU["YOU (the developer)"]
        Y["Prompts, reviews, steers, approves"]
    end

    subgraph CONTEXT["CONTEXT"]
        C1["Project instructions\n(CLAUDE.md)"]
        C2["Memory files\n(MEMORY.md)"]
        C3["Conversation\nhistory"]
        C4["System\nprompt"]
        C5["Rules &\nskill defs"]
        C6["File contents,\ntool outputs"]
    end

    subgraph AGENT["THE AGENT (ReAct Loop)"]
        Think --> Act --> Observe --> Think
    end

    subgraph CAPABILITIES["CAPABILITIES"]
        T1["Built-in Tools\nRead, Write, Edit,\nBash, Grep, Glob"]
        T2["MCP Servers\nGitHub, Sentry, Slack,\ndatabases, custom APIs"]
        T3["Extensions\nSkills, subagents, hooks, custom commands"]
    end

    YOU --> CONTEXT --> AGENT -- uses --> CAPABILITIES
```

Four layers:

1. **You** — the developer who provides intent and judgment
2. **Context** — everything the agent knows when it starts thinking
3. **The Agent** — the ReAct loop that reasons and acts
4. **Capabilities** — the tools and extensions the agent can use

The agent sits in the middle. Context flows down into it. It reaches out to capabilities to act. You sit on top, steering. Understanding these layers — and which parts you control — is the key to working effectively with agents.

---

## The Agent: The ReAct Loop

At the center of everything is a loop. Not code you write. Not a plugin you install. A reasoning pattern called **ReAct** (Reason + Act).

```mermaid
flowchart LR
    Think --> Act --> Observe --> Think
```

When you give an agent a task, it doesn't execute a script. It **reasons** about what to do, **acts** using a tool, **observes** the result, and then **reasons** again about what to do next. This cycle repeats until the task is done or the agent decides it needs your input.

A simple example — "fix the failing test in auth.test.ts":

| Step | Phase | What happens |
|------|-------|-------------|
| 1 | Think | "I need to read the test file to understand the failure" |
| 2 | Act | Reads `auth.test.ts` |
| 3 | Observe | Sees the test expects a 200 but gets a 401 |
| 4 | Think | "The auth middleware might be blocking. Let me check." |
| 5 | Act | Reads `middleware/auth.ts` |
| 6 | Observe | Finds a missing token validation path |
| 7 | Think | "I need to add a check for expired tokens" |
| 8 | Act | Edits `middleware/auth.ts` |
| 9 | Observe | File saved |
| 10 | Think | "Let me verify the fix by running the test" |
| 11 | Act | Runs `npm test auth.test.ts` |
| 12 | Observe | Test passes |
| 13 | Think | "Done. The fix handles expired tokens correctly." |

This loop is what makes agents different from chat assistants. A chat assistant would stop at step 3 and say "here's what you could try." The agent keeps going.

**You don't control the loop itself.** You control what goes into it (context) and what it can do (capabilities). That's where your leverage is.

---

## Context: The Most Important Layer

Here's the truth about AI coding agents: **the agent has no memory**. Every time you start a new session, it knows nothing about your project. Nothing about your preferences. Nothing about what you did yesterday.

Everything the agent knows comes from **context** — the information loaded into its context window at the start of a session and accumulated during the conversation. Context is your primary lever for making agents reliable.

### What Makes Up the Context

```mermaid
flowchart TD
    subgraph CW["CONTEXT WINDOW"]
        direction TB
        subgraph AUTO["AUTOMATIC (you don't control)"]
            A1["System prompt — Core instructions from the tool vendor. Read-only."]
            A2["Tool definitions — Descriptions of available tools. Grows with MCP."]
            A3["Compaction summaries — Older messages get summarized automatically."]
        end

        subgraph YOU["YOU CONTROL"]
            B1["Project instructions (persistent) — CLAUDE.md, copilot-instructions.md, AGENTS.md. Loaded every session."]
            B2["Memory files (persistent) — MEMORY.md auto, first 200 lines. Topic files load on demand."]
            B3["Rules (persistent, scoped) — .claude/rules/*.md. Load when matching files are accessed."]
            B4["Your prompts (session) — What you type. The intent, constraints, examples."]
            B5["Conversation history (session) — Builds up turn by turn. Lost on compaction."]
            B6["File contents & outputs (session, on demand) — What the agent reads and what tools return."]
        end
    end
```

### The Control Matrix

| Context source | Who writes it | When it loads | Persists across sessions | You can edit it |
|---|---|---|---|---|
| System prompt | Tool vendor | Session start | Always | No |
| Tool definitions | Built-in + MCP config | Session start | Always | Indirectly (MCP config) |
| Project instructions (CLAUDE.md) | You | Session start | Yes | Yes |
| User instructions (~/.claude/CLAUDE.md) | You | Session start | Yes | Yes |
| Rules (.claude/rules/) | You | On demand (path-scoped) | Yes | Yes |
| Auto-memory (MEMORY.md) | Agent (you can edit) | Session start (200 lines) | Yes | Yes |
| Skill descriptions | You | Session start | Yes | Yes |
| Your prompt | You | When you type | No (session only) | N/A |
| Conversation history | You + agent | Accumulated | No (session only) | No |
| File contents | Codebase | On demand (agent reads) | No (session only) | Yes (your code) |
| Tool outputs | Tools | On demand (agent runs) | No (session only) | No |
| Compaction summaries | Agent | When context fills | No | No |

Here's what each of these looks like in practice:

**System prompt** — The vendor's built-in instructions. You never see the full text, but it tells the agent things like "you are Claude Code, an AI coding assistant" and defines its core behavior. You can't edit it.

**Tool definitions** — Each tool the agent can use has a description: what it does, what parameters it takes. The agent reads these to decide which tool fits. When you add MCP servers, their tool definitions get added here too — which is why many MCP servers means more context consumed.

**Project instructions (CLAUDE.md)** — Your team's ground truth. Lives in the repo root. Every session starts by reading this file. This is where you put tech stack, conventions, and guardrails.

```markdown
# CLAUDE.md
- We use TypeScript strict mode with Vitest for testing
- API routes go in src/routes/, one file per resource
- Never use `any` — use `unknown` and narrow
- Run `npm run lint` before committing
```

**In GitHub Copilot:** the equivalent is `.github/copilot-instructions.md` — a single markdown file auto-included in every chat and agent session. Copilot also reads `CLAUDE.md` for cross-tool compatibility, so a team can maintain one file that works with both agents.

**User instructions (~/.claude/CLAUDE.md)** — Like project instructions, but personal. Applies to all your projects. Good for editor preferences, commit style, or tools you always want available.

**Rules (.claude/rules/)** — Scoped instructions that load only when the agent touches matching files. This is the least-known but most powerful targeting mechanism. Each rule file has a `globs` frontmatter that controls when it activates.

```markdown
# .claude/rules/api-routes.md
---
globs: src/routes/**/*.ts
---
- Every route must validate input with zod
- Return standard error format: { error: string, code: number }
- Always add rate limiting middleware
```

Rules are invisible until the agent reads or edits a file matching the glob. Then they inject into context automatically. Think of them as "if the agent touches this area, remind it of these constraints."

**In GitHub Copilot:** the equivalent is `.github/instructions/*.instructions.md`. Same idea — scoped markdown files with YAML frontmatter — but the key is `applyTo` instead of `globs`:

```markdown
# .github/instructions/api-routes.instructions.md
---
applyTo: "src/routes/**/*.ts"
---
- Every route must validate input with zod
- Return standard error format: { error: string, code: number }
```

VS Code agent mode also reads `.claude/rules/` for cross-tool compatibility.

**Auto-memory (MEMORY.md)** — The agent writes this file to remember things across sessions: your preferences, patterns it learned, corrections you made. The first 200 lines load automatically. You can edit it directly — it's just a markdown file.

**In GitHub Copilot:** Copilot Memory (agentic memory) serves a similar purpose but works differently. Instead of a file you edit, Copilot autonomously discovers and stores repository-level facts — conventions, architecture, dependencies — with citations back to the code. Memories auto-expire after 28 days but renew if validated. You can't edit the memory directly; the system manages it. The Claude Code approach (a plain markdown file) gives you more control; the Copilot approach is more hands-off.

**Skill descriptions** — When you define skills (`.claude/skills/`), their names and descriptions load at session start so the agent knows what's available. The full skill content only loads when invoked.

**Your prompt** — What you type. The most direct but least persistent form of context.

**Conversation history** — Every message you and the agent exchange. Builds up during a session but gets summarized (compacted) when the context window fills up. Important details can be lost during compaction.

**File contents & tool outputs** — What the agent reads from your codebase or gets back from running commands. These are ephemeral — first to be compacted away in long sessions.

**Compaction summaries** — When context fills up, the agent summarizes older messages to free space. You don't control what gets kept or dropped. This is why persistent context (CLAUDE.md, rules) matters more than things you said 50 messages ago.

### How Context Maps to the Message Model

Under the hood, every LLM conversation is a sequence of **messages** with roles. Understanding this helps you see where each context type actually lands:

| Message role | What it contains | Who sends it |
|---|---|---|
| **system** | System prompt, CLAUDE.md, MEMORY.md, rules, tool definitions | The tool (invisible to you) |
| **user** (human) | Your prompts, hook outputs | You (and the tool on your behalf) |
| **assistant** (AI) | Agent's reasoning, tool calls, responses | The model |
| **tool** | Results from Read, Bash, Grep, MCP calls, subagent results, etc. | The tool execution environment |

The key insight: **persistent context you configure ends up in the system message or injected as annotations on conversation messages.** Both are seen before or alongside your prompts. That's why persistent context is so effective.

The **system message** is the highest-priority slot — it contains the vendor's core instructions plus your project-level files (CLAUDE.md, MEMORY.md, rules). The model treats system content as ground truth.

Beyond the system message, the tool injects additional context as **annotations on conversation messages** — typically as `<system-reminder>` tags appended to user messages or tool results. Skill descriptions, deferred tool lists, and other metadata arrive this way. The agent sees them, but they're technically part of the conversation flow, not the system prompt.

> **Note:** The exact placement varies by tool and version. Claude Code currently injects skill descriptions as `<system-reminder>` annotations on tool results. Other tools may place them elsewhere. The principle matters more than the exact implementation: some context is system-level (highest priority, never compacted), some is injected into the conversation (still high priority, but subject to compaction in long sessions).

```mermaid
flowchart LR
    subgraph system["system message"]
        S1["System prompt\n(vendor instructions)"]
        S2["CLAUDE.md"]
        S3["MEMORY.md"]
        S4["Rules files"]
        S5["Tool definitions"]
    end

    subgraph conversation["conversation messages"]
        subgraph user["user messages"]
            U1["Your prompts"]
            U2["Hook outputs"]
        end

        subgraph assistant["assistant messages"]
            A1["Agent reasoning"]
            A2["Tool calls\n(including subagent spawns)"]
        end

        subgraph tool["tool results"]
            T1["File contents"]
            T2["Command outputs"]
            T3["MCP results"]
            T4["Subagent results"]
        end
    end

    annotations["Injected annotations\n(skill descriptions,\ndeferred tool lists)"]

    system --> conversation
    annotations -.->|appended to\nuser/tool messages| conversation
```

**Where skills and agents land in the message flow:**

- **Skill descriptions** (name, one-line summary) are injected as annotations on conversation messages — the agent sees them early and knows what `/commands` are available. The full skill content is **not** loaded yet, keeping things lean. Because these are annotations on the conversation (not the system prompt), they can get compacted in very long sessions — though in practice they're re-injected periodically.
- **Invoked skill content** — when you type `/skill-name`, the tool expands the skill's full markdown (all the step-by-step instructions, constraints, examples) and injects it into the conversation as if you had typed it yourself. This is why skills feel like prompts on steroids: they literally become your prompt.
- **Subagent spawns** are **tool calls** in the assistant message. When the main agent decides to delegate work, it calls the Agent tool like any other tool. The subagent runs in its own isolated context window — separate system message, separate conversation — and returns a summary as a **tool result**. The main agent never sees the subagent's internal reasoning, only the final answer.
- **Custom agents** (Copilot's `.agent.md` files) work similarly — they define a separate system prompt and tool restrictions. When invoked via `@agent-name`, a new context is created with that agent's instructions in its system message.

This matters because it tells you what the agent sees and when:

| What you define | Where it lands | When the agent sees it |
|---|---|---|
| CLAUDE.md, MEMORY.md, rules | System message | Always (highest priority, never compacted) |
| Skill name + description | Annotation on conversation messages | Session start (re-injected periodically) |
| Skill full content | Conversation (as your prompt) | Only when invoked |
| Subagent instructions | Subagent's system message | Only the subagent sees it |
| Subagent result | Tool result (main agent) | After the subagent finishes |
| Custom agent persona | That agent's system message | Only that agent sees it |

The practical implication: skill descriptions consume context all the time, but the full content only costs context when used. If you have 20 skills, the agent sees 20 short descriptions — manageable. But invoking a skill with a 500-line playbook adds all 500 lines to your conversation. Design skills to be as concise as they need to be, no more.

The conversation alternates: system sets the stage, you send a prompt (user), the agent reasons and calls tools (assistant), tools return results (tool), the agent reasons again (assistant), and so on. Compaction summarizes older user/assistant/tool messages but the system message stays intact — another reason why CLAUDE.md outlasts anything you say in conversation.

### The Hierarchy of Context

Not all context is equal. Here's the priority, from most to least reliable:

```mermaid
flowchart TD
    P1["Project instructions (CLAUDE.md)<br/>Your team's ground truth"]
    P2["Auto-memory (first 200 lines)<br/>MEMORY.md — learned preferences"]
    P3["Rules files (path-specific)<br/>.claude/rules/ — scoped guardrails"]
    P4["Your current prompt<br/>What you ask right now"]
    P5["Conversation history<br/>Builds up, then gets compacted away"]
    P6["Tool outputs & file reads<br/>On-demand, cleared first during compaction"]

    P1 -- "always loaded,<br/>persistent" --- P2 --- P3 --- P4 --- P5 -- "ephemeral,<br/>compacted" --- P6

    style P1 fill:#2d6a4f,color:#fff
    style P2 fill:#40916c,color:#fff
    style P3 fill:#52b788,color:#fff
    style P4 fill:#74c69d,color:#000
    style P5 fill:#b7e4c7,color:#000
    style P6 fill:#d8f3dc,color:#000
```

**The takeaway:** If something matters, put it in CLAUDE.md or a rules file. Don't rely on saying it once in conversation — it will get compacted away in long sessions.

### Why Context Is Everything

The agent starts every session blank. It doesn't remember your last conversation. It doesn't know your project uses Tailwind or that you prefer functional components. It doesn't know your test runner is Vitest, not Jest.

Context is how you teach it — every single time. The good news: you can automate most of that teaching.

```
Session 1:  "We use TypeScript with strict mode."
Session 2:  "We use TypeScript with strict mode."   ← you again
Session 3:  "We use TypeScript with strict mode."   ← still you

  vs.

CLAUDE.md:  "We use TypeScript with strict mode."   ← once, always loaded
```

This is the most important lesson in this chapter: **invest in your persistent context files**. A well-crafted CLAUDE.md is worth more than perfect prompting.

---

## Capabilities: What the Agent Can Do

The agent reasons. But reasoning alone doesn't ship code. It needs **tools** — the hands that turn thoughts into actions.

### Built-in Tools

Every agent ships with a core set of tools. These are always available, no configuration needed.

| Tool | What it does | Category |
|------|-------------|----------|
| **Read** | Read file contents | File operations |
| **Write** | Create new files | File operations |
| **Edit** | Modify existing files (line-level diffs) | File operations |
| **Glob** | Find files by name pattern (`**/*.ts`) | Search |
| **Grep** | Search file contents with regex | Search |
| **Bash** | Run any shell command (tests, builds, git) | Execution |
| **Agent** | Spawn subagents for parallel/isolated work | Orchestration |
| **WebFetch** | Fetch URLs, convert to markdown | Web |
| **WebSearch** | Search the web | Web |

These tools map directly to the ReAct loop. The agent **thinks** about what to do, then **acts** using one of these tools, then **observes** the result.

**In GitHub Copilot:** agent mode has a similar set — file read/edit, terminal execution, text and file search, web fetch — plus a few extras like `usages` (find references via LSP) and `rename` (LSP-powered refactoring across files). The Copilot coding agent on GitHub.com adds CodeQL security analysis and secret scanning. The tool names differ but the categories are the same.

You don't choose which tool the agent uses — it decides based on context. But you influence the choice. "Search the codebase for usages of `getUserById`" nudges it toward Grep. "Create a new component" nudges it toward Write.

**Permissions** are how you control tool access:

| Mode | What the agent can do |
|------|----------------------|
| **Plan mode** | Read-only. Agent can think and search but not change anything. |
| **Default** | Agent asks before risky actions (Bash commands, file writes). |
| **Auto-accept edits** | File edits go through without asking. Bash still asks. |
| **Full auto** | Everything goes through. Use with caution. |

You cycle between modes with `Shift+Tab` during a session. Start with plan mode to explore, then switch to default for implementation.

**In GitHub Copilot:** similar tiers exist. VS Code offers Default Approvals (confirm each tool), Bypass Approvals (auto-approve all), and Autopilot (auto-approve + continue autonomously). Copilot CLI has Interactive (default), Plan mode (`Shift+Tab`), and Autopilot (`Shift+Tab` again). The coding agent on GitHub.com always requires a human-reviewed PR — there's no fully autonomous mode for merged code.

### MCP Servers: Extending the Toolbox

Built-in tools cover files, search, and shell commands. But what about GitHub issues? Slack messages? Database queries? Sentry errors?

That's what **MCP** (Model Context Protocol) does. It's an open standard that lets you plug external services into your agent as new tools.

```mermaid
flowchart BT
    Agent["THE AGENT\n(picks the right tool)"]

    subgraph Built-in["Built-in Tools"]
        B["Read, Write, Edit,\nBash, Grep, Glob"]
    end

    subgraph GitHub["MCP Server (GitHub)"]
        G["create_issue, list_prs,\nadd_comment"]
    end

    subgraph Postgres["MCP Server (Postgres)"]
        P["query, list_tables,\ndescribe"]
    end

    Built-in --> Agent
    GitHub --> Agent
    Postgres --> Agent
```

After configuration, MCP tools look just like built-in tools to the agent. It can call `create_issue` as naturally as it calls `Read`.

**Configuration scopes:**

| Scope | File | Shared with team | Use case |
|-------|------|-----------------|----------|
| Project | `.mcp.json` (repo root) | Yes (via git) | Team tools: shared database, project Sentry |
| User | `~/.claude.json` | No | Personal tools: your Slack, your GitHub |
| Local | `~/.claude.json` (project path) | No | Local dev: your database, your API keys |

**The trade-off:** Each MCP server adds tool definitions to your context window. More servers = less room for everything else. Claude Code handles this with **Tool Search** — when MCP tools exceed ~10% of context, it loads tool descriptions on demand instead of all at once.

**In GitHub Copilot:** MCP configuration lives in `.vscode/mcp.json` (workspace-level, shareable via git) or your user-profile `mcp.json`. Both stdio and SSE transports are supported. Enterprise admins can configure MCP registries with allowlists to control which servers teams can use.

---

## Extensions: Customizing the Agent

Tools let the agent act. Extensions let you shape **how** it acts.

### Skills: Reusable Instructions

A skill is a markdown file that teaches the agent a workflow. Think of it as a macro — instead of typing the same instructions every session, you save them as a skill.

```markdown
# .claude/skills/api-endpoint/SKILL.md
---
name: api-endpoint
description: Create a new REST API endpoint following project conventions
allowed-tools: Read, Write, Edit, Bash, Grep
---

When creating a new API endpoint:

1. Check existing endpoints in src/routes/ for patterns
2. Create route file in src/routes/
3. Add request/response types in src/types/
4. Write tests in tests/routes/
5. Update the route index in src/routes/index.ts
6. Run tests to verify
```

Now you type `/api-endpoint POST /users/reset-password` and the agent follows your workflow, not its own improvisation.

**Where skills live:**

| Location | Scope | Shared |
|----------|-------|--------|
| `.claude/skills/` | Project | Yes, via git |
| `~/.claude/skills/` | User (all projects) | No |

**In GitHub Copilot:** two mechanisms cover this. **Agent skills** use `SKILL.md` files in `.github/skills/` or `.agents/skills/` — same concept, similar frontmatter (`name`, `description`, `argument-hint`), invoked via `/skill-name`. **Prompt files** (`.prompt.md`) are a lighter alternative — markdown files you invoke via `/prompt-name` in chat. Copilot also reads `.claude/skills/` for cross-tool compatibility.

### Subagents: Delegation

When a task is complex, the agent can spawn **subagents** — isolated instances that handle a subtask and return a summary.

```mermaid
flowchart TD
    Main["Main agent"]
    E["Explore subagent\n(read-only)"]
    T1["Task subagent\n(full access)"]
    T2["Task subagent\n(full access)"]

    Main --> E -- result --> R1["Here's how auth works\nin this codebase"]
    Main --> T1 -- result --> R2["Tests written\nand passing"]
    Main --> T2 -- result --> R3["Component\nrefactored"]
```

Built-in subagent types:

| Type | Access | Best for |
|------|--------|----------|
| **Explore** | Read-only | Codebase research, finding patterns |
| **Plan** | Read-only | Designing implementation approach |
| **General-purpose** | Full | Complex multi-step tasks |

You can also create custom subagents with restricted tools, specific models, and tailored instructions — useful for enforcing patterns across a team.

**In GitHub Copilot:** the coding agent uses built-in specialized subagents — Explore (codebase analysis), Task (builds/tests), Code Review, and Plan. Beyond that, Copilot supports **custom agents** defined as `.agent.md` files with YAML frontmatter (`name`, `description`, `tools`, `mcp-servers`). You invoke them via `@agent-name` — for example, `@docs-agent` or `@security-agent`. This goes further than Claude Code's subagent model by letting you define named personas with restricted toolsets.

### Hooks: Automation at Lifecycle Points

Hooks are shell commands or scripts that fire at specific moments in the agent's lifecycle.

| Hook | Fires when | Example use |
|------|-----------|-------------|
| `PreToolUse` | Before the agent uses a tool | Block edits to protected files |
| `PostToolUse` | After a tool succeeds | Auto-format code after edits |
| `Stop` | Agent finishes responding | Run linter on changed files |
| `SessionStart` | Session begins | Inject dynamic context |
| `UserPromptSubmit` | Before processing your prompt | Validate or enrich prompts |

Hooks give you **guardrails and automation** without changing how the agent reasons. The agent doesn't know about your hooks — they run around it, not through it.

**In GitHub Copilot:** hooks live in `.github/hooks/*.json` and support eight lifecycle events: `sessionStart`, `sessionEnd`, `userPromptSubmitted`, `preToolUse`, `postToolUse`, `agentStop`, `subagentStop`, and `errorOccurred`. Each hook specifies a shell command, receives JSON input about the agent action, and can approve or deny tool executions. The concept is the same — guardrails that run around the agent, not through it.

---

## Putting It All Together

Now you see the full picture. Here's how the layers interact in a real workflow:

```mermaid
flowchart TD
    Prompt["You type: 'Add rate limiting to the /api/upload endpoint'"]

    subgraph Context["CONTEXT LOADS"]
        CL1["CLAUDE.md: We use Express.\nRate limiting uses express-rate-limit.\nTests in tests/."]
        CL2["MEMORY.md: User prefers\nfunctional middleware."]
        CL3["System prompt + Tool definitions"]
        CL4["Your prompt: Add rate limiting\nto /api/upload"]
    end

    subgraph ReAct["REACT LOOP"]
        S1["Think: I need to find the upload endpoint"]
        S2["Act: Grep /api/upload → finds routes/upload.ts"]
        S3["Think: Let me check existing rate limiting patterns"]
        S4["Act: Grep rateLimit → finds middleware/rate.ts"]
        S5["Think: I'll use the existing helper, add tests"]
        S6["Act: Edit routes/upload.ts\nWrite tests/upload-rate-limit.test.ts\nBash: npm test"]
        S7["Hook fires: PostToolUse → prettier formats files"]
        S8["Think: Done. Rate limiting added,\ntests passing."]

        S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7 --> S8
    end

    Prompt --> Context --> ReAct
```

Notice what happened:

- **CLAUDE.md** told the agent the tech stack and test location — you didn't need to say it
- **MEMORY.md** shaped the style — functional middleware, not a class
- **Built-in tools** (Grep, Edit, Write, Bash) did the actual work
- **A hook** (prettier) auto-formatted without the agent knowing
- **Your prompt** was 8 words — the context did the rest

---

## What This Means for You

Understanding the big picture changes how you work with agents. Here are the practical implications:

### 1. Invest in persistent context, not perfect prompts

Your prompt is maybe 50 words. Your CLAUDE.md is loaded every session and can be thousands of words. One hour spent writing a good CLAUDE.md pays off across hundreds of sessions.

| Investment | Impact | Persistence |
|-----------|--------|------------|
| Better prompt | This task | Gone next session |
| Better CLAUDE.md | Every task | Permanent (version-controlled) |
| Better rules files | Specific file patterns | Permanent |
| Better skills | Specific workflows | Permanent |

### 2. Understand what you control

| You control fully | You influence | You don't control |
|---|---|---|
| CLAUDE.md | Tool selection | System prompt |
| Rules files | Subagent delegation | Compaction strategy |
| Skills | Auto-memory content | ReAct reasoning |
| MCP configuration | Conversation flow | Tool definitions |
| Hooks | | |
| Permission modes | | |
| Your prompts | | |

Don't fight the things you can't control. Work with them. If the agent picks the wrong tool, adjust your prompt context. If compaction loses important instructions, put them in CLAUDE.md instead.

### 3. Build your system incrementally

You don't need to configure everything on day one. Start simple and layer up as you hit friction:

```mermaid
flowchart TD
    W1["Week 1: Just prompts and conversation"]
    F1(["I keep repeating the same setup instructions..."])
    W2["Week 2: Add CLAUDE.md with project basics"]
    F2(["I want path-specific rules..."])
    W3["Week 3: Add rules files for test patterns, API conventions"]
    F3(["I keep typing the same workflow..."])
    W4["Week 4: Create skills for common tasks"]
    F4(["I need GitHub integration..."])
    W5["Week 5: Add MCP servers — GitHub, Sentry"]
    F5(["I want auto-formatting after edits..."])
    W6["Week 6: Add hooks for code quality"]

    W1 --> F1 --> W2 --> F2 --> W3 --> F3 --> W4 --> F4 --> W5 --> F5 --> W6

    style F1 fill:#fff3cd,color:#000
    style F2 fill:#fff3cd,color:#000
    style F3 fill:#fff3cd,color:#000
    style F4 fill:#fff3cd,color:#000
    style F5 fill:#fff3cd,color:#000
```

Each layer solves a real friction you've experienced. Don't pre-optimize.

### 4. The agent learns your project through context, not experience

Unlike a human teammate, the agent won't gradually "get" your codebase. It starts fresh every time. But unlike a human teammate, it reads your entire CLAUDE.md in under a second and follows it perfectly.

This is the mental shift: stop thinking of the agent as a junior developer who learns over time. Think of it as an expert who arrives each morning with amnesia — but reads your briefing document cover to cover before starting work.

Your job is to make that briefing document excellent.

---

## Cross-Tool Reference

The architecture is the same across agents. The file names differ.

| Feature | Claude Code | GitHub Copilot |
|---|---|---|
| Project instructions | `CLAUDE.md` | `.github/copilot-instructions.md` (also reads `CLAUDE.md`) |
| Scoped rules | `.claude/rules/*.md` (`globs:`) | `.github/instructions/*.instructions.md` (`applyTo:`) |
| Memory | `MEMORY.md` (editable file) | Copilot Memory (auto-managed, 28-day expiry) |
| Skills | `.claude/skills/SKILL.md` | `.github/skills/SKILL.md` + `.prompt.md` files |
| MCP config | `.mcp.json` / `~/.claude.json` | `.vscode/mcp.json` / user `mcp.json` |
| Hooks | `.claude/settings.json` (`hooks`) | `.github/hooks/*.json` |
| Subagents | `Agent` tool (Explore, Plan, General) | Built-in (Explore, Task, Review, Plan) + custom `.agent.md` |
| Custom agents | Skills + subagent tool | `.agent.md` files, invoked via `@agent-name` |
| Permission modes | Plan → Default → Auto-accept → Full auto | Interactive → Plan → Autopilot |

The concepts transfer. If you learn to write good rules in Claude Code, those same rules work in Copilot (and vice versa). Invest in the skill, not the syntax.

---

## Where to Focus Your Effort

This chapter covered the architecture. But the real question is: **now that you see the machine, where should you spend your time?**

Not all layers give you equal return. Here's the priority, ranked by impact per hour invested:

| Priority | Area | Why it matters | Time to set up |
|---|---|---|---|
| 1 | **Project instructions** (CLAUDE.md) | Loaded every session, shapes every task. One hour here saves hundreds of repeated prompts. | 30–60 min |
| 2 | **Scoped rules** | Prevent entire categories of mistakes automatically. The agent doesn't forget rules like it forgets conversation. | 15 min per rule |
| 3 | **Skills for repeated workflows** | If you type the same workflow more than twice, it should be a skill. Consistency compounds. | 20 min per skill |
| 4 | **MCP servers for your stack** | Connecting GitHub, your database, or your error tracker turns the agent from "code helper" to "team member." | 30 min per server |
| 5 | **Hooks for quality gates** | Auto-formatting, linting, and validation after every edit. Set once, never think about it again. | 15 min per hook |
| 6 | **Better prompts** | Still matters — but only after the persistent layers are solid. A great prompt on a weak context is wasted effort. | Ongoing |

The pattern: **invest in the things that persist first.** A prompt helps once. A CLAUDE.md helps forever. A rule prevents bugs before they happen. A skill encodes your team's best workflow so nobody has to reinvent it.

Most developers start with prompts and stay there. The ones who get the most from agents invest early in the layers above the prompt — the context, the rules, the skills. That's where the leverage is.

---

## Key Takeaways

1. **Four layers:** You → Context → Agent (ReAct) → Capabilities. Understanding these layers is understanding the machine.

2. **Context is your primary lever.** The agent has no memory. Everything it knows comes from context. Invest in persistent context (CLAUDE.md, rules, skills) over session context (prompts, conversation).

3. **The ReAct loop is the engine.** You don't control how it reasons. You control what it knows (context) and what it can do (tools).

4. **Tools are extensible.** Built-in tools handle files and shell. MCP extends to any external service. Skills and hooks customize behavior.

5. **The architecture is portable.** Claude Code, Copilot, Cursor — same layers, different file names. Learn the concepts, not just the syntax.

6. **Focus on what persists.** Project instructions, rules, and skills give you the highest return on time. Better prompts come last, not first.

---

## Resources

- [Claude Code documentation — Context](https://docs.anthropic.com/en/docs/claude-code/context) — How context loading works in Claude Code
- [Claude Code documentation — Memory](https://docs.anthropic.com/en/docs/claude-code/memory) — Memory and persistent context files
- [Claude Code documentation — MCP](https://docs.anthropic.com/en/docs/claude-code/mcp) — Configuring MCP servers
- [Claude Code documentation — Skills](https://docs.anthropic.com/en/docs/claude-code/skills) — Creating and using skills
- [Claude Code documentation — Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) — Lifecycle hooks
- [GitHub Copilot — Custom instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot) — Project instructions and scoped rules
- [GitHub Copilot — Agent skills](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills) — Creating reusable skills
- [GitHub Copilot — Hooks](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/use-hooks) — Lifecycle hooks for the coding agent
- [GitHub Copilot — Custom agents](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-custom-agents) — Defining named agent personas
- [How to write a great AGENTS.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/) — Lessons from 2,500+ repositories
- [Model Context Protocol](https://modelcontextprotocol.io/) — The MCP specification
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — The original ReAct paper
