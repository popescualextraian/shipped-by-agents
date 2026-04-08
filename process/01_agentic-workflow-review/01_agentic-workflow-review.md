# Agentic Workflow Review

*A periodic checklist for developers and teams to find manual work that agents can handle.*

---

## Purpose

You build habits fast. Some of those habits involve manual steps that made sense before you had an AI agent but no longer need to be done by hand. This checklist helps you find them.

Run it individually (end of week) or as a team (end of sprint). Each item is a question. A "yes" means there is an improvement to make. Not every "yes" needs action immediately — prioritise by frequency and time cost.

---

## When to Run

| Cadence | What | Who | Time |
|---------|------|-----|------|
| **Weekly** | Quick Scan (10 items) | Individual developer | 5 minutes |
| **Per sprint** | Full Review (all sections) | Team, in sprint retrospective | 20-30 minutes |
| **After onboarding** | Full Review | New team member, after first two weeks | 20-30 minutes |
| **Quarterly** | Maturity Check | Team lead or team | 30-45 minutes |

---

## Quick Scan (Weekly)

Ten high-signal questions. If you only do one thing, do this. Five minutes at the end of your week. Actions here are kept brief — the Full Review has more detailed guidance for each area.

- [ ] Did I correct the agent on something it should have already known?
  - **Action:** Add it to the instruction file
- [ ] Did I copy-paste between an external tool and the agent?
  - **Action:** Find an MCP integration or pipe the output directly
- [ ] Did I have to explain a business rule, domain concept, or internal standard the agent should have known?
  - **Action:** Write it down — instruction file, wiki, or both
- [ ] Did I test something manually that could be an automated test?
  - **Action:** Ask the agent to generate the test
- [ ] Did I do something manually that I also did manually last week?
  - **Action:** This is the strongest signal. If it repeats, automate it
- [ ] Did I review code without asking the agent to review it first?
  - **Action:** Run an agentic review before human review
- [ ] Did I write something from scratch that the agent could have drafted (PR description, story, release notes, status update)?
  - **Action:** Ask the agent to draft it next time. You edit, not create
- [ ] Did I Google something to answer a question the agent could not?
  - **Action:** Add the answer to the instruction file or connect a documentation MCP
- [ ] Did a session go well or badly? Do I know why?
  - **Action:** Run `/insights`. Capture what worked and what did not
- [ ] Is there tribal knowledge on the team that is not written down anywhere?
  - **Action:** Start with the top three things that trip people up. Document them

---

## Full Review

The complete checklist, organised by category. You do not need to run every category every sprint — pick two or three categories, rotate through all of them over two to three sprints. Not every "yes" needs action immediately — prioritise by frequency and time cost.

### Instruction File Health

- [ ] Did I correct the agent on something it should have already known?
  - **Action:** Add the missing rule to `CLAUDE.md` (or equivalent)
- [ ] Did the agent search extensively for something in the codebase that could be documented?
  - **Action:** Add architecture notes or file location hints to the instruction file
- [ ] Did I ask the agent to generate a diagram and it was wrong?
  - **Action:** Diagnose — is the code misleading or is the instruction file incomplete? Fix the root cause
- [ ] Did I explain the same concept to the agent that I explained last week?
  - **Action:** If you said it twice, write it down. Repeated explanations are missing documentation
- [ ] Did the agent pick the wrong pattern, framework, or library for a task?
  - **Action:** Add explicit "use X, not Y" rules to the instruction file with the reason why
- [ ] Did I run `/insights` or ask the agent to reflect at the end of each session?
  - **Action:** Make this a habit. Session reflections are the fastest way to improve the instruction file

### External Knowledge Access

The agent only knows what is in the codebase, the instruction file, and its training data — everything else is invisible unless you make it available.

- [ ] Did the agent use outdated information about a library, framework, or API?
  - **Action:** Add a documentation MCP so the agent fetches current docs instead of relying on training data
- [ ] Did I have to explain a business rule, domain concept, or client-specific requirement?
  - **Action:** If it is documented somewhere (Confluence, wiki, shared drive), find an MCP integration so the agent can read it. If it is not documented anywhere, write it down — in the instruction file, a project wiki, or both
- [ ] Does the team have design standards, coding guidelines, or architecture decision records that live outside the repo?
  - **Action:** Either bring them into the repo (preferred) or connect the agent to where they live
- [ ] Did the agent make a wrong assumption about how an external service or API works?
  - **Action:** Add the relevant API docs or integration notes to the instruction file, or connect a documentation MCP
- [ ] Is there tribal knowledge on the team — things everyone "just knows" that are not written down anywhere?
  - **Action:** This is the most dangerous gap. If the agent does not know it and a new team member would not know it, it needs to be documented. Start with the top three things that trip people up most often
- [ ] Did I Google something to answer a question the agent could not?
  - **Action:** Consider whether the answer should be in the instruction file (project-specific), fetched live via MCP (external docs), or is a one-off (no action needed)

### Copy-Paste and Tool Switching

- [ ] Did I copy-paste errors from a logging platform into the agent?
  - **Action:** Find an MCP integration for your log platform, or pipe test output directly to the agent
