# Chapter 8: Multi-Agent Workflows

## From L3 to L4

In Chapter 7, you reached L3 — reusable skills, shared team practices, and custom agents that handle well-defined tasks end to end. A code review skill, a test generator, a documentation writer. Each does one thing reliably.

But real development work rarely fits into a single step. Building a feature involves analysis, planning, implementation, testing, and documentation. Each step depends on the previous one. Each step can fail. And the longer the chain, the more things can go wrong.

This is where **workflows** come in. A workflow coordinates multiple agents or skills into a structured, multi-step process — with checkpoints, state management, and human review between steps.

Here's where we are on the maturity ladder:

| Level | What it looks like |
|-------|-------------------|
| L0 | No AI tools. No awareness. |
| L1 | Tools installed. First supervised attempts. Copy-paste prompting. |
| L2 | Daily individual use. Instruction files. Basic workflows: plan, build, test. |
| L3 | Team-level shared practices. Reusable skills and custom agents. |
| **L4** | **Structured workflows: spec, plan, implement, test, review. Human is PM and reviewer.** |
| L5 | Full SDLC automated. Multi-agent orchestration. |
| L6 | Dark Factory — fully automated. Theoretical horizon. |

This chapter takes you from L3 to L4. By the end, you'll understand how to design multi-step workflows, see five concrete implementations across Claude Code and GitHub Copilot, and know when to use each approach.

---

## Single-Responsibility Agents — The Foundation

Before building workflows, you need solid building blocks. Single-responsibility agents are reusable prompts that do **one job end to end**, with clear inputs and predictable outputs. Keeping the scope narrow makes them reliable, repeatable, and easy to share across teams.

You've already built these in Chapter 7. Here's a quick example to set the stage for what comes next.

### Example: Code Review Agent

```md
# Code Review Checklist

## Objective
Verify that code meets quality standards and is ready for integration.

## Input
- Source code or pull request diff

## Steps
1. Readability: clarity, naming, comments
2. Functionality: correctness and edge cases
3. Performance: potential bottlenecks
4. Security: common vulnerabilities
5. Testing: coverage and relevance
6. Style: adherence to project standards

## Output
- Structured review with findings and recommendations

## Checklist
- [ ] No syntax or logical errors
- [ ] Performance concerns identified
- [ ] Security issues flagged
- [ ] Tests reviewed
- [ ] Style guidelines followed
```

This agent does one thing: review code. It doesn't plan features, write tests, or update documentation. That focus is what makes it reliable — and what makes it composable into larger workflows.

---

## Multi-Step Workflows

Multi-step workflows are used when a task cannot be solved reliably by a single agent. Instead, multiple agents work in sequence, where each step produces input for the next one.

### Orchestration Models

There are two fundamental ways to orchestrate a workflow:

#### Agent-Orchestrated

A master agent calls other agents automatically:
- Runs in a single context window (in most tools)
- No human review between steps
- Errors compound without intervention
- Harder to debug when things go wrong

#### Human-Orchestrated

A human controls the flow, invoking agents step by step:
- A master agent guides the sequence with human validation
- Results are reviewed between steps
- Errors are caught early
- Higher overall success rate

### The Cumulative Error Problem

The main risk with multi-step workflows is **cumulative error**. Even small inaccuracies compound across steps.

If each step has an accuracy of 0.8, the overall success rate drops quickly:

```text
Step accuracy = 0.8

After 5 steps:
0.8 x 0.8 x 0.8 x 0.8 x 0.8 = 0.33
```

A workflow with five 80%-accurate steps succeeds only one-third of the time without human intervention. This is why **human-in-the-loop validation is critical**, especially for complex or high-impact tasks.

### Best Practices for Multi-Step Workflows

- **Keep each agent narrowly scoped** — one clear responsibility per step
- **Use shared state files** for project rules, input/output templates, and workflow state
- **Insert human approval checkpoints** at critical decision points
- **Use code execution for deterministic logic** — parsing, calculations, and transformations should run as code, not as LLM prompts. This improves stability and reduces token usage
- **Persist intermediate results** — don't rely on conversation history for important outputs

Multi-step workflows trade speed for reliability. For complex or high-impact tasks, human orchestration is the safer default.

---

## Sample Workflow: Feature Implementation

To make these concepts concrete, we'll walk through a **5-step feature implementation workflow** — the same workflow implemented five different ways across Claude Code and GitHub Copilot.

The workflow contains five sequential steps that represent the basic parts of a development flow:

1. **Analyze** — understand what needs to be done
2. **Plan** — break work into phases and define changes
3. **Implement** — execute the plan with checkpoints
4. **Test** — validate the implementation
5. **Document** — record changes and decisions

### Workflow Steps Explained

#### Step 1: Analyze Requirements
- Understands what needs to be done
- Identifies affected files and dependencies
- Assesses risks and challenges

**Output:** `analysis-results.md`

#### Step 2: Create Plan
- Breaks work into phases
- Defines concrete file-level changes
- Plans the testing strategy

**Output:** `implementation-plan.md`
**Approval Gate:** must be reviewed and approved before continuing

#### Step 3: Implementation
- Executes the plan phase by phase
- Creates checkpoints between phases
- Documents deviations from the plan

**Output:** `implementation-results.md`

#### Step 4: Test and Validate
- Runs existing tests
- Adds tests for new functionality
- Validates against original requirements

**Output:** `test-results.md`

#### Step 5: Documentation
- Updates code-level documentation
- Updates README and usage guides
- Produces a workflow summary

