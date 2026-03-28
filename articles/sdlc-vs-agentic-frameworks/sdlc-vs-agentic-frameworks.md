# Every Agent Framework Is Just SDLC in Disguise

Pick any agentic coding framework. Strip away the branding, the agent names, the YAML configs. What's left? Requirements. Design. Implementation. Review. Testing. The same phases developers have followed since the 1960s.

This isn't a criticism. It's a pattern. Every framework — from a bare Claude Code session to a full BMAD deployment with six specialized agents — reimplements the software development lifecycle. The only variable is **ceremony**: how much structure wraps each phase.

This article compares five agentic coding approaches across the SDLC spectrum. The thesis is simple: for most teams, especially experienced ones working in existing codebases, the lightweight defaults built into CLI agents are enough. You don't need a Product Manager agent, an Architect agent, and a Scrum Master agent to build a feature. You need a plan and an agent that can code.

---

## The Frameworks

Before we map them to SDLC phases, here's what we're comparing:

| Framework | What It Is | Model | License |
|---|---|---|---|
| **Claude Code** | Anthropic's CLI agent | Claude only | Proprietary |
| **GitHub Copilot CLI** | GitHub/Microsoft's CLI agent | GPT-4o, Claude, Gemini | Proprietary |
| **OpenCode** | Open-source CLI agent | 75+ providers, local models via Ollama | MIT |
| **OpenSpec** | Spec-driven overlay that works with any CLI agent | Tool-agnostic | MIT |
| **BMAD** | Full-ceremony agile framework with specialized agents | Tool-agnostic | Open source |

The first three are **CLI agents** — tools you run in the terminal that read, write, and execute code. They come with sensible defaults: a planning mode, an implementation agent, and some form of review.

OpenSpec and BMAD sit **on top** of CLI agents. They don't replace Claude Code or Copilot — they add structure around them. OpenSpec adds a lightweight spec layer. BMAD adds an entire agile methodology with dedicated agent personas.

---

## The SDLC Mapping

Here's the core claim: every framework covers the same phases. The table below maps each SDLC phase to its equivalent in each framework.

| SDLC Phase | Claude Code | Copilot CLI | OpenCode | OpenSpec | BMAD |
|---|---|---|---|---|---|
| **Requirements** | Conversation + context files (`CLAUDE.md`, skills) | Conversation + context files (`copilot-instructions.md`) | Conversation + context files (rules, skills) | `/opsx:propose` — creates `proposal.md` + `specs/` | Project Brief (Analyst agent) → PRD (PM agent) |
| **Design** | `/plan` command (extended thinking) | `/plan` command | Dedicated Plan agent (`Tab` to switch, read-only) | `design.md` per change (created during propose) | Architecture doc (Architect agent) + readiness check |
| **Implementation** | Default agent (full tool access) | Default agent (full tool access) | Build agent (`Tab` to switch, full tool access) | `/opsx:apply` — delegates to any CLI agent | Developer agent (`bmad-agent-dev`) executes sprint stories |
| **Code Review** | `/review` command | `/review` command | Via conversation (no dedicated command) | `/opsx:verify` (expanded profile) | Code review skill (`bmad-code-review`) |
| **Testing** | Agent writes tests on request | Agent writes tests on request | Agent writes tests on request | Not built-in — uses underlying CLI | QA role + Test Architecture module (`bmad-agent-tea`) |
| **Completion** | Manual commit/PR | Manual commit/PR | Manual commit/PR | `/opsx:archive` — archives change, merges specs | Retrospective (`bmad-retrospective`) |
| **Project Management** | Not built-in | GitHub Issues/Projects integration | Not built-in | Change folders as lightweight tracking | Scrum Master agent + `sprint-status.yaml` + retrospectives |

Look at the pattern. Every row has coverage across all five columns. The difference isn't *what* gets done — it's *how much structure* surrounds it.