- [ ] Did I copy-paste content from a project management or documentation tool?
  - **Action:** Find an MCP integration so the agent reads tickets and docs directly
- [ ] Did I switch to a browser to verify something the agent could check?
  - **Action:** Find an MCP integration or write a script the agent can call
- [ ] Did I manually look up documentation for a library or framework?
  - **Action:** Add a documentation MCP server for live reference access
- [ ] Did I read a monitoring dashboard to diagnose a problem?
  - **Action:** Find an MCP for your monitoring platform so the agent can query metrics directly
- [ ] Did I copy data from a database client to give the agent context?
  - **Action:** Find a database MCP or give the agent access to run read-only queries

### Manual Testing

- [ ] Did I test APIs manually from a REST client or curl?
  - **Action:** Ask the agent to generate automated integration tests from your API specs or existing collections
- [ ] Did I run tests manually instead of asking the agent to run them as part of the task?
  - **Action:** Add test commands to the instruction file and include "run tests before considering this complete" in your prompts
- [ ] Did I verify UI changes by manually clicking through the application?
  - **Action:** Find a browser automation MCP so the agent can verify UI flows
- [ ] Did I create test data by hand?
  - **Action:** Ask the agent to generate test fixtures or seed scripts from your schemas
- [ ] Did I manually verify that a migration worked by inspecting the database?
  - **Action:** Ask the agent to write a verification query or test that checks the expected state

### Code Review and Quality

- [ ] Did I write a PR description from scratch?
  - **Action:** Ask the agent to draft it from the diff and commit history
- [ ] Did I manually check for security issues, dead code, or convention violations?
  - **Action:** Create a skill or prompt template that runs these checks automatically before review
- [ ] Did I spend review time catching things a linter or static analysis tool could catch?
  - **Action:** Add the rule to the linter config or the instruction file so the agent follows it during implementation
- [ ] Did I review code without asking the agent to review it first?
  - **Action:** Run an agentic review before human review — let the agent catch the obvious issues so the human can focus on design and intent
- [ ] Did the agent introduce a potential security issue that I almost missed?
  - **Action:** Add security rules to the instruction file, or create a review skill that includes a security check

### Debugging and Incident Response

- [ ] Did I manually trace a request across multiple services or log groups?
  - **Action:** Find a log aggregation MCP, or create a skill that automates the correlation
- [ ] Did I manually correlate an alert with a recent deployment or code change?
  - **Action:** Create a skill that checks recent commits and deployments when an alert fires
- [ ] Did I reproduce a bug by manually setting up state?
  - **Action:** Ask the agent to write a failing test that reproduces the bug — it becomes both the diagnosis and the regression test
- [ ] Did I spend time re-understanding code I had already understood in a previous session?
  - **Action:** Ask the agent to document the flow or add architecture notes to the instruction file so context survives between sessions

### Documentation and Communication

- [ ] Did I write release notes or a changelog entry by hand?
  - **Action:** Ask the agent to generate them from the commit log and PR descriptions
- [ ] Did I manually update documentation after a code change?
  - **Action:** Include "update related documentation" as part of the agent's task definition, or create a hook that reminds you
- [ ] Did I write a status update, standup note, or progress report from memory?
  - **Action:** Ask the agent to summarise what was done based on commits, PRs, and completed tickets
- [ ] Did I explain the same architectural decision to multiple people?
  - **Action:** Ask the agent to draft an ADR (Architecture Decision Record) so the explanation exists once

### Repetitive Work

- [ ] Did I write user stories by hand when requirements already existed in a document?
  - **Action:** Point the agent at the requirements and ask it to draft stories with acceptance criteria
- [ ] Did I create or update diagrams manually?
  - **Action:** Ask the agent to generate diagrams from the code — and use wrong diagrams as a diagnostic tool
- [ ] Did I perform a manual check before every commit that could be automated?
  - **Action:** Add it to the agent's workflow, a pre-commit hook, or CI
- [ ] Did I format, lint, or reorganise code manually?
  - **Action:** Ensure the agent runs formatting and linting as part of its workflow
- [ ] Did I manually set up a local development environment or configure services?
  - **Action:** Create a setup skill or script the agent can run for new environments
- [ ] Did I manually upgrade a dependency and check for breaking changes?
  - **Action:** Ask the agent to check the changelog, identify breaking changes, and update the code
- [ ] Did I manually resolve merge conflicts?
  - **Action:** Ask the agent to resolve them — it can read both sides, understand the intent, and propose the merge
- [ ] Did I write boilerplate code that follows an existing pattern in the codebase?
  - **Action:** Create a skill or template so the agent generates it consistently every time
- [ ] Did I write the same prompt structure more than once this sprint?
  - **Action:** Turn it into a reusable skill or prompt template

### Learning and Improvement

- [ ] Did a session go particularly well? Do I know why?
  - **Action:** Capture the pattern — what prompt, what context, what approach made it work
- [ ] Did I discover a useful workflow or shortcut?
  - **Action:** Share it with the team. Add it to the instruction file or team knowledge base