**Output:** `workflow-summary.md`

### Key Design Features

| Feature | Purpose |
|---------|---------|
| **Context preservation** | Each step writes results to `workflow-state/`, so later steps can reuse prior outputs |
| **Checkpoints** | Git checkpoints allow rollback if a step fails or needs adjustment |
| **Approval gates** | Critical steps pause execution until explicitly approved by a human |
| **State management** | Intermediate results are persisted to files and can be reviewed or edited |
| **Iterative refinement** | Steps can be rolled back and re-run with modified inputs if needed |

### Building Workflows — Practical Guidelines

When building your own workflows, start with these basics:

- **Small agent scope, few agents** — keep each agent focused, but avoid too many handoffs
- **State files** (shared project context) — use dedicated files to store project rules, per-agent input/output templates, and current workflow state
- **Breakpoints** (human-in-the-loop) — add explicit stop points where execution continues only after human review
- **Code execution for algorithmic work** — when a task is deterministic, run code instead of prompting

---

## Claude Code Workflows

Claude Code provides several mechanisms to build workflows: **skills**, **sub-agents**, and combinations of both.

If you completed Chapter 7, you already know how skills and agents work individually. This section focuses on how to **combine them into workflows**.

> **Deprecation notice:** Earlier versions of Claude Code used **instruction files** (also called "slash commands") stored in `.claude/commands/`. These are now **deprecated** in favor of **skills** stored in `.claude/skills/`. Existing command files still work for backward compatibility, but all new workflows should use the skills system. The key differences: skills support richer metadata (description-based auto-triggering, `context: fork` for isolation, per-skill model selection), while commands were just plain prompts. If you have existing `.claude/commands/` workflows, migrating them is straightforward — move the files to `.claude/skills/<name>/SKILL.md` and add frontmatter. See Chapter 7 for the full skills reference.

### Skills vs Sub-Agents for Workflows

| Aspect | Skills (user-invocable) | Sub-Agents |
|--------|------------------------|------------|
| **Context** | Run inside the calling context (main conversation or sub-agent) | Fully isolated, own private context |
| **Execution** | Explicitly invoked by the user via `/skill-name` or auto-triggered | Triggered automatically when matched by description |
| **Purpose** | Reusable workflow steps that share conversational context | Specialized workers for well-defined, isolated tasks |
| **Overhead** | Low — just a prompt injected into the conversation | Higher — separate context initialization per agent |

**Rule of thumb:**
- Use **skills** for explicit, user-controlled workflow steps where shared context matters
- Use **sub-agents** for isolated steps where context separation is beneficial
- Use a **skill as orchestrator** + **sub-agents as workers** for the most structured approach

### Approach 1: Skill-Based Workflow

Skills (formerly called "slash commands" before the January 2025 unification) are the simplest way to implement multi-step workflows in Claude Code.

Each workflow step is a separate skill stored as a Markdown file. The user invokes them in sequence, and workflow state is persisted to files between steps. An orchestrator skill ties everything together.

> **Historical note:** Before January 2025, these were called "slash commands" and lived in `.claude/commands/`. Anthropic merged slash commands into the skills system. Old command files still work, but the recommended location is now `.claude/skills/`. Skills with `user-invocable: true` (the default) appear in the `/` menu — exactly like slash commands did. See Chapter 7 for details on the skills architecture.

#### Directory Structure

```
project/
├── .claude/
│   └── skills/
│       └── workflow/
│           ├── 00_orchestrator/
│           │   └── SKILL.md
│           ├── 01_analyze_requirements/
│           │   └── SKILL.md
│           ├── 02_create_plan/
│           │   └── SKILL.md
│           ├── 03_implement/
│           │   └── SKILL.md
│           ├── 04_test_validate/
│           │   └── SKILL.md
│           └── 05_document/
│               └── SKILL.md
└── workflow-state/
    ├── analysis-results.md
    ├── implementation-plan.md
    ├── implementation-results.md
    ├── test-results.md
    └── workflow-summary.md
```

#### Orchestrator Skill

The orchestrator is the entry point. It describes the full workflow sequence and tells the agent how to invoke each step.

```md
---
name: workflow-orchestrator
description: Orchestrates a complete multi-step development workflow from analysis through documentation
argument-hint: "[detailed task description]"
---

# Workflow Orchestrator

## Overview
This skill coordinates a complete development workflow with five sequential steps,
from initial analysis to final documentation.

## Workflow Sequence

1. Analyze — gather requirements and assess the current state
2. Plan — produce a detailed implementation plan
3. Implement — execute the plan with checkpoints
4. Test — verify the implementation meets requirements
5. Document — record all changes and decisions

## Step Execution

### Step 1: Analysis
- Run the `/01-analyze-requirements` skill with the user's task description
- Wait for analysis to finish
- Summarize key findings from workflow-state/analysis-results.md

### Step 2: Planning
- Run the `/02-create-plan` skill
- Present the implementation plan to the user
- APPROVAL GATE: Do not proceed until the user explicitly approves

### Step 3: Implementation
- Create a git checkpoint tagged "pre-implementation"
- After receiving user approval, run the `/03-implement` skill
- Create a checkpoint after each completed phase
- Summarize implementation progress

### Step 4: Testing
- Run the `/04-test-validate` skill
- Report test results to the user
- If tests fail, ask whether to fix issues or roll back

### Step 5: Documentation
- Run the `/05-document` skill
- Present the final workflow summary
- Mark the workflow as complete

## Rules
1. Complete each step fully before moving to the next
2. Always save intermediate results to workflow-state/
3. Create git checkpoints before and after major changes
4. Reference outputs from previous steps explicitly
5. Stop and wait for user approval at marked gates
6. If a step fails, stop and ask the user how to proceed

## State Directory
All intermediate artifacts are stored in workflow-state/:
- analysis-results.md — requirements and impact analysis
- implementation-plan.md — detailed implementation plan
- implementation-results.md — what was actually implemented
- test-results.md — testing outcomes
- workflow-summary.md — final summary and documentation

## Usage
Invoke with: /workflow-orchestrator [detailed task description]

Example: /workflow-orchestrator Add user authentication with JWT tokens
```

