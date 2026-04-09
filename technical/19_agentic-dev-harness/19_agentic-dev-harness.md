# Chapter 19: Building Your Agentic Development Harness

Two developers use Claude Code to build the same microservice. Same model, same day, same codebase.

Developer A opens a terminal, types `claude`, and starts prompting. The agent produces code that works — but uses `any` types everywhere, picks a logging library the team doesn't use, and skips error handling in three endpoints. Developer A spends two hours cleaning up what the agent got wrong.

Developer B opens the same terminal. But their project has a `CLAUDE.md` with architectural rules, a hook that runs the linter after every file edit, and a `/review` skill that checks for OWASP issues. The agent follows the rules from the start, gets corrected automatically when it drifts, and flags its own security gaps before Developer B even looks. The feature ships in half the time — and passes code review on the first try. Same model. The difference is the harness.

## What Is a Harness?

Martin Fowler puts it simply: **Agent = Model + Harness**. The model is the LLM — the part that reasons and generates code. The harness is everything else: the context it reads, the rules it follows, the checks it runs against. You don't control the model. You control the harness. That's where your leverage is.

A harness steers the agent through two types of controls:

**Guides (feedforward controls)** work like guardrails on a road. They steer the agent *before* it acts. The agent reads them and adjusts its behavior up front.

- `CLAUDE.md` rules ("All services must be stateless")
- Spec templates that define what "done" looks like
- Architectural constraints ("Use the repository pattern for data access")
- Approved library lists ("Use `zod` for validation, not `joi`")

**Sensors (feedback controls)** work like speed cameras. They check *after* the agent acts and enable self-correction.

- Linters that flag style violations
- Test runners that catch broken behavior
- Code review skills that evaluate design decisions
- Quality gates that block commits until standards are met

Both guides and sensors come in two flavors:

| Flavor | How It Works | Speed | Cost | Catches |
|--------|-------------|-------|------|---------|
| **Computational** | Deterministic rules — linters, type checkers, formatters | Fast | Free | Syntax, types, style |
| **Inferential** | AI-based judgment — review agents, LLM judges | Slower | Tokens | Semantic issues, design flaws, security gaps |

Use computational checks for everything they can cover. They're fast, free, and reliable. Reserve inferential checks for the things only an LLM can judge — "Does this API design make sense?" or "Could this input be exploited?"

## Three Approaches to Agentic Workflows

There's more than one way to structure how an agent works on your code. Here are the three main approaches:

| Approach | Philosophy | Your Interface | When Code Is Wrong | Tradeoff |
|----------|-----------|----------------|-------------------|----------|
| **Harness** (this chapter) | Build guardrails incrementally. Keep direct control. | CLAUDE.md + hooks + skills + subagents | Fix code directly or adjust the harness | Most flexible, no lock-in, but you build it yourself |
| **Spec-driven** (OpenSpec, Kiro, Spec Kit) | The spec is the source of truth. | Edit the spec, agent regenerates code | Update the spec and regenerate | Clean separation, but you become a spec editor — struggles with exploratory work |
| **Full ceremony** (BMAD) | 12+ specialized agents orchestrated by YAML workflows. | Approve at gates between phases | Roll back to the right phase and re-run | Most automated, but heavy ceremony and framework lock-in |

This chapter focuses on the harness approach. It gives you direct control over the agent's behavior. You build it incrementally — start with a few rules, add checks as you learn what goes wrong. There's no framework to adopt and no lock-in. And when you're ready, the harness composes naturally with the other approaches: you can add spec-driven generation on top, or plug harness components into a larger orchestration.

## How This Works in Claude Code

Claude Code has no workflow engine. The harness is assembled from four mechanisms:

| Mechanism | Role | Runs... | Example |
|-----------|------|---------|---------|
| **CLAUDE.md** | Guides — rules the agent reads | Automatically at session start | "All services must be stateless. Never use `any` type." |
| **Hooks** | Sensors — scripts that fire on events | Automatically on edit/commit/etc | ESLint after every file edit, block `rm -rf` |
| **Skills** | Inferential checks — reusable prompts | On invocation (manual or instructed by CLAUDE.md) | `/review` checks OWASP top 10, `/simplify` reduces complexity |
| **Subagents** | Independent workers — spawn for specific tasks | Programmatically by the agent | Spawn a code reviewer agent, spawn a test generator |

> **Hooks can't be bypassed by the agent** — they're mechanical enforcement. CLAUDE.md can be ignored (the agent might "forget"). Use hooks for hard rules, CLAUDE.md for guidance, skills for judgment calls.
