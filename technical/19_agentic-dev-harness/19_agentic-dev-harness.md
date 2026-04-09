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

## The Compounding Effect

Each phase of the SDLC is a filter. What passes through to the next phase is cleaner, more correct, and easier to work with.

A well-written `CLAUDE.md` and a solid spec template eliminate more defects than any number of post-hoc sensors. The speed gain comes not from skipping quality, but from front-loading it — fewer review cycles, fewer rework loops, fewer surprises.

Here's how guidance effort tapers across the SDLC:

```
Conception  ██████████████████  ← most guidance, cheapest to fix
Spec        █████████████████
Design      ████████████████
Code        ██████████████      ← hooks catch most issues here
Test        ████████████
Review      ████████            ← less to find if earlier phases worked
Quality     ██████
Optimize    ████
Maintain    ██                  ← lightest touch, mostly monitoring
```

<img src="./compounding-funnel.svg" width="100%"/>

Invest most in the early guides. The goal is not zero checks at the end — sensors always stay on. But the agent self-corrects less because it got better input. When CLAUDE.md is clear, the spec is tight, and the design is agreed upon, the code phase produces fewer mistakes. The test phase catches less. The review phase has less to flag. Fewer review cycles means faster delivery.

## Phase 1: Conception and Requirements

This is where you brainstorm features, explore constraints, and discuss trade-offs with the agent. You're not writing code yet — you're figuring out what to build and why. The agent becomes a thinking partner: it asks questions you forgot, surfaces edge cases you missed, and structures the mess of ideas into something actionable.

This phase has the most leverage of any in the SDLC. A wrong requirement is 100x more expensive to fix in production than to catch here. Front-load your guidance investment. Give the agent rich context about your project, your domain, and your constraints — and it will ask better questions, spot more gaps, and produce requirements that actually hold up.

### Guide

- **Project context files** — a `CLAUDE.md` with project description, domain glossary, and team conventions. The agent needs to know what this system *is* before it can reason about what it *should do*.
- **Existing documentation fed as context** — PRDs, architecture docs, prior specs. The more the agent knows about past decisions, the less it reinvents or contradicts.
- **User story templates with required fields** — persona, goal, acceptance criteria, edge cases, non-functional requirements. Templates force completeness; without them, the agent skips sections.
- **Brainstorming skills that enforce structured exploration** — a skill that walks through a checklist before letting the agent jump to implementation. Structure prevents premature solutioning.

### Sensor

- **Checklist validation** — does the output cover acceptance criteria, edge cases, non-functional requirements, security considerations? A simple completeness check catches the most common gaps.
- **Cross-reference check** — does this feature conflict with existing features or specs? The agent should verify against what's already been decided.

### Concrete Config

A `CLAUDE.md` snippet that sets project context and points the agent to the brainstorming skill:

```markdown
## Project Context
This is an e-commerce platform (Java/Spring Boot backend, React frontend).
Domain: orders, inventory, payments. Key constraint: PCI compliance for payment data.
Before implementing any feature, brainstorm requirements using /brainstorm.
```

A brainstorming skill at `.claude/skills/brainstorm.md` that enforces structured exploration:

```markdown
Ask clarifying questions one at a time. For each feature, cover:
1. Who is the user? What's their goal?
2. What are the acceptance criteria?
3. Edge cases and error scenarios?
4. Non-functional requirements (performance, security, compliance)?
5. Does this conflict with existing features?
Output a structured requirements doc in docs/requirements/.
```

### Framework Alternative

Teams wanting more structure can use BMAD's Analyst and PM agents to generate PRDs, or OpenSpec's `/opsx:propose` to formalize the idea.

## Phase 2: Specification

You've figured out *what* to build. Now you write the detailed spec: acceptance criteria, API contracts, error handling, testing strategy. The spec becomes the guide for every subsequent phase — the agent reads it before coding, tests against it, and references it during review.

A vague spec creates a vague implementation. If the spec says "handle errors appropriately," the agent will guess — and guess differently every time. Tight specs with concrete examples produce consistent, correct code. Your investment here pays off in every phase that follows.

### Guide