#### Step 1: Analyze Requirements

```md
---
name: 01-analyze-requirements
description: Analyze project requirements and codebase state to determine what needs to be built or changed
argument-hint: "[description of task]"
---

# Step 1: Analyze Requirements

## Goal
Examine the project requirements and current codebase to build a clear picture
of what needs to happen, what's affected, and what could go wrong.

## What You Need
- Project documentation (if available)
- Access to the current codebase
- The user's feature request or requirement description

## Process
1. Read through relevant documentation and project files
2. Explore the existing codebase structure and conventions
3. Identify which files and components will be affected
4. Map out dependencies and constraints
5. Flag potential risks or open questions

## Verification
- [ ] Requirements are clearly understood
- [ ] Affected files and components are identified
- [ ] Dependencies are mapped
- [ ] Risks are documented
- [ ] Any open questions are noted

## Output
Write workflow-state/analysis-results.md containing:
- A summary of what needs to be done
- List of files to modify or create, with reasons
- Dependency analysis
- Risk assessment
- Open questions that need user input (if any)

## What Happens Next
After analysis is complete, the orchestrator will move to Step 2 (Planning),
or pause to address open questions first.
```

The remaining step skills (02 through 05) follow the same pattern. Full files are included in the `sample-workflows/` directory alongside this chapter.

### Approach 2: Agent-Based Workflow

For workflows where **context isolation matters**, Claude Code sub-agents are the better choice. Each step runs in its own isolated context, receives focused input, and returns only a final summary.

The orchestrator remains a skill (invoked explicitly by the user), but it delegates each step to a dedicated sub-agent.

> **Important:** Sub-agents cannot call other sub-agents. Workflow orchestration must stay in the main conversation — typically in a skill. Sub-agents handle the individual steps. For complex parallel work requiring inter-agent communication, use **Agent Teams** (experimental) — where a lead coordinates independent teammates that can communicate directly with each other and self-claim tasks from a shared list.

#### Why Use Sub-Agents

- The main conversation stays clean and focused on workflow control
- Each step runs with a fresh, task-specific context
- Steps can run in parallel when they don't depend on each other
- Per-step configuration (tools, model) allows fine-grained optimization

#### Trade-Offs

- Limited interactivity during execution — the agent works silently until done
- Each sub-agent call has additional context and token overhead
- Conversational or resumable sub-agents are not practical today

#### Directory Structure

```
project/
├── .claude/
│   ├── agents/
│   │   ├── analyze-requirements.md
│   │   ├── create-plan.md
│   │   ├── implement.md
│   │   ├── test-validate.md
│   │   └── document.md
│   └── skills/
│       └── workflow/
│           └── orchestrator/
│               └── SKILL.md
└── workflow-state/
    ├── analysis-results.md
    ├── implementation-plan.md
    ├── implementation-results.md
    ├── test-results.md
    └── workflow-summary.md
```

#### Orchestrator Skill (Agent-Based)

Notice how the orchestrator references sub-agents by name using the Agent tool, instead of invoking skills:

```md
---
name: workflow-orchestrator
description: Orchestrates a complete development workflow by delegating steps to specialized sub-agents
argument-hint: "[detailed task description]"
---

# Workflow Orchestrator

## Overview
This skill coordinates a full development workflow by dispatching each step
to a specialized sub-agent. Each agent works in isolation and writes results
to shared state files.

## Workflow Sequence

1. Analyze — understand requirements and current state
2. Plan — create a detailed implementation plan
3. Implement — execute the plan with checkpoints
4. Test — validate the implementation
5. Document — complete all documentation

## Step Execution

### Step 1: Analysis
- Dispatch the Agent tool with subagent_type: "analyze-requirements", passing the user's task description
- Wait for the agent to complete
- Summarize key findings from workflow-state/analysis-results.md

### Step 2: Planning
- Dispatch the Agent tool with subagent_type: "create-plan"
- Present the implementation plan to the user
- APPROVAL GATE: Do not proceed until the user explicitly approves

### Step 3: Implementation
- Create a git checkpoint tagged "pre-implementation"
- After receiving approval, dispatch the Agent tool with subagent_type: "implement"
- Create a checkpoint after each completed phase
- Summarize implementation progress

### Step 4: Testing
- Dispatch the Agent tool with subagent_type: "test-validate"
- Report test results to the user
- If tests fail, ask whether to fix issues or roll back

### Step 5: Documentation
- Dispatch the Agent tool with subagent_type: "document"
- Present the final workflow summary
- Mark the workflow as complete

## Rules
1. Complete each step fully before moving to the next
2. Always save intermediate results to workflow-state/
3. Create git checkpoints before and after major changes
4. Reference outputs from previous steps explicitly
5. Stop and wait for user approval at marked gates
6. If a step fails, stop and ask the user how to proceed

## State Directory
All intermediate artifacts are stored in workflow-state/:
- analysis-results.md — requirements and impact analysis
- implementation-plan.md — detailed implementation plan
- implementation-results.md — what was actually implemented
- test-results.md — testing outcomes
- workflow-summary.md — final summary and documentation

## Usage
Invoke with: /workflow-orchestrator [detailed task description]

Example: /workflow-orchestrator Add user authentication with JWT tokens
```