### Requirements: from a chat message to a formal PRD

In Claude Code, requirements are what you type into the prompt plus whatever context you've put in `CLAUDE.md`. That's it. Copilot and OpenCode work the same way — the developer holds the requirements in their head and communicates them through conversation.

OpenSpec formalizes this into a `proposal.md` file with a `specs/` folder containing acceptance criteria. Still lightweight, but written down.

BMAD goes full ceremony: an Analyst agent produces a Project Brief, then a PM agent turns it into a PRD with functional requirements, non-functional requirements, epics, and draft user stories.

The output of all three approaches is the same: the agent knows what to build. The question is whether that understanding lives in a chat transcript, a markdown file, or a formal document.

### Design: plan mode by any other name

Claude Code's plan mode uses extended thinking to reason about architecture before writing code. Copilot has an equivalent. OpenCode goes further — its Plan agent is a completely separate agent with read-only access, physically unable to modify files. It can only write to `.opencode/plans/*.md`.

OpenSpec captures design decisions in a `design.md` file per change. BMAD has a dedicated Architect agent that produces an architecture document and runs an implementation readiness checklist before any code is written.

Same phase. Same output. Different wrappers.

### Implementation: everyone has a default agent

This is where the frameworks converge most visibly. Claude Code, Copilot, and OpenCode all give you an agent with full access to read files, write files, run shell commands, and search code. The tool surface is nearly identical across all three.

OpenSpec doesn't implement code itself — it delegates to whatever CLI agent you're using via `/opsx:apply`. BMAD has a Developer agent, but in practice it's the same underlying LLM writing the same code.

### Review and testing: the optional phases

Claude Code and Copilot both have a dedicated `/review` command. OpenCode has no dedicated review feature; you ask it to review code through conversation.

All three can write tests when asked. None of them force you to. OpenSpec and BMAD don't add their own review or testing capabilities — they rely on the underlying CLI agent or external tools.

BMAD's QA role and Test Architecture module are the exception, but they're part of the enterprise track that most teams skip.

---

## The Ceremony Spectrum

Line up the frameworks from least to most ceremony:

| | Claude Code / Copilot / OpenCode | OpenSpec | BMAD |
|---|---|---|---|
| **Ceremony level** | Low — built-in defaults | Medium — spec layer on top | High — full agile methodology |
| **Setup time** | Zero (install and go) | `openspec init` + project.md | Multiple agent files + config + folder structure |
| **Artifacts produced** | Chat history, code, commits | proposal.md, specs/, design.md, tasks.md per change | Project Brief, PRD, Architecture doc, epics, stories, sprint-status.yaml |
| **Agents involved** | 1 (+ plan mode) | 1 (your CLI agent) | 6+ (Analyst, PM, Architect, Dev, Scrum Master, QA) |
| **Token cost per feature** | Low | Low-medium | High (each agent consumes context) |
| **Speed to first commit** | Minutes | 30+ minutes (spec first) | Hours (full workflow) |
| **Documentation output** | Minimal | Moderate (per-change specs) | Extensive (full project docs) |
| **Code control** | Direct — you see every change | Direct — specs guide but you control implementation | Indirect — agent follows stories from sprint plan |

### What you gain as ceremony increases

- **Traceability.** BMAD gives you a paper trail from requirement to story to code. Useful for audits, compliance, onboarding new team members.
- **Repeatability.** OpenSpec's propose → apply → archive cycle is the same every time. No variation between developers.
- **Role separation.** BMAD's agents can't step on each other. The Architect doesn't write code. The Developer doesn't change requirements. Boundaries are enforced.

### What you lose as ceremony increases