- **Spec templates** — a markdown structure with required sections: overview, requirements, API contract, error handling, testing strategy. The template makes missing sections visible.
- **Existing specs as few-shot examples** — show the agent what a good spec looks like in your project. One example is worth a hundred instructions.
- **Domain glossary** — enforce consistent terminology. If your team says "order," the agent shouldn't say "purchase" or "transaction."
- **Constraints doc** — approved technologies, forbidden patterns, compliance requirements. The agent should know what it *can't* use before it proposes solutions.

### Sensor

- **Spec review skill** — checks for completeness, ambiguity, contradictions, and missing error scenarios. This is an inferential sensor — it uses the LLM to judge spec quality.
- **Human review gate** — specs always need human sign-off. The agent can self-improve the spec, but you make the final call.

### Feedback Loop

Agent writes spec. The spec review skill checks for completeness and ambiguity. The agent rewrites flagged sections. The review skill re-checks. This loop converges — each pass fixes fewer issues. When it's clean, you see a polished spec, not a first draft. The agent did two or three rounds of revision before you even looked.

### Concrete Config

A spec review skill at `.claude/skills/review-spec.md`:

```markdown
Review the spec at the given path. Check for:
- Missing sections: overview, requirements, API contract, error handling, testing strategy
- Vague language: "should", "appropriately", "as needed", "etc."
- Missing error scenarios for each API endpoint
- TBD/TODO placeholders
- Contradictions between sections
Output: list of findings with severity (MUST FIX / SHOULD FIX / NOTE).
After listing findings, rewrite the flagged sections and present the updated spec.
```

A `CLAUDE.md` instruction that wires the skill into the workflow:

```markdown
## Specs
After writing any spec, run /review-spec on it before presenting to the user.
If findings are MUST FIX, rewrite and re-check until clean.
```

### Framework Alternative

OpenSpec's `/opsx:apply` formalizes this into a strict three-phase state machine (proposal, spec, archive).

## Phase 3: Architecture and Design

You know what to build and you have a tight spec. Now you decide *how* to build it — architecture decisions, data models, API design, component boundaries. This phase sets the structural constraints the agent must follow during implementation.

The agent is good at generating architecture proposals. It's bad at knowing your system's history. Without context, it'll propose patterns that contradict past decisions, introduce dependencies that violate module boundaries, or design stateful services in a stateless system. Feed it your ADRs, your existing diagrams, and your design principles — and it proposes designs that fit.

### Guide

- **Architecture Decision Records (ADRs)** — the agent reads past decisions and follows established patterns. ADRs are the institutional memory that prevents the agent from re-debating settled questions.
- **Existing diagrams and models as context** — Mermaid source files, ERDs, component diagrams. Visual context helps the agent understand system structure.
- **Design principles doc** — explicit rules like "prefer composition over inheritance" or "all services must be stateless." Without these, the agent defaults to whatever the training data suggests.
- **Module boundary rules** — which packages can depend on which. Cross-boundary imports are the most common architectural violation agents produce.

### Sensor

- **Structural validation** — does the design violate module boundaries? This can be checked mechanically against the rules in `CLAUDE.md`.
- **Pattern consistency check** — does the design match existing patterns or deviate? Deviation isn't always wrong, but it should be flagged and justified.
- **Diagram generation** — the agent produces Mermaid diagrams for review. Visual output makes architectural issues obvious that text descriptions hide.

### Feedback Loop

Agent proposes architecture. The fitness check validates against ADRs, module boundaries, and established patterns. The agent restructures any violations. The re-check passes. You review a design that already fits the system — not a raw proposal that ignores half of your constraints.

### Concrete Config

A `CLAUDE.md` section that defines architecture rules:

```markdown
## Architecture Rules
- Layered architecture: controller → service → repository. No skipping layers.
- Module boundaries: `orders` cannot import from `payments` directly — use events.
- All new services must be stateless. Session data goes in Redis.
- Before proposing new components, read docs/adrs/ for past decisions.
- After designing, run /check-architecture to validate.
```

An architecture check skill at `.claude/skills/check-architecture.md`:

```markdown
Review the proposed design against:
1. Module boundary rules in CLAUDE.md — any cross-boundary imports?
2. Existing ADRs in docs/adrs/ — does this contradict a past decision?
3. Layer violations — does any component skip a layer?
4. New dependencies — does this introduce a library not in approved-libs.md?
If violations found, restructure the design and re-check.
Generate a Mermaid diagram of the final design.
```

### Framework Alternative

BMAD's Architect agent produces formal architecture documents with orchestrator memory.