#### Example Sub-Agent: Analyze Requirements

```md
---
name: analyze-requirements
description: Examines project requirements and codebase state to determine what needs to be built. Explores project structure, identifies affected areas, maps dependencies, assesses risks, and writes a comprehensive analysis to guide the planning phase.
tools: Bash, Glob, Grep, Read, Write
model: sonnet
---

# Agent: Analyze Requirements

## Goal
Examine the project requirements and current codebase to build a clear picture
of what needs to happen, what's affected, and what could go wrong.

## What You Need
- Project documentation (if available)
- Access to the current codebase
- The user's feature request or requirement description

## Process
1. Read through relevant documentation and project files
2. Explore the existing codebase structure and conventions
3. Identify which files and components will be affected
4. Map out dependencies and constraints
5. Flag potential risks or open questions

## Verification
- [ ] Requirements are clearly understood
- [ ] Affected files and components are identified
- [ ] Dependencies are mapped
- [ ] Risks are documented
- [ ] Any open questions are noted

## Output
Write workflow-state/analysis-results.md containing:
- A summary of what needs to be done
- List of files to modify or create, with reasons
- Dependency analysis
- Risk assessment
- Open questions that need user input (if any)
```

The remaining agents (create-plan, implement, test-validate, document) follow the same structure. Full files are in the `sample-workflows/` directory.

#### Sub-Agent Configuration Reference

Sub-agents are configured through YAML frontmatter. For the full field reference, see Chapter 7. The key fields for workflow agents are:

| Field | Why it matters for workflows |
|-------|------------------------------|
| `name` | How the orchestrator references this agent |
| `description` | Tells the LLM when to delegate to this agent |
| `tools` | Restricts what the agent can do — good for safety and context management |
| `model` | Use a faster model (e.g. `sonnet`) for simpler steps to save cost |

### Parallel Execution and Background Agents

Claude Code supports running sub-agents in **foreground** (blocking) or **background** (asynchronous) mode. Both still use isolated contexts, but background execution lets you continue working while the agent runs.

#### Foreground Sub-Agents
The main conversation waits until the sub-agent finishes. Permission prompts and clarifying questions can be handled interactively.

#### Background Sub-Agents
You can send a running sub-agent to the background with **Ctrl+B** or by asking Claude to "run this in the background."

- The agent runs asynchronously while you continue working
- When complete, it notifies the main conversation with results
- Before launching, Claude Code requests all needed tool permissions up front so the agent won't block later
- If the agent encounters a question it can't ask, the tool call fails and the agent continues
- Some tools (like MCP) are not available in background mode

You can list running background agents with `/tasks`.

#### Practical Limitations
- Background agents can't prompt interactively for permissions mid-run — missing permissions cause tool calls to fail
- Some tools (like MCP) are unavailable in background mode
- Background tasks have reduced interactivity compared to foreground runs

#### When to Use Background Agents
- **Exploration and research** — start background agents for large code searches while you work on other parts
- **Aggregated investigations** — spawn multiple background sub-agents to explore independent parts of the codebase, then gather their summaries

Background sub-agents approximate asynchronous execution and improve workflow throughput without blocking your main session.

### Choosing Between Skills and Sub-Agents

There is no universal best choice. The right approach depends on the workflow:

**Use skills when you need shared context:**
If multiple steps must see the same evolving context — design decisions, constraints, partial code — keep them in the main conversation and orchestrate with skills.

**Use sub-agents when you need separation:**
When steps should not influence each other, use sub-agents with isolated contexts.

**Good fit for sub-agents — parallel exploration:**
- An orchestrator starts multiple sub-agents in parallel
- One analyzes security, one reviews best practices, one checks performance
- Each explores a different area in isolation and returns a summary
- The orchestrator aggregates results into a single report

**Good fit for skills — coding workflows:**
For implementation-heavy workflows (plan, code, test, refine):
- Steps often benefit from full shared context
- Earlier decisions matter deeply for later steps
- A skill-based workflow may be more reliable than isolated agents

**Rule of thumb:** Experiment early and adapt the architecture to the workflow, not the other way around. The implementations are similar enough that switching between them is straightforward.

---

## Where Instructions Live — Context and Message Placement

Understanding *where* your prompts end up in the message hierarchy is critical for building reliable workflows. This section explains the practical mechanics.

### Message Placement by Type

| Item | Where it is placed | What it's used for |
|------|-------------------|-------------------|
| **System prompt** | System message | Global rules, safety, tool access, baseline behavior. Set by the framework. |
| **CLAUDE.md** | `<system-reminder>` annotation on user message | Project conventions, coding standards, repo-specific guidance |
| **Skills** | User message (when invoked) + `<system-reminder>` annotation for discovery | Procedural "how-to" instructions for a task |
| **Sub-agents** | System message (at sub-agent startup) | Behavioral persona, boundaries, delegated responsibility |

### Comparison

| Feature | Skills | Sub-Agents |
|---------|--------|------------|
| **Primary location** | User message (on invocation) | System message (at startup) |
| **Metadata** | `<system-reminder>` annotation on user messages for discovery | Loaded in system prompt as identity |
| **Instruction type** | Procedural task instructions | Behavioral role + boundaries |
| **Persistence** | Loaded on-demand, stays in conversation history | Foundation for the entire isolated session |