- [ ] Did a new team member struggle with the agent?
  - **Action:** Their struggles reveal gaps in the instruction file and onboarding docs. Fix those, not just their immediate problem
- [ ] Did I spend time onboarding someone by walking them through the codebase manually?
  - **Action:** The agent can do guided walkthroughs if the instruction file and documentation are solid. Invest in those instead
- [ ] Did I answer a question about the code that the agent could have answered?
  - **Action:** Test it — ask the agent the same question. If it gets it wrong, the instruction file needs work. If it gets it right, the team member did not know they could ask

### Team Dynamics and Collaboration

- [ ] Did the team spend significant time in a refinement session estimating and breaking down work?
  - **Action:** Before the session, ask the agent to draft a breakdown with effort rationale — "this touches 3 services, here's what changes in each." Use the draft as a starting point for discussion, not a replacement for it
- [ ] Is there a knowledge silo — one person who knows a module and the team is stuck when they are unavailable?
  - **Action:** Ask that person to improve the instruction file and documentation for their area. The goal: the agent plus the docs should be enough for another developer to work in that module

---

## Maturity Check (Quarterly)

Once you have been running the weekly scan and full review for a few sprints, a different kind of question becomes relevant: **how long have I been answering "no" to these items?**

If an item has been "no" for several consecutive reviews, that step is stable. Stable steps can be chained. This section is about graduating from fixing individual friction points to composing automated flows.

### Chaining Stable Steps

- [ ] Are there two or more consecutive steps I always do in the same order that are both stable?
  - **Action:** Chain them into a single agent workflow — plan-build-test, build-review-commit, draft-review-publish
- [ ] Am I still manually triggering each step in a sequence, even though I never intervene between them?
  - **Action:** Compose them into a skill, a hook, or an automated pipeline. Validate the output at the end, not at every intermediate step
- [ ] Do I have a recurring multi-step process (e.g., triage ticket, read context, plan, implement, test, create PR) that I run the same way every time?
  - **Action:** Write it as a single prompt or skill. Let the agent run the whole sequence. Review the final result
- [ ] Am I running the same agentic flow across multiple tasks or repos?
  - **Action:** Extract it into a shared skill or template that the whole team can use

### Team Process Automation

This is where you zoom out from individual developer work to team-level operational processes. Support rotations, release workflows, incident handling, client-facing tasks — processes that involve multiple manual steps, multiple tools, and sometimes multiple people. This may go beyond a single coding agent into scheduled agents, webhooks, or orchestration tools.

- [ ] Does the team have a recurring triage process (check an alert inbox, categorise, create tickets, assign)?
  - **Action:** Map the steps. Identify which ones are rule-based and can be automated. Start with the simplest step
- [ ] Does the team run a manual release or deployment checklist?
  - **Action:** Write it as a script or skill. The agent can execute it with a human gate at the end
- [ ] Does the team provide support that involves reading logs, checking systems, and reporting back?
  - **Action:** Build a diagnostic skill — the agent gathers context and drafts the response. A human reviews before sending
- [ ] Does the team follow an incident response runbook with mostly mechanical steps?
  - **Action:** Turn the runbook into an agent workflow. The agent investigates, the human decides the response
- [ ] Is there a handoff process between teams that involves copying context between tools?
  - **Action:** Automate the context transfer — the agent reads from one system and writes to the other
- [ ] Does the team onboard new clients, tenants, or environments using a manual step-by-step process?
  - **Action:** Script it. If the process is documented well enough for a human to follow, it is documented well enough for an agent to execute
- [ ] Are there periodic audits, reviews, or compliance checks that someone does by hand on a schedule?
  - **Action:** Schedule an agent to run the check and flag exceptions. A human reviews only the flagged items
- [ ] Are there team processes where multiple steps have been individually automated but are still triggered manually?
  - **Action:** Connect them into full pipelines with human gates only where judgment is needed

**How to find these processes:** Ask each team member: *"What do you do every week or every sprint that is not writing code?"* The answers are your candidate list.

The progression: **fix individual steps, then chain stable steps, then automate entire flows**. Do not skip ahead — chaining unreliable steps just multiplies the unreliability.

---

## How to Use the Results

**Individual:** After running the checklist, pick the top one or two items by frequency (how often it happens) and time cost (how much time it wastes each occurrence). Fix those first. Do not try to address everything at once.

**Team:** Collect answers from each team member. Look for patterns — if three people hit the same issue, it is a team-level improvement, not an individual one. Assign one improvement per sprint as a concrete action item.

**Track over time:** Keep a simple log of what you changed and when. After a few sprints, you will see the cumulative effect: shorter sessions, fewer corrections, better agent output, less manual work.

---

## The Compound Effect

Each item you fix makes every future session slightly better. The instruction file gets richer. The integrations remove manual steps. The agent's output improves because its context improves. Over weeks, the cumulative effect is significant — not because the agent got smarter, but because you got better at using it.

The goal is not perfection. The goal is continuous improvement, one friction point at a time.

---

*For the full reasoning behind this checklist, see the [Think Like an Agent User](../../articles/agentic-thinking/agentic-thinking.md) article.*