- **Speed.** A full BMAD workflow takes hours before the first line of code. Claude Code gets you there in minutes.
- **Code-level control.** When an agent implements stories from a sprint plan, you're one layer removed from the code. You review what the agent wrote rather than guiding it in real time.
- **Token budget.** Each BMAD agent consumes context. Six agents reasoning about the same project burns tokens fast. The CLI defaults use one agent and one context window.
- **Flexibility.** Spec-driven workflows are sequential. Change the design? Update the spec, regenerate tasks, re-apply. With defaults, you just tell the agent what changed.

---

## BMAD in Theory vs. BMAD in Practice

Here's an observation that motivated this article: I've noticed teams that say they use BMAD but in practice just run `bmad-quick-dev` — the Quick Flow track that skips the full four-phase ceremony and consolidates everything into a single streamlined workflow.

They install the framework. They see the six specialized agents, the four-phase workflow, the extensive artifact structure. And then they reach for `bmad-quick-dev`, which skips Analysis, Planning, and Solutioning entirely — producing a `spec-*.md` file plus working code in one pass.

This isn't laziness. It's rational behavior. The defaults already cover the core loop:

1. **Tell the agent what you want** (requirements)
2. **Ask it to plan** (design)
3. **Let it build** (implementation)
4. **Review the output** (code review)
5. **Ask it to write tests** (testing)

That's the SDLC. In five steps. Without a single YAML config file.

BMAD acknowledges this need — that's why `bmad-quick-dev` exists. But at that point, the question becomes: if you're skipping three of four phases, are you using BMAD or are you using plan mode with extra steps?

---

## Why Defaults Win for Most Teams

Three reasons:

**1. The plan → implement → review loop covers 80% of workflows.**

An experienced developer doesn't need an Analyst agent to brainstorm requirements. They know what they're building. They don't need an Architect agent to design the system. They've already designed it — or the system already exists and they're extending it. What they need is an agent that can execute the plan quickly and a way to review the result.

**2. The "missing" ceremony isn't missing — it's implicit.**

When you use Claude Code's plan mode, the requirements live in your prompt and `CLAUDE.md`. The design lives in the plan output. The review happens when you read the diff. The documentation lives in the commit message and PR description. None of this is formal, but it's all there.

The question isn't whether these phases happen. They always happen. The question is whether they need to be written down in separate files managed by separate agents.

**3. Premature process is as wasteful as premature abstraction.**

Adding OpenSpec or BMAD before you feel the pain is like creating an abstract factory for a class you'll only instantiate once. The ceremony has a cost — setup time, token usage, context-window pressure, cognitive overhead. That cost is worth paying when you have a specific problem (compliance requirements, team coordination issues, onboarding friction). It's wasted when the defaults work fine.

Enterprise teams — the ones you'd expect to want maximum ceremony — overwhelmingly choose the defaults. They pick Claude Code or Copilot, configure their context files, and ship. The framework choice is less about capability and more about how much pain you're currently in.

---

## The Trade-Off Nobody Talks About: Who Writes the Code?

Full spec-driven development changes your relationship with the code. With BMAD or OpenSpec's full workflow, you write specs — the agent writes code. You become a product manager who reviews pull requests rather than a developer who steers implementation.

That's a real trade-off, and you should make it consciously:

| | CLI Defaults | Full Spec-Driven (OpenSpec / BMAD) |
|---|---|---|
| **Your role** | Developer steering an agent | Spec writer reviewing agent output |
| **Code familiarity** | High — you guide every change | Low — you read what the agent produced |
| **Debugging** | You know the code because you shaped it | You need to reverse-engineer agent decisions |
| **Speed of change** | Fast — tell the agent, see the diff | Slow — update spec, regenerate tasks, re-apply |
| **Architectural control** | Direct — you decide in real time | Indirect — you hope the spec captures your intent |
| **Learning** | You learn the codebase as you go | You learn the spec format, not the code |

For experienced teams who know their codebase, this trade-off rarely makes sense. You already have the domain knowledge. You already know the architecture. You don't need an Architect agent to tell you where to put the new service — you know. What you need is an agent that can write the boilerplate, run the tests, and handle the repetitive parts while you focus on the decisions that matter.