**Important note on CLAUDE.md:** A project's CLAUDE.md is injected as a `<system-reminder>` annotation on a **user message** — it is not part of the system prompt itself. The agent is instructed to treat these annotations as authoritative, but they live in the conversation flow and can be compacted (though they are re-injected periodically).

### Why This Matters for Workflows

#### System vs Conversation Placement

**Sub-agents:**
Their prompt is injected into the **system message** of the sub-agent. This means:
- It is always present for the entire sub-agent execution
- It does not get pushed out by conversation growth inside that sub-agent
- It still counts toward the context window, but it is not dropped selectively

**Skills / CLAUDE.md:**
These are injected as **user messages**. This means:
- They live in the conversation history
- If the context window fills up, **older user messages can be truncated**
- Important project rules or instructions may silently disappear

System-level instructions are more stable than conversation-level ones.

**Practical advice:**
- Put non-negotiable behavior and boundaries in agent system prompts
- Keep CLAUDE.md concise and avoid repeating large instructions every turn
- Persist critical outputs to files instead of relying on chat history

### Context Degradation

Even if a model supports 200k tokens, real-world behavior often degrades earlier (around 50-60k tokens):

- Attention becomes diffuse
- Earlier instructions are followed less reliably
- Long chains of intermediate reasoning pollute context
- Small inconsistencies accumulate

This is usually a **gradual degradation**, not a hard failure.

**Practical advice:**
- Treat the effective context limit as lower than the advertised maximum
- Periodically summarize or externalize state (files, workflow-state/)
- Use sub-agents to keep the main thread short and clean
- Avoid letting orchestration logic and implementation details mix in one context

### Common Pitfalls

- **Instruction duplication** — repeating the same rules in system prompt, CLAUDE.md, and skills can cause conflicts
- **Hidden context loss** — when a step "suddenly forgets" rules, it is often due to silent truncation
- **Overusing sub-agents** — each sub-agent has startup overhead (tools, skills, system prompt). Use them where isolation genuinely helps
- **Assuming resumability** — resumable or conversational sub-agents are not reliable today

### Rule of Thumb

- System message = identity, role, hard constraints
- Conversation = transient interaction
- Files = durable memory

If something must not be forgotten, don't leave it only in the chat.

---

## GitHub Copilot Workflows

The same workflow concepts apply to GitHub Copilot, with different mechanics. If you've read the Claude Code sections above, the core ideas are already familiar. This section focuses on the Copilot-specific implementation details.

### Prompt Files vs Custom Agents

GitHub Copilot provides two main mechanisms for building workflows: **prompt files** and **custom agents**.

They map closely to Claude Code concepts:
- **Prompt files** = user-invocable skills (shared context, user-triggered)
- **Custom agents** = sub-agents (role-based, system-prompt stability)

| Feature | Prompt Files | Custom Agents |
|---------|-------------|---------------|
| Invocation | `/prompt-name` in chat | Selected from Copilot Chat dropdown |
| Prompt placement | User-level prompt | System prompt |
| Purpose | Task-specific, reusable prompts | Role-based assistants |
| Isolation | Shared conversation context | Agent-scoped behavior |

**Key difference:**
Prompt files are sent as **user messages**, while custom agents are injected into the **system prompt**, making agents more stable for long sessions. (The same system-vs-conversation dynamic described in the Claude Code section above.)

### Prompt File Metadata

| Field | Description |
|-------|------------|
| `description` | Short explanation of the prompt's purpose |
| `name` | Prompt name used in chat (defaults to filename) |
| `argument-hint` | Hint shown in chat for expected arguments |
| `agent` | Agent to run the prompt (`ask`, `edit`, `agent`, or custom) |
| `model` | Model to use for this prompt |
| `tools` | Allowed tools or tool sets |

### Important Observations and Limitations

- **No prompt chaining by name** — saying `run /other-prompt` inside a prompt does not work. You must reference files explicitly: `continue with instructions in #file:path/to/prompt.md`
- **Metadata applies only on manual invocation** — when a prompt is executed indirectly (e.g. from an orchestrator), it inherits the orchestrator's configuration, not its own

These limitations affect how reliably metadata can be used for automated orchestration.

### Approach 3: Prompt-Based Workflow (Copilot)

This uses prompt files as workflow steps — structurally similar to the Claude Code skill-based approach.

#### Directory Structure

```
project/
├── .github/
│   └── prompts/
│       ├── 00_orchestrator.prompt.md
│       ├── 01_analyze_requirements.prompt.md
│       ├── 02_create_plan.prompt.md
│       ├── 03_implement.prompt.md
│       ├── 04_test_validate.prompt.md
│       └── 05_document.prompt.md
└── workflow-state/
    ├── analysis-results.md
    ├── implementation-plan.md
    ├── implementation-results.md
    ├── test-results.md
    └── workflow-summary.md
```

#### Orchestrator

Note the key difference from Claude Code: prompts are referenced with `#file:` syntax instead of skill names.

