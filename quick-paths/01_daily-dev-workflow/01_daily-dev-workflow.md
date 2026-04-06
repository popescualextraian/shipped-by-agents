# Quick Path: Daily Dev Workflow

A fast-track guide to the most common development activities with AI agents. Each section is a self-contained recipe — pick the ones you need.

---

## 1. Creating Documentation

**The key insight:** With AI agents, your documentation lives *inside* your project — as markdown files, right next to your code. The agent reads them, writes them, and keeps them in sync. External systems like Confluence become a publishing target, not the source of truth. Your project folder *is* the knowledge base.

**What:** Draft documentation as Markdown with your AI agent, then publish to Confluence using the Atlassian MCP.

**Setup:**

- A strong `CLAUDE.md` (or equivalent rules file) with project context, conventions, and document templates
- External sources (requirements docs, design specs, stakeholder notes, standards) saved as `.md` files in your project or a dedicated reference folder — the agent indexes these automatically. This follows Karpathy's [LLM Knowledge Bases](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern: keep raw sources as markdown, let the LLM maintain and cross-reference them. No RAG pipeline needed. With 200k–1M token context windows, you can fit ~100 documents (~400k characters) directly in context.
- [Atlassian MCP server](https://github.com/sooperset/mcp-atlassian) configured for Confluence and JIRA

**How:**

1. Ask the agent to draft the document as Markdown. Provide the relevant source files and any existing pages for context.
2. Review the draft — iterate on structure, tone, and technical accuracy.
3. Once approved, ask the agent to create the Confluence page using the Atlassian MCP. The agent converts Markdown to Confluence format and uploads it.

**Example prompt:**

```
Read the files in /docs/api-specs/ and create a developer onboarding guide
for our REST API. Follow the structure in CLAUDE.md. When done, publish it
to our Confluence space "ENG" under the "Onboarding" parent page.
```

**Links:**

- [Atlassian MCP server docs](https://github.com/sooperset/mcp-atlassian)
- [Confluence storage format](https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html)
- [Claude Code CLAUDE.md guide](https://docs.anthropic.com/en/docs/claude-code/memory)
- Dive deeper: [Chapter 9 — Automating User Story Creation](../technical/09_story-creation/09_story-creation.md) (covers Atlassian MCP setup)

---

## 1.1 Creating Diagrams

**What:** Generate diagrams with your AI agent. No MCP servers, no plugins, no skills required — every AI coding agent can do this out of the box. Multiple options depending on your needs.

**Options:**

| Approach | Best for | Editable? | How |
|----------|----------|-----------|-----|
| **Mermaid** | Flowcharts, sequences, ER diagrams | Yes (text) | Ask the agent to write Mermaid syntax. Render in Markdown previews, Confluence, or GitHub. |
| **DrawIO XML** | Complex architecture diagrams | Yes (GUI + XML) | Ask the agent to generate DrawIO XML. Save as `.drawio`, open in draw.io, upload to Confluence. |
| **SVG** | Custom visuals, brand-aligned diagrams | Yes (code) | Ask the agent to create SVG directly. Claude has gotten good at this recently. Export to PNG if needed. |

**How (Mermaid example):**

1. Describe the diagram you need — the agent generates the Mermaid code.
2. Preview it in your IDE or a Mermaid live editor.
3. Embed it in your Markdown doc or Confluence page.

**How (DrawIO example):**

1. Ask the agent to create a DrawIO XML file for your diagram.
2. Open it in [draw.io](https://app.diagrams.net/) to tweak layout and styling.
3. Upload the `.drawio` file to Confluence — it renders natively with the draw.io plugin.

**Links:**

- [Mermaid documentation](https://mermaid.js.org/)
- [draw.io documentation](https://www.drawio.com/doc/)
- Dive deeper: [Chapter 6 — A Development Workflow](../technical/06_a-development-workflow/06_a-development-workflow.md)

---

## 2. Writing User Stories

**Same principle as documentation:** your requirements, templates, and reference material live as markdown in your project. The agent drafts stories from this local knowledge base and pushes them to JIRA — the project folder is the source of truth, JIRA is the delivery target.

**What:** Use your AI agent to draft user stories from project context and external sources, then push them straight to JIRA.

**Setup:**

- Same `CLAUDE.md`, external sources, and Atlassian MCP setup as [section 1](#1-creating-documentation)
- Add user story conventions to your `CLAUDE.md` — acceptance criteria format, story templates, definition of done

**How:**

1. **Create a story template.** Most teams have one — acceptance criteria format, story structure, definition of done. Save it as a markdown file and reference it in your `CLAUDE.md`. The agent will follow it for every story.
2. Gather your external sources into markdown files. Most reference material doesn't change often — index it once, reuse it across stories.
3. Point the agent at the relevant source files and template, and ask it to draft stories following your conventions.
4. Review and refine the drafts with the agent — iterate on acceptance criteria, edge cases, and scope.
5. Use the Atlassian MCP to create the JIRA issues directly from the conversation.

**Links:**

- [Atlassian MCP server docs](https://github.com/sooperset/mcp-atlassian)
- Dive deeper: [Chapter 9 — Automating User Story Creation](../technical/09_story-creation/09_story-creation.md)

---

## 3. Coding

**What:** Use the plan-first approach: plan with the agent, review the plan, execute, and create a PR. No special plugins needed — just the defaults.

**Setup:**

- An AI coding agent (Claude Code, Cursor, Windsurf, etc.)
- A well-configured `CLAUDE.md` or equivalent rules file

**How:**

1. **Plan first.** Ask the agent to create an implementation plan. Review it — challenge assumptions, check scope.
2. **Split if complex.** If the plan has more than 5-7 steps, break it into smaller plans. Each should be independently executable.
3. **Execute.** Let the agent implement the plan. If your tool supports it, assign multiple agents to independent parts for parallelization.
4. **Review.** Use the agent's review command (e.g., `/review` in Claude Code) to get a first pass. Then review the code yourself.
5. **Create the PR.** Ask the agent to create the pull request with a clear description.

**Think in components, not specs.** Don't just hand the agent a full specification and hope for the best. Break work into architectural components — a service, a module, an API layer. Plan and execute at that level. Component-based thinking gives the agent clear boundaries and gives you reviewable chunks.

**Key principle:** The agent proposes, you decide. Never merge code you haven't reviewed yourself.

**Links:**

- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- Dive deeper: [Chapter 3 — Coding with AI Agents](../technical/03_coding-with-agents/03_coding-with-agents.md)
- Dive deeper: [Chapter 6 — A Development Workflow](../technical/06_a-development-workflow/06_a-development-workflow.md)

---

## 4. Unit Testing

**What:** Always write unit tests — they're cheap and the agent generates them fast. Make this a default part of every coding task.

**Setup:**

- Your project's test framework (JUnit, pytest, Jest, etc.) already configured
- Test conventions documented in `CLAUDE.md`

**How:**

1. When coding, ask the agent to write unit tests alongside the implementation — or immediately after.
2. Review the tests for meaningful assertions. Agents tend to over-test happy paths and under-test edge cases — nudge them.
3. Run the tests and let the agent fix any failures.

**Tip:** Add a line to your `CLAUDE.md`: *"Always create unit tests for new code."* The agent will do it automatically.

**Links:**

- [JUnit 5 docs](https://junit.org/junit5/docs/current/user-guide/) | [pytest docs](https://docs.pytest.org/) | [Jest docs](https://jestjs.io/docs/getting-started)
- Dive deeper: [Chapter 10 — Testing with AI Agents](../technical/10_testing-with-agents/10_testing-with-agents.md)

---

## 5. Integration / API Testing

**What:** Use AI agents with MCP plugins to write and run integration tests against real APIs and UIs.

**Setup:**

- For UI testing, pick one:
  - **Claude in Chrome** (built-in) — install the [Claude Chrome extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn), then launch Claude Code with `--chrome`. No MCP needed — Claude Code controls your browser directly.
  - **Playwright MCP** — install the [Playwright MCP plugin](https://github.com/anthropics/claude-code-playwright). Works with any browser, headless-friendly.
- Your API test framework (REST Assured, Supertest, requests, etc.)
- Test environment URLs and credentials configured

**How:**

1. Describe the scenario you want to test — the agent writes the test.
2. For UI tests, both Claude in Chrome and Playwright MCP let the agent interact with the browser — navigate, click, fill forms, read console errors, and assert.
3. For API tests, the agent writes requests against your endpoints and validates responses.
4. Run the tests, review the results, iterate.

**Tip:** Prefer writing reusable test scripts (Playwright tests, REST Assured suites) over one-off agent browser sessions. Reusable tests go into your CI/CD pipeline and keep paying off long after the agent conversation ends.

**Links:**

- [Claude in Chrome docs](https://code.claude.com/docs/en/chrome)
- [Playwright MCP docs](https://github.com/anthropics/claude-code-playwright)
- [REST Assured docs](https://rest-assured.io/) | [Supertest docs](https://github.com/ladjs/supertest)
- Dive deeper: [Chapter 10 — Testing with AI Agents](../technical/10_testing-with-agents/10_testing-with-agents.md)

---

## 6. Debugging

**What:** Use the agent for systematic root cause analysis instead of random trial-and-error.

**Setup:**

- No special setup needed — your agent and codebase are enough
- For remote logs: configure MCP servers for your logging platform (CloudWatch, Datadog, Splunk, etc.)

**How:**

1. Describe the bug — paste the error, the expected behavior, and the actual behavior.
2. Let the agent investigate. It reads code, traces call paths, and checks logs.
3. Review the agent's diagnosis before accepting any fix. Agents are good at finding the root cause but can propose overly broad fixes.
4. Ask the agent to implement the fix and write a regression test.

**Links:**

- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- Dive deeper: [Chapter 11 — Debugging & Troubleshooting](../technical/11_debugging/)

---

## 6.1 Debugging with Remote Logs

**What:** Give your agent direct access to production or staging logs — CloudWatch, Datadog, Splunk, Grafana, etc. Instead of copy-pasting log snippets, the agent queries logs itself, correlates timestamps, and traces issues across services.

**Setup:**

Pick one approach:

- **MCP server** — install an MCP server for your logging platform. Examples:
  - [AWS CloudWatch MCP](https://github.com/awslabs/mcp/tree/main/src/cloudwatch-mcp-server) — CloudWatch Logs, alarms, metrics
  - [Datadog MCP](https://github.com/datadog-labs/mcp-server) — metrics, logs, APM traces
  - Community servers exist for Splunk, Grafana, Elastic, and others — check [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- **Custom skill** — write a skill that wraps your CLI tools (e.g., `aws logs filter-log-events`, `datadog-ci logs`) and returns formatted output to the agent
- **Plain CLI** — if your logging CLI is already installed, the agent can run it directly via bash. No MCP needed, but less structured.

**How:**

1. Configure the MCP server or skill with your credentials and default log groups/indexes.
2. Describe the issue — include timestamps, affected services, and error messages if you have them.
3. The agent queries logs directly, filters by time range, and searches for patterns.
4. It correlates across services — e.g., tracing a request ID from an API gateway log to a downstream service error.
5. Review the agent's findings, then fix and test as in section 6.
6. **Close the loop:** combine with your integration tests from [section 5](#5-integration--api-testing). The agent reads the logs, proposes a fix, runs the integration tests to verify, and iterates until they pass — all in one conversation.

**Example prompt:**

```
The /api/orders endpoint started returning 500 errors around 14:30 UTC today.
Check CloudWatch logs for the orders-service and the payments-service.
Find the root cause and suggest a fix.
```

**Links:**

- [AWS CloudWatch MCP server](https://github.com/awslabs/mcp/tree/main/src/cloudwatch-mcp-server)
- [Datadog MCP server](https://github.com/datadog-labs/mcp-server)
- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) — community MCP server catalog
- Dive deeper: [Chapter 11.1 — Integrating Remote Log Analysis](../technical/11_debugging/01_log-analysis-integration.md)

---

## 7. Code Review

**What:** Use the agent as a first-pass reviewer, then do your own review before merging.

**Setup:**

- No special setup needed

**How:**

1. Ask the agent to review the changes (e.g., `/review` in Claude Code, or paste the diff).
2. The agent checks for bugs, security issues, style violations, and missing tests.
3. Address the agent's findings — fix real issues, dismiss false positives.
4. Do your own review. The agent catches mechanical issues; you catch design and intent problems.
5. Create the PR when both passes are clean.

**Links:**

- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- Dive deeper: [Chapter 6 — A Development Workflow](../technical/06_a-development-workflow/06_a-development-workflow.md)

---

## 8. Refactoring

**What:** Use the agent to clean up code, migrate patterns, or upgrade dependencies — with a safety net of tests.

**Setup:**

- Good test coverage (see sections 4 and 5)
- Clear scope — tell the agent exactly what to refactor and what to leave alone

**How:**

1. **Tests first.** Make sure the code you're refactoring has tests. If not, ask the agent to write them before touching anything.
2. **Define the scope.** "Refactor the auth module to use the new middleware" is good. "Clean up the codebase" is not.
3. **Execute.** Let the agent do the refactoring. Review each change — agents can be overeager with "improvements."
4. **Run tests.** Verify nothing broke. Ask the agent to fix any failures.
5. **Review and PR.** Same as coding — agent review first, then your own.

**Links:**

- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- Dive deeper: [Chapter 3 — Coding with AI Agents](../technical/03_coding-with-agents/03_coding-with-agents.md)

---

## Tools & Alternatives

What you need for each activity and what skill bundles can replace or enhance the defaults.

| Section | Default tool | MCP / Plugin | Superpowers alternative |
|---------|-------------|--------------|------------------------|
| 1. Documentation | AI agent — drafts Markdown from your source files | [Atlassian MCP](https://github.com/sooperset/mcp-atlassian) (publish to Confluence) | — |
| 1.1 Diagrams | AI agent — generates Mermaid, DrawIO XML, or SVG | None needed | — |
| 2. User Stories | AI agent — drafts stories from templates and sources | [Atlassian MCP](https://github.com/sooperset/mcp-atlassian) (create JIRA issues) | — |
| 3. Coding | AI agent — plan, execute, review cycle | None needed | `/writing-plans` (architect), `/executing-plans` (executor) |
| 4. Unit Testing | AI agent + your test framework (JUnit, pytest, Jest) | None needed | `/test-driven-development` |
| 5. Integration Tests | AI agent + your test framework + browser tool | [Playwright MCP](https://github.com/anthropics/claude-code-playwright) or [Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) | — |
| 6. Debugging | AI agent — reads code, traces call paths | None needed | `/systematic-debugging` |
| 6.1 Remote Logs | AI agent + your logging CLI (aws, datadog-ci) | [AWS CloudWatch MCP](https://github.com/awslabs/mcp/tree/main/src/cloudwatch-mcp-server), [Datadog MCP](https://github.com/datadog-labs/mcp-server), etc. | — |
| 7. Code Review | AI agent — checks bugs, security, style, missing tests | None needed | `/requesting-code-review`, `/receiving-code-review` |
| 8. Refactoring | AI agent + existing test coverage as safety net | None needed | `/brainstorming` (scope), `/writing-plans` (plan) |

**Key:**
- **Default tool** — what you need at minimum. Most activities work with any AI coding agent out of the box.
- **MCP / Plugin** — optional add-ons that unlock external integrations (JIRA, Confluence, browsers, logs).
- **Superpowers** — [Superpowers skill bundle](https://github.com/claude-did-this/superpowers) for Claude Code. Adds structured workflows for planning, testing, debugging, and review.

---

## 9. What to Automate vs. Where to Intervene

Not everything should be hands-off. Here's a practical split between what the agent can handle autonomously and where you need to stay in the loop.

**Let the agent handle (low effort, low risk):**

| Activity | Why it's safe |
|----------|---------------|
| Drafting docs and stories | You review before publishing anyway |
| Writing unit tests | Fast to generate, fast to verify — just run them |
| Creating commits | Low risk — you review the diff before pushing |
| Generating diagrams | Visual output — you see immediately if it's wrong |
| Running tests | No side effects — the agent reads the output and iterates |
| Starting the deployment pipeline | A trigger, not a decision — the pipeline has its own gates |

**Stay hands-on (high judgment, high stakes):**

| Activity | Why you intervene |
|----------|-------------------|
| Reviewing code | The agent catches mechanical issues; you catch design and intent problems |
| Approving the plan | The plan shapes everything — challenge assumptions before execution |
| Merging PRs | Final gate — you own the decision to ship |
| Debugging production issues | The agent investigates, but you decide what to deploy to prod |
| Scoping refactors | "Clean up" without boundaries leads to scope creep |

**When to use agent review:** Use it as a first pass on every PR. It catches things you'd miss scanning quickly — unused imports, missing null checks, inconsistent naming. But don't skip your own review. The agent doesn't know your team's intent or the bigger picture.

### Growing into a streamlined process

Once your flow works most of the time with few interventions, you can start chaining activities into an end-to-end process:

1. **Validate inputs at the start.** Before the agent begins, make sure the sources, templates, and context are in place. A quick checklist in your `CLAUDE.md` works well.
2. **Let the agent run the full cycle.** Draft → implement → test → commit → create PR. Minimal interruptions.
3. **Validate outputs at the end.** Review the PR, run the pipeline, check the results. Your role shifts from doing to verifying.

The goal is not full autopilot — it's reducing your touch points to the ones that matter: **the beginning** (set direction) and **the end** (verify results). Everything in between, the agent handles.

---

## Conclusion

As the table shows, you can cover most of your daily development stack with just an AI coding agent, a couple of skills, and 1-2 MCP servers. The Atlassian MCP alone unlocks documentation, user stories, and project management. Add a logging MCP and a browser tool, and you've got debugging and integration testing covered too.

The barrier to entry is low. Most activities need nothing beyond the agent itself. Start with the defaults, add MCP servers as you hit real needs, and layer in skill bundles when you want more structure. You don't need the full setup on day one — grow it as you go.