Full spec-driven development shines when **nobody on the team knows the answer** — greenfield projects, unfamiliar domains, or teams of junior developers who benefit from the guardrails. If your team already knows what they're doing, the specs are overhead.

There is one genuine advantage spec-driven approaches have: **they survive context windows**. When you're working on something complex across many sessions, having a `design.md` and `tasks.md` that persist between conversations is genuinely useful. The agent picks up where the last session left off without you re-explaining everything. But you don't need BMAD or OpenSpec for that — a markdown file in your repo and a `CLAUDE.md` pointer do the same thing.

Ask yourself: do you want to write code with AI assistance, or do you want to write specs and let AI write the code? Neither answer is wrong. But they're very different workflows, and picking the wrong one for your team will slow you down.

---

## When to Level Up

The defaults aren't always enough. Here's when to consider adding structure:

| Your Situation | Recommendation | Why |
|---|---|---|
| Experienced team, existing codebase, fast iteration needed | **Stay with CLI defaults** (Claude Code, Copilot, OpenCode) | The plan → implement → review loop is all you need. Adding ceremony slows you down. |
| Greenfield project, solo developer, want guardrails against scope creep | **Consider OpenSpec** | The propose → apply → archive cycle forces you to define scope before coding. Lightweight enough to not slow you down. |
| Need structured handoff between sessions or developers | **Consider OpenSpec** | Specs in `changes/` folders survive context-window resets. New sessions pick up where old ones left off. |
| Regulatory or compliance requirements, need audit trail | **Consider BMAD** | Full traceability from requirement → story → code. Documents every decision. |
| Large team with junior developers, complex multi-system project | **Consider BMAD** | Role separation prevents agents from overstepping. Stories provide clear, bounded work items. Sprint tracking keeps everyone aligned. |
| You tried defaults and keep hitting the same problems | **Level up one step** | Don't jump from defaults to BMAD. Try OpenSpec first. Add ceremony incrementally, matching structure to pain. |

### The upgrade path

```
CLI defaults (Claude Code / Copilot / OpenCode)
    │
    │  "I keep losing context between sessions"
    │  "Features keep growing beyond what I intended"
    ▼
OpenSpec (specs + design docs per change)
    │
    │  "I need formal traceability"
    │  "Multiple teams need coordinated planning"
    ▼
BMAD (full agile methodology with agent roles)
```

Each step adds ceremony. Each step costs speed. Move up only when the pain justifies the cost.

---

## Closing

The SDLC phases haven't changed since they were formalized in the 1960s. Requirements, design, implementation, review, testing — every software project goes through them, whether you call them that or not.

What's changed is who executes them. An Architect agent or a developer typing "make a plan" in Claude Code — same phase, different ceremony. A PM agent writing a PRD or a developer describing the feature in a prompt — same phase, different formality.

Pick the level of ceremony that matches your pain, not your ambition. For most teams, the defaults are not just good enough — they're better. They're faster, cheaper, and keep you closer to the code. Start there. Level up when you feel the friction. Not before.

---

## Resources

- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub Copilot CLI](https://docs.github.com/en/copilot)
- [OpenCode — GitHub](https://github.com/anomalyco/opencode) | [Docs](https://opencode.ai/docs/)
- [OpenSpec — GitHub](https://github.com/Fission-AI/OpenSpec) | [Docs](https://openspec.pro/)
- [BMAD Method — GitHub](https://github.com/bmad-code-org/BMAD-METHOD) | [Docs](https://docs.bmad-method.org/)
- [Spec-Driven Development landscape (Medium)](https://medium.com/@visrow/spec-driven-development-is-eating-software-engineering-a-map-of-30-agentic-coding-frameworks-6ac0b5e2b484)
- Chapter 8 — [Multi-Agent Workflows](../technical/08_workflows/08_workflows.md) in this training