```md
---
name: orchestrator
description: Orchestrates a complete multi-step development workflow from analysis to documentation
argument-hint: "[detailed task description]"
---

# Workflow Orchestrator

## Overview
This prompt coordinates a complete development workflow with five sequential steps,
from initial analysis to final documentation.

## Workflow Sequence

1. Analyze — gather requirements and assess the current state
2. Plan — produce a detailed implementation plan
3. Implement — execute the plan with checkpoints
4. Test — verify the implementation meets requirements
5. Document — record all changes and decisions

## Step Execution

### Step 1: Analysis
- Follow instructions from #file:./01_analyze_requirements.prompt.md using the user's task description
- Wait for analysis to finish
- Summarize key findings from workflow-state/analysis-results.md

### Step 2: Planning
- Follow instructions from #file:./02_create_plan.prompt.md
- Present the implementation plan to the user
- APPROVAL GATE: Do not proceed until the user explicitly approves

### Step 3: Implementation
- Create a checkpoint tagged "pre-implementation"
- Follow instructions from #file:./03_implement.prompt.md
- Create a checkpoint after each completed phase
- Summarize implementation progress

### Step 4: Testing
- Follow instructions from #file:./04_test_validate.prompt.md
- Report test results to the user
- If tests fail, ask whether to fix issues or roll back

### Step 5: Documentation
- Follow instructions from #file:./05_document.prompt.md
- Present the final workflow summary
- Mark the workflow as complete

## Rules
1. Complete each step fully before moving to the next
2. Always save intermediate results to workflow-state/
3. Create checkpoints before and after major changes
4. Reference outputs from previous steps explicitly
5. Stop and wait for user approval at marked gates
6. If a step fails, stop and ask the user how to proceed

## State Directory
All intermediate artifacts are stored in workflow-state/:
- analysis-results.md — requirements and impact analysis
- implementation-plan.md — detailed implementation plan
- implementation-results.md — what was actually implemented
- test-results.md — testing outcomes
- workflow-summary.md — final summary and documentation
```

Step prompts 01-05 are structurally identical to the Claude Code skill versions. Full files are provided in the `sample-workflows/` directory.

### Approach 4: Agent-Based Workflow (Copilot)

GitHub Copilot supports **custom agents** for building role-based workflows with stronger structure and isolation than prompt files. Custom agents are stored under `.github/agents/` and selected from the Copilot Chat dropdown.

#### What Custom Agents Do Well

- Represent specialized roles (reviewer, planner, implementer)
- Define stable behavior via system-level prompts
- Fine-tune execution per step (model, tools, permissions)
- Support manual orchestration via **handoffs**

#### Custom Agent Configuration

| Field | Description |
|-------|------------|
| `name` | Agent name. Defaults to filename. |
| `description` | Brief description, shown in chat placeholder. |
| `argument-hint` | Hint text for user interaction. |
| `tools` | Available tools or tool sets (built-in, MCP, or extensions). |
| `model` | AI model to use. |
| `target` | Target environment (e.g. `vscode`, `github-copilot`). |
| `mcp-servers` | Optional MCP servers and tools (primarily for GitHub integrations). |
| `handoffs` | Optional list of sequential handoffs to other agents. |
| `handoffs.label` | Label shown on the handoff button. |
| `handoffs.agent` | Target agent to switch to. |
| `handoffs.prompt` | Optional prompt sent to the target agent during handoff. |
| `handoffs.send` | Whether to auto-submit the prompt on handoff (default: `false`). |

#### Automated Orchestration (Experimental)

GitHub Copilot also exposes an experimental tool `#runSubAgent`:
- Runs a custom agent in an isolated context
- Similar in concept to Claude Code sub-agents
- Requires explicit enablement
- Execution details are not always visible in the UI

By default, a sub-agent inherits the agent from the main session. You can configure a sub-agent to use a different agent. This differs from Claude Code, where agents are isolated by default.

#### Operational Differences

| Feature | Standard Agent Mode | `#runSubAgent` |
|---------|-------------------|----------------|
| **Workspace** | Operates in the active workspace | Often uses a separate Git worktree |
| **Visibility** | All steps visible in main chat | Only final results returned |
| **Best for** | Iterative feature development | Focused research or discrete background tasks |

#### Directory Structure

```
project/
├── .github/
│   └── agents/
│       ├── 00_orchestrator.md
│       ├── 01_analyze_requirements.md
│       ├── 02_create_plan.md
│       ├── 03_implement.md
│       ├── 04_test_validate.md
│       └── 05_document.md
└── workflow-state/
    ├── analysis-results.md
    ├── implementation-plan.md
    ├── implementation-results.md
    ├── test-results.md
    └── workflow-summary.md
```

#### Orchestrator Agent

```md
---
name: orchestrator
description: Orchestrates a complete multi-step development workflow from analysis to documentation
tools: ['runSubagent']
---

# Workflow Orchestrator

## Overview
This agent coordinates a complete development workflow by dispatching each step
to a specialized sub-agent.

## Workflow Sequence

1. Analyze — gather requirements and assess the current state
2. Plan — produce a detailed implementation plan
3. Implement — execute the plan with checkpoints
4. Test — verify the implementation meets requirements
5. Document — record all changes and decisions

## Step Execution

### Step 1: Analysis
- Run `#runSubagent analyze-requirements` with the user's task description
- Wait for analysis to complete
- Summarize key findings from workflow-state/analysis-results.md

### Step 2: Planning
- Run `#runSubagent create-plan`
- Present the implementation plan to the user
- APPROVAL GATE: Wait for explicit user approval before continuing

### Step 3: Implementation
- Create a checkpoint tagged "pre-implementation"
- Run `#runSubagent implement`
- After each phase, create a checkpoint and summarize progress

### Step 4: Testing
- Run `#runSubagent test-validate`
- Review and summarize test results

### Step 5: Documentation
- Run `#runSubagent document`
- Produce the final workflow summary

## Rules

- **Sequential execution** — complete each step fully before moving to the next
- **State preservation** — always save intermediate results to workflow-state/
- **Checkpoints** — create checkpoints before and after major changes
- **Explicit context** — reference outputs from previous steps explicitly
- **Approval gates** — stop and wait for user approval at critical points
- **Error handling** — if a step fails, stop and ask the user how to proceed

## State Directory
All intermediate artifacts are stored in workflow-state/:
- analysis-results.md — requirements and impact analysis
- implementation-plan.md — detailed implementation plan
- implementation-results.md — what was actually implemented
- test-results.md — testing outcomes
- workflow-summary.md — final summary and documentation
```

#### Example Sub-Agent: Analyze Requirements

Note how Copilot agents include **handoffs** — UI buttons that let the user manually transition to the next agent:

```md
---
name: analyze-requirements
description: Analyzes project requirements and codebase state to determine what needs to be built
tools: ['edit/createFile', 'edit/createDirectory', 'edit/editFiles', 'search', 'usages']
handoffs:
  - label: Create Implementation Plan
    agent: create-plan
    prompt: Create an implementation plan based on the analysis results.
    send: false
---

# Step 1: Analyze Requirements

You are a requirements analysis specialist. Your job is to understand what needs
to be done for a given task by examining the project and its codebase.

## Your Role
Examine the project requirements and current codebase state to build a clear
picture of what needs to happen.

## What You Need
- Project documentation (if available)
- Current codebase structure
- The user's feature request or requirement description

## Your Process
1. Read through relevant documentation and project files
2. Explore the existing codebase structure and conventions
3. Identify which files and components will be affected
4. Map out dependencies and constraints
5. Flag potential risks or open questions

## Verification
Confirm you have addressed:
- [ ] Requirements are clearly understood
- [ ] Affected files and components are identified
- [ ] Dependencies are mapped
- [ ] Risks are documented
- [ ] Open questions are noted

## Your Output
Write workflow-state/analysis-results.md containing:
- Summary of requirements — clear statement of what needs to be done
- Files to modify or create — specific paths and reasons
- Dependency analysis — what the changes depend on
- Risk assessment — potential issues or challenges
- Open questions — anything that needs user input

## Guidelines
- Be thorough but concise
- Focus on facts, not assumptions
- Identify information gaps early
- Document technical constraints
- Consider backward compatibility
- Think about testing requirements
```

The remaining agents (02-05) follow the same pattern with appropriate handoff configurations. Full files are in the `sample-workflows/` directory.

### Copilot Trade-Offs

**Pros:**
- Strong role separation through system-prompt agents
- Clear manual handoffs between steps
- Fine-grained per-agent configuration

**Cons:**
- Automated orchestration (`#runSubAgent`) is still experimental
- Parallel execution semantics are unclear
- Debugging multi-agent flows requires extra effort

### Practical Guidance

- Use **custom agents** for role-based or review-heavy workflows
- Use **handoffs** when humans should stay in control of transitions
- Treat automated agent chaining as experimental
- Prefer prompt files for simple, shared-context workflows

### Approach 5: Skill-Based Workflow (Copilot)

GitHub Copilot also supports **skills**, structurally very similar to Claude Code skills:
- Each skill lives in its own folder under `.github/skills/` with a `skill.md` entry point
- The folder can also contain scripts, templates, and helper files
- Skills are suited for reusable capabilities — both deterministic actions and procedural instructions
- Users invoke skills via `/skill-name` in Copilot Chat

Skills in Copilot work the same way as in Claude Code conceptually: they inject instructions into the conversation context when invoked. The structural pattern (folder + entry point markdown + optional supporting files) is identical.

#### Directory Structure

```
project/
├── .github/
│   └── skills/
│       ├── workflow-orchestrator/
│       │   └── skill.md
│       ├── analyze-requirements/
│       │   └── skill.md
│       ├── create-plan/
│       │   └── skill.md
│       ├── implement/
│       │   └── skill.md
│       ├── test-validate/
│       │   └── skill.md
│       └── document/
│           └── skill.md
└── workflow-state/
    ├── analysis-results.md
    ├── implementation-plan.md
    ├── implementation-results.md
    ├── test-results.md
    └── workflow-summary.md
```

#### Orchestrator Skill

The orchestrator follows the same pattern as the Claude Code skill-based workflow. The main difference is the file location (`.github/skills/` instead of `.claude/skills/`):

```md
---
name: workflow-orchestrator
description: Orchestrates a complete multi-step development workflow from analysis through documentation
argument-hint: "[detailed task description]"
---

# Workflow Orchestrator

## Overview
This skill coordinates a complete development workflow with five sequential steps,
from initial analysis to final documentation.

## Workflow Sequence

1. Analyze — gather requirements and assess the current state
2. Plan — produce a detailed implementation plan
3. Implement — execute the plan with checkpoints
4. Test — verify the implementation meets requirements
5. Document — record all changes and decisions

## Step Execution

### Step 1: Analysis
- Run the `/analyze-requirements` skill with the user's task description
- Wait for analysis to finish
- Summarize key findings from workflow-state/analysis-results.md

### Step 2: Planning
- Run the `/create-plan` skill
- Present the implementation plan to the user
- APPROVAL GATE: Do not proceed until the user explicitly approves

### Step 3: Implementation
- Create a git checkpoint tagged "pre-implementation"
- After receiving user approval, run the `/implement` skill
- Create a checkpoint after each completed phase
- Summarize implementation progress

### Step 4: Testing
- Run the `/test-validate` skill
- Report test results to the user
- If tests fail, ask whether to fix issues or roll back

### Step 5: Documentation
- Run the `/document` skill
- Present the final workflow summary
- Mark the workflow as complete

## Rules
1. Complete each step fully before moving to the next
2. Always save intermediate results to workflow-state/
3. Create git checkpoints before and after major changes
4. Reference outputs from previous steps explicitly
5. Stop and wait for user approval at marked gates
6. If a step fails, stop and ask the user how to proceed

## State Directory
All intermediate artifacts are stored in workflow-state/:
- analysis-results.md — requirements and impact analysis
- implementation-plan.md — detailed implementation plan
- implementation-results.md — what was actually implemented
- test-results.md — testing outcomes
- workflow-summary.md — final summary and documentation
```

Step skills 01-05 are structurally identical to the Claude Code skill versions — the only difference is the file location and naming convention (`skill.md` instead of `SKILL.md`). Full files are provided in the `sample-workflows/` directory.

### Choosing Between Prompt Files, Skills, and Agents (Copilot)

Copilot now offers three mechanisms for workflow steps, paralleling the evolution in Claude Code:

| Mechanism | Best for | Context | Invocation |
|-----------|----------|---------|------------|
| **Prompt files** | Simple, explicit workflow steps | Shared conversation | `/prompt-name` |
| **Skills** | Reusable capabilities with supporting files | Shared conversation | `/skill-name` or auto-triggered |
| **Custom agents** | Role-based steps needing system-prompt stability | Agent-scoped | Dropdown or `#runSubAgent` |

**When to use which:**
- **Prompt files** — quick and simple. Good for lightweight workflows where each step is a single markdown file with no supporting assets.
- **Skills** — more structured. Good when steps need supporting scripts, templates, or helper files bundled together. The folder structure keeps things organized.
- **Custom agents** — strongest isolation. Good for long-running or complex steps where system-prompt stability matters, or when you want manual handoff buttons between steps.

In practice, skills and prompt files behave similarly for workflow purposes. The main advantage of skills is the folder structure — you can bundle scripts, templates, and configuration alongside the skill definition. For pure prompt-based workflows, prompt files are simpler.

> **Heads up:** Claude Code already deprecated its equivalent of prompt files (instruction files / slash commands in `.claude/commands/`) in favor of skills. Given that Copilot skills offer a strict superset of prompt file functionality — same invocation model, plus folder structure, bundled assets, and richer metadata — it's reasonable to expect prompt files may follow the same deprecation path. If you're starting fresh, **build on skills rather than prompt files** to avoid a future migration.

---

## Recommendations

### Single-Responsibility Agents
**(recommended for practical project use)**

- Use agents for **repetitive, well-defined tasks** with stable patterns (code reviews, refactoring, test generation)
- Document agents clearly and share them across the team
- Actively maintain agents so output quality improves over time
- Treat agents as long-lived assets, not one-off prompts

### Multi-Agent Workflows
**(recommended to experiment with carefully)**

At the current level of GenAI maturity, workflow success needs active risk management:

- **Prefer human orchestration over agent orchestration** — humans should control flow and transitions
- **Validate intermediate results** — human review is mandatory, even when reviewing machine-generated artifacts feels tedious
- **Keep context focused** — pass only what the next step needs; isolate steps when possible
- **Balance scope vs number of steps** — narrow agent focus increases per-step success, but more steps reduce overall success rate
- **Measure and adapt** — monitor real success rates and adjust workflow design accordingly
- **Expect operational friction** — tooling UIs rarely guide complex workflows well, and many automation features are still experimental

### Start Small

- Adopt single-responsibility agents first
- Add workflows incrementally
- Evolve designs based on real usage, not theory

Agents and workflows are powerful, but only when combined with **human judgment and discipline**.

---

## Related Frameworks

Several community frameworks explore spec-driven, multi-step AI workflows with strong emphasis on structure, memory, and human review:

- **Spec-kit** — spec-driven development framework that guides AI through spec, plan, and implement steps. Uses memory files for project rules, templates per step, and explicit breakpoints for human review.
  https://github.com/github/spec-kit

- **OpenSpec** — similar multi-step approach focused on updating existing codebases. Separates current state and proposed changes using folders, memory files, and templates for each stage.
  https://github.com/epicweb-dev/open-spec

- **BMAD** — defines specialized AI agents that work in planned steps with shared memory. Uses templates and custom tools to decompose complex tasks into manageable workflow stages.
  https://github.com/bmad-code-org/BMAD-METHOD

**Common theme:** all three reinforce the same ideas covered in this chapter — structured workflows, durable memory, narrow agent responsibilities, and human-in-the-loop validation.

---

## Resources

- Claude Code: Sub-agents — https://code.claude.com/docs/en/sub-agents
- Claude Code: Background sub-agents — https://code.claude.com/docs/en/sub-agents#run-subagents-in-foreground-or-background
- Claude Code: Skills — https://code.claude.com/docs/en/skills
- Claude Code: Checkpointing — https://code.claude.com/docs/en/checkpointing
- Single-responsibility agents (EPAM) — https://www.epam.com/insights/ai/blogs/single-responsibility-agents
- GitHub Copilot: Agent skills — https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- Anthropic skills repository — https://github.com/anthropics/skills
- Awesome Copilot — https://github.com/github/awesome-copilot
