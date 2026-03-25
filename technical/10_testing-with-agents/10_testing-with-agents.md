# Chapter 10: Testing with AI Agents

## The Validate Step

You've been building features with your agent — planning, writing code, reviewing. But how does the agent know the feature actually works?

Consider two developers:

**Developer A** has no test suite. She builds a checkout form and asks the agent: "Open the browser and check if this form works." The agent launches Playwright MCP, navigates to the page, fills in the fields, clicks submit, and reports: "The form submits but the confirmation message doesn't appear — there's a JavaScript error in the console." She never left her editor.

**Developer B** inherited 500 Playwright tests from his team. He adds a new API endpoint and asks the agent: "Write tests for this endpoint and make sure the existing tests still pass." The agent generates three new test files, runs the full suite, finds one regression, fixes it, and commits — all while he reviews the PR from the last sprint.

Two worlds. One chapter.

In Chapter 6, you learned the plan-build-validate cycle. This chapter upgrades the **validate** step from "you check it manually" to "the agent checks it for you" — both for UI and API, whether you have an existing test suite or not.

---

## MCP in 30 Seconds

If you haven't read Chapter 15, here's the minimum you need:

**Model Context Protocol (MCP)** is a standard that lets AI agents talk to external tools through a uniform interface. An MCP server is a plugin — you configure it, and the agent discovers new tools automatically.

For this chapter, you need to know:

1. **An MCP server is a plugin.** Configure it in your agent's settings. Tools appear automatically.
2. **Browser MCP servers** let the agent control a real browser — navigate, click, read page content.
3. **API MCP servers** let the agent call your REST endpoints as native tools.

We'll set up specific MCP servers in each section. If you want the full MCP deep dive, see Chapter 15.

---

## When You Have No UI Tests

No Playwright tests. No Selenium. No Cypress. No automation at all. You built a feature, and you need to know if it works.

The usual answer is: open a browser, click around, eyeball it. The agent can do that for you.

Here's the core idea: you connect a **browser MCP server** to your agent. The agent launches a real browser, reads the page through its accessibility tree, clicks buttons, fills forms, and reports what happened. It sees what a screen reader sees — every element, every label, every state change.

**This is ad-hoc validation, not a test suite.** Nothing gets saved. Nothing is repeatable. The agent checks your work right now, in this moment. Think of it as a colleague who opens your branch, tries the feature, and tells you what they found. If you need repeatable tests, keep reading — the next section covers that.

### Browser MCP Options

Three free, open-source tools can give your agent browser access:

| Tool | What It Does | When to Use |
|------|-------------|-------------|
| **Playwright MCP** | Microsoft's official MCP server. Controls browser via accessibility tree. | Default choice — most mature, best docs |
| **Chrome DevTools MCP** | Google's MCP. Connects to a live Chrome via DevTools protocol. | When you need network inspection or performance profiling |
| **Browser MCP** | Chrome extension that exposes your browser to AI agents. | When you need the agent to use your existing logged-in session |

All three are free and open source (Apache 2.0 or equivalent).

### Setup: Claude Code

One command:

```bash
claude mcp add playwright -- npx @playwright/mcp@latest
```

Or add it to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

The agent discovers Playwright's tools automatically on next start — `browser_navigate`, `browser_click`, `browser_type`, `browser_snapshot`, and more.

### Setup: GitHub Copilot

Config file location depends on your environment:

| Environment | Config file |
|-------------|------------|
| **VS Code** | `.vscode/mcp.json` (workspace) |
| **IntelliJ / JetBrains** | `.vscode/mcp.json` (same path, cross-IDE compat) |
| **Copilot CLI** | `~/.copilot/mcp-config.json` (global) |

Add the server:

```json
{
  "servers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "transportType": "stdio"
    }
  }
}
```

### Seeing It in Action

You built a TodoMVC app and want to know if the form works. Here's how the conversation goes:

**You:** "Check if the todo form works — add an item, verify it appears in the list."

The agent gets to work:

```
Agent: [uses browser_navigate → opens http://localhost:3000]
       Page loads. Status: 200 OK.

Agent: [uses browser_snapshot → reads accessibility tree]
       Sees: input field labeled "What needs to be done?", empty todo list.

Agent: [uses browser_type → types "Buy groceries" into the input field]
       [uses browser_press_key → presses Enter]
       Item submitted.

Agent: [uses browser_snapshot → reads updated accessibility tree]
       Sees: todo list now contains one item — "Buy groceries" with an unchecked checkbox.
```

**Agent:** "The todo form works. I typed 'Buy groceries' into the input field, pressed Enter, and the item appeared in the list with an unchecked checkbox. No errors in the console."

That's it. The agent opened a browser, interacted with your app, and told you what happened. You never left your editor.

### Trade-Offs

| Pros | Cons |
|------|------|
| Zero setup — no test framework needed | Token-heavy: ~114K tokens per validation via MCP |
| Agent sees the real app, real state | Not repeatable — no saved test artifacts |
| Good for exploratory / ad-hoc validation | Accessibility tree bloats on complex pages |
| Works with any web app | Sessions degrade after ~15 browser interactions |
| Catches visual/interaction bugs code review misses | Non-deterministic — agent may take different paths |

### Lighter Alternative: Playwright CLI

Microsoft released `@playwright/cli` in early 2026 as a lighter-weight alternative to the MCP server. Instead of streaming the full accessibility tree into context (~114K tokens), CLI saves browser state to disk as compact YAML files (~27K tokens) — a ~4x reduction.

Use CLI for longer sessions or when running many validations in sequence. Use MCP when you need deep page understanding for short workflows.

```bash
npx @playwright/cli --help
```

**Cost awareness:** at current Claude pricing, one browser validation session costs roughly $0.30–0.50 in tokens. Use browser MCP for quick validation during development — to check a form, verify a layout, or confirm a fix. It is not a test suite replacement. When you find yourself validating the same thing twice, that's your signal to write a real test — the next section shows you how.

---

## When You Have (or Want) UI Tests

The previous section was about quick, throwaway validation — the agent opens a browser, pokes around, and tells you what it found. Nothing gets saved.

This section is different. Here the agent still uses browser MCP to **explore** your app, but the output is **real test code** — Playwright specs, Selenium tests, Cypress files — that lives in your repo and runs in CI. Two phases:

1. **Explore** — the agent navigates your app through MCP, reads the accessibility tree, and understands the current UI state.
2. **Generate** — the agent writes standard test code using the framework you already use (or want to adopt).

The result is repeatable. You commit the tests, they run on every push, and they catch regressions long after the agent has moved on.

### Tool Landscape

| Your Stack | MCP Server for Exploration | What the Agent Generates |
|------------|---------------------------|--------------------------|
| **Playwright** | Playwright MCP | `.spec.ts` files using Playwright Test |
| **Selenium** | Selenium MCP (by Angie Jones) | Selenium test code (Java/Python/JS) |
| **Cypress** | Playwright MCP (for exploration) | Cypress `.cy.ts` spec files |

**Selenium MCP setup:** The package is `@angiejones/mcp-selenium`. Add it with:

```bash
claude mcp add selenium -- npx -y @angiejones/mcp-selenium@latest
```

Or in your MCP config:

```json
{
  "mcpServers": {
    "selenium": {
      "command": "npx",
      "args": ["-y", "@angiejones/mcp-selenium@latest"]
    }
  }
}
```

See the [Selenium MCP repo](https://github.com/angiejones/mcp-selenium) for full documentation.

**Why Playwright MCP for Cypress?** Cypress doesn't have its own MCP server. But the agent only needs MCP for exploration — to see what's on the page. It generates Cypress code from what it learned. Playwright MCP works fine for that discovery step.

### Playwright's Built-in AI Agents (v1.56+)

Since version 1.56, Playwright ships three [built-in AI agents](https://playwright.dev/docs/test-agents) that handle the explore-generate-heal cycle without a separate coding agent. These agents use MCP under the hood to control a real browser — the same protocol you set up in the previous section — but they're purpose-built for test automation.

| Agent | What It Does |
|-------|-------------|
| **Planner** | Explores the app, writes a markdown test plan describing each user flow and scenario |
| **Generator** | Converts the plan into `.spec.ts` files with proper selectors and assertions, verifying live as it goes |
| **Healer** | Runs existing tests, detects failures, inspects page snapshots, and auto-patches broken selectors |

#### Setting up Playwright Agents

One command scaffolds everything. Pick your coding agent:

```bash
# For Claude Code
npx playwright init-agents --loop=claude

# For VS Code (Copilot)
npx playwright init-agents --loop=vscode
```

This creates an agents folder with markdown definitions and a seed file:

```
.claude/agents/         # or .vscode/ for Copilot
├── planner.md          # Planner agent instructions
├── generator.md        # Generator agent instructions
├── healer.md           # Healer agent instructions
specs/                  # Test plans (output of Planner)
tests/
└── seed.spec.ts        # Seed file — shared setup copied into every generated test
```

The **seed file** is important. It's your foundation — authentication, test data, base URL, navigation helpers. If the seed is unreliable, nothing the agents produce will be reliable either. Get the seed right first.

#### The three-stage workflow

The agents work in sequence:

**1. Planner → markdown test plan.** Point the Planner at your app. It navigates pages, reads the accessibility tree, and produces a structured markdown plan: "User can log in," "User can add item to cart," "User can checkout." Each scenario lists the steps and expected outcomes.

```bash
# In Claude Code, invoke the planner agent
/agents planner
```

**2. Generator → `.spec.ts` files.** Feed the plan to the Generator. It reads each scenario, navigates the app live to verify selectors, and produces Playwright Test files with real assertions. It doesn't guess — it checks every selector against the actual page.

**3. Healer → auto-fix broken tests.** When tests break (a button moved, a label changed, a page restructured), the Healer runs the failing tests in debug mode. It inspects page snapshots, identifies the broken locator, finds the correct replacement, updates the test code, and re-runs to confirm the fix.

#### Customizing agent behavior

Because agent definitions are plain markdown files, you can edit them:

- Adjust the Planner's exploration depth (how many pages, which flows to prioritize)
- Change the Generator's code style (prefer page objects, use specific assertion patterns)
- Tune the Healer's tolerance (how aggressively to rewrite selectors vs. flagging for human review)

This is one of the strengths of Playwright's approach — the agents are transparent and configurable, not black boxes.

#### When to use built-in agents vs. a general-purpose coding agent

| Scenario | Use Playwright Agents | Use Claude Code / Copilot |
|----------|----------------------|--------------------------|
| Pure Playwright stack, focused on test generation | Yes — fast, specialized, idiomatic output | Overkill |
| Multiple frameworks (Playwright + Selenium + API tests) | No | Yes — handles any framework |
| Need to fix source code when tests fail | No — agents only fix tests | Yes — can fix app code too |
| Self-healing existing test suite | Yes — Healer is purpose-built for this | Can do it, but less specialized |
| Need to coordinate tests with app changes | Partially | Yes — sees full codebase |

You can combine both — let Playwright's Generator create the initial specs, then use your coding agent to refine them alongside your application code. The "record then refine" pattern works especially well: Planner discovers the flows, Generator writes the specs, and your coding agent polishes them to match team conventions.

### The Explore → Generate Workflow

This is what the agent does, regardless of which tool combination you pick:

```mermaid
flowchart LR
    A[Agent explores app\nvia MCP] --> B[Understands\ncurrent UI]
    B --> C[Generates test code\nPlaywright / Selenium]
    C --> D[Runs tests\nin terminal]
    D -->|Pass| E[Commit]
    D -->|Fail| F[Reads error +\nre-explores UI]
    F --> C

    style A fill:#0A2540,color:#fff
    style B fill:#0A2540,color:#fff
    style C fill:#0A2540,color:#fff
    style D fill:#0A2540,color:#fff
    style E fill:#00BFA5,color:#fff
    style F fill:#E8722A,color:#fff
```

The feedback loop (fail → re-explore → regenerate) is where agents shine. A human would alt-tab to the browser, squint at the error, and manually fix the selector. The agent reads the error, snapshots the page, and patches the test in seconds.

### Best Practices for Agent-Generated Tests

**Use stable selectors.** Prefer `getByRole`, `getByTestId`, and `getByLabel` over CSS selectors or XPath. These survive UI redesigns and are accessible by default.

**"Record then refine" pattern.** Let Playwright's codegen (or the agent) capture the raw flow first. Then ask the agent to clean it up — extract page objects, remove waits, add meaningful assertions. The first draft is never the final draft.

**One behavior per test.** Keep tests small and focused. "User can add a todo" is one test. "User can add, edit, and delete a todo" is three tests. Small tests fail with clear messages.

**Always run generated tests before committing.** The agent should execute the tests it wrote. If you're using Claude Code, tell it: "Run the tests and fix any failures before committing." The explore → generate → run → fix loop should complete before code hits your branch.

**Store tests alongside the code they test.** Put `checkout.spec.ts` next to your checkout component, not in a distant `tests/` folder. When the agent modifies a component, it sees the related tests in the same context window.

---

## When You Have No API Tests

Same situation as the UI section, but for APIs. Your agent just built or modified REST endpoints and you need to validate they work. No test suite exists yet. Several strategies can help, from lightweight throwaway scripts to reusable MCP-based approaches.

### The Simplest Approach: Just Ask

Before reaching for any framework, remember: the agent already has a terminal. You can simply ask it to validate an endpoint.

**curl** — zero setup, works everywhere:

```
You: "Hit POST /api/users with a test payload and check the response."
```

The agent runs `curl`, reads the output, and tells you if the status code and body look right. No library, no config.

**Python requests / Java HttpClient / Node fetch** — the agent writes a quick script:

```
You: "Write a Python script that calls GET /api/products and checks we get a 200 with a JSON array."
```

The agent writes the script, runs it, and reports the result. The script is throwaway — but for a quick "does this endpoint work?" check, that's fine.

These approaches are fast and frictionless. Their limitation: nothing gets saved. If you want the agent to validate endpoints *as part of every change it makes*, you need something more structured.

### Strategies Compared

| Approach | Setup | Agent-Friendly? | Repeatable? | Best For |
|----------|-------|-----------------|-------------|----------|
| **curl / inline scripts** | None | High — agents write these naturally | No — throwaway | Quick one-off checks |
| **OpenAPI → MCP Server** | Medium — need OpenAPI spec + FastMCP | Highest — API becomes native tools | Yes — MCP server is reusable | Teams with OpenAPI specs |
| **Postman + MCP** | Medium — need Postman account | Medium | Yes — collections persist | Teams already using Postman |

For quick validation, curl or a script is all you need. For structured, repeatable validation — especially if you have an OpenAPI spec — read on.

### Worked Example: OpenAPI → MCP

If you have an OpenAPI spec, you can auto-generate an MCP server that exposes each endpoint as a tool. The agent then calls your API the same way it calls any other MCP tool — with structured inputs and typed responses.

We'll use [FastMCP](https://gofastmcp.com/integrations/openapi) — it's well-maintained, enterprise-friendly, and works with any OpenAPI spec regardless of your cloud provider.

**1. Install FastMCP:**

```bash
pip install fastmcp httpx
```

**2. Create the MCP server** — one file, a few lines:

```python
# api_mcp_server.py
import os
import httpx
from fastmcp import FastMCP

# Load your OpenAPI spec
spec = httpx.get("https://api.example.com/openapi.json").json()

# Create an HTTP client with auth
client = httpx.AsyncClient(
    base_url="https://api.example.com",
    headers={"Authorization": f"Bearer {os.environ['API_TOKEN']}"}
)

# Generate the MCP server — every endpoint becomes a tool
mcp = FastMCP.from_openapi(openapi_spec=spec, client=client, name="My API")

if __name__ == "__main__":
    mcp.run()
```

By default, every endpoint in the spec becomes an MCP tool. FastMCP handles path parameters, query strings, request bodies, and headers automatically.

**3. Control what the agent can access.** Enterprise APIs have endpoints the agent shouldn't touch. Use route maps to exclude admin, internal, or destructive endpoints:

```python
from fastmcp.server.openapi import RouteMap, MCPType

mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    route_maps=[
        RouteMap(methods=["GET"], pattern=r"^/api/.*", mcp_type=MCPType.TOOL),
        RouteMap(pattern=r"^/admin/.*", mcp_type=MCPType.EXCLUDE),
        RouteMap(tags={"internal"}, mcp_type=MCPType.EXCLUDE),
    ],
)
```

This gives the agent read access to your API while keeping admin and internal routes off-limits.

**4. Configure in Claude Code:**

```bash
claude mcp add my-api -- python api_mcp_server.py
```

**5. Configure in Copilot:**

```json
{
  "servers": {
    "my-api": {
      "command": "python",
      "args": ["api_mcp_server.py"],
      "transportType": "stdio"
    }
  }
}
```

**6. Agent calls endpoints as MCP tools.** It sends a request, reads the response, and validates status codes and payloads — all within the conversation.

> **Note:** FastMCP's docs are clear that auto-converted OpenAPI servers work best for validation and prototyping. For production-critical agent workflows, consider curating which endpoints are exposed and adding meaningful descriptions.

**Alternative:** The [AWS OpenAPI MCP Server](https://awslabs.github.io/mcp/servers/openapi-mcp-server) (TypeScript) is part of the AWS Labs MCP monorepo and creates tools from endpoints at runtime with Cognito auth, caching, and observability built in. A good fit for teams already on AWS.

### Challenges

| Challenge | What to Watch For | Mitigation |
|-----------|------------------|------------|
| **Authentication** | Tokens, API keys, OAuth flows | Pass via env vars or MCP server config. NEVER hardcode in prompts or MCP configs committed to git. |
| **Stateful APIs** | Create → Read → Update → Delete chains | Agent must sequence calls correctly. Prompt it with the expected order. |
| **Environment isolation** | Dev vs staging vs prod | Configure base URL per environment. Warn about prod side effects. |
| **Data setup/teardown** | Tests need seed data, cleanup after | Use factory endpoints or setup scripts. Agent should clean up what it creates. |
| **Rate limiting** | Agent may hammer endpoints rapidly | Add rate-limit awareness in agent instructions (e.g., "wait 1s between calls"). |

**Passing credentials safely.** Use environment variables in your MCP server config — never inline secrets:

```json
{
  "servers": {
    "my-api": {
      "command": "node",
      "args": ["./api-mcp-server/index.js"],
      "env": {
        "API_BASE_URL": "http://localhost:3000",
        "API_KEY": "${MY_API_KEY}"
      },
      "transportType": "stdio"
    }
  }
}
```

Set `MY_API_KEY` in your shell environment or `.env` file (which should be in `.gitignore`). The MCP config references the variable — the secret never touches version control.

---

## When You Have (or Want) API Tests

Your team has an existing API test suite — or plans to build one. The agent writes, runs, and maintains tests in your chosen framework. This mirrors the UI testing workflow from the previous section, but for APIs: the agent understands your endpoints (via specs or MCP), generates test code, runs it, and fixes failures.

### Tool Landscape

| Your Stack | MCP Integration | What the Agent Does |
|------------|----------------|-------------------|
| **Playwright API tests** | Playwright MCP | Generates `request` context tests in `.spec.ts` |
| **Postman** | Postman MCP Server | Creates/updates collections, test scripts, runs via Newman |
| **pytest + requests** | OpenAPI MCP (for understanding) | Generates Python test functions |
| **Jest + supertest** | OpenAPI MCP (for understanding) | Generates JS test files |

### Worked Example: Postman MCP

Many teams already use Postman for API testing. The Postman MCP Server lets your agent interact directly with your Postman workspace — reading existing collections, creating new requests, writing test scripts, and running everything through Newman.

**Setup: Claude Code**

```bash
claude mcp add postman \
  -e POSTMAN_API_KEY=your-api-key \
  -- npx @postmanlabs/postman-mcp-server@latest
```

**Setup: GitHub Copilot**

Config file location depends on your environment:

| Environment | Config file |
|-------------|------------|
| **VS Code** | `.vscode/mcp.json` (workspace) |
| **IntelliJ / JetBrains** | `.vscode/mcp.json` (same path, cross-IDE compat) |
| **Copilot CLI** | `~/.copilot/mcp-config.json` (global) |

```json
{
  "servers": {
    "postman": {
      "command": "npx",
      "args": ["@postmanlabs/postman-mcp-server@latest"],
      "env": {
        "POSTMAN_API_KEY": "${POSTMAN_API_KEY}"
      },
      "transportType": "stdio"
    }
  }
}
```

**The walkthrough**

You built a new `/orders` API with three endpoints: create, get by ID, and list. Your Postman workspace already has collections for `/users` and `/products`, but nothing for orders.

**You:** "Connect to my Postman workspace. See what's already tested, then add tests for the new orders endpoints."

The agent gets to work:

```
Agent: [connects to Postman workspace via MCP]
       Found workspace "ecommerce-api" with 2 collections:
       - Users API (12 requests, all with test scripts)
       - Products API (8 requests, all with test scripts)

Agent: [reads existing collections to understand patterns]
       Your team uses: status code checks, response time assertions,
       JSON schema validation, and environment variables for base URL.

Agent: [creates new collection "Orders API"]
       Adding request: POST /orders — creates an order
       Adding test script: checks 201 status, validates response schema,
       stores order ID in collection variable.

Agent: [adds GET /orders/:id request]
       Test script: checks 200 status, validates order fields match
       what was created, uses stored order ID from previous request.

Agent: [adds GET /orders request]
       Test script: checks 200 status, validates array response,
       confirms created order appears in list.

Agent: [runs collection via Newman CLI]
       ✓ POST /orders — 201 Created (142ms)
       ✓ GET /orders/:id — 200 OK (89ms)
       ✗ GET /orders — 200 OK but schema validation failed:
         "totalCount" field is integer, test expected string.

Agent: [fixes the test script to expect integer for totalCount]
       [re-runs collection]
       ✓ All 3 requests passing. Collection saved to workspace.
```

**Agent:** "Done. Created an 'Orders API' collection with 3 requests and test scripts. All tests pass. The collection follows your team's existing patterns — schema validation, environment variables, response time checks. I fixed one schema mismatch in the list endpoint test (totalCount is an integer, not a string)."

The key insight: the agent read your existing collections first. It didn't invent a testing style — it matched what your team already does.

> **Note:** Postman is freemium. The free tier is limited to 1 user and 25 collection runs/month (as of March 2026). Teams will likely need a paid plan ($19+/user/month). The Postman MCP Server code itself is open source, but requires a Postman account and API key.

### The Understand → Generate Workflow

Whether you use Postman, pytest, Jest, or Playwright's API testing, the agent follows the same loop:

```mermaid
flowchart LR
    A[Agent reads\nAPI spec / MCP] --> B[Understands\nendpoints]
    B --> C[Generates test code\nin team's framework]
    C --> D[Runs tests]
    D -->|Pass| E[Commit]
    D -->|Fail| F[Reads error →\nfixes code or test]
    F --> C

    style A fill:#0A2540,color:#fff
    style B fill:#0A2540,color:#fff
    style C fill:#0A2540,color:#fff
    style D fill:#0A2540,color:#fff
    style E fill:#00BFA5,color:#fff
    style F fill:#E8722A,color:#fff
```

The feedback loop is the same as UI testing: fail → read error → fix → retry. The difference is speed. API tests run in milliseconds, so the agent iterates faster. A typical generate-run-fix cycle completes in under a minute.

### Cross-Reference: REST API Testing Skill (Chapter 7)

The REST API testing skill from [Chapter 7](../07_skills-and-agents/07_skills-and-agents.md) is a concrete implementation of this pattern using Hurl files — declarative, lightweight HTTP tests that agents generate naturally. Teams that prefer a minimal, code-free approach to API testing can adopt that skill directly. It pairs well with the OpenAPI → MCP approach from Section 2: the agent reads the spec for understanding, then produces Hurl files instead of framework-specific test code.

---

## The Power Combo: Testing + Logging

Testing tells the agent "it failed." Logging tells the agent "it failed **and here's why**." Put them together, and the agent can find a bug, diagnose its root cause, fix the code, and verify the fix — all without asking you a single question.

This is what makes autonomous debugging loops possible. Without logs, a failing test gives the agent a symptom. With logs, the agent gets the full diagnosis. This section bridges testing (this chapter) with debugging (Chapter 11).

### Two Workflows, One Big Difference

**Without logging — you relay errors (L2):**

```
Agent runs tests → Fails → You read the error
  → You copy-paste server logs to agent → Agent guesses → Maybe fixes
```

You are the bottleneck. Every failure requires you to context-switch, read output, and ferry information back to the agent. The agent waits while you play messenger.

**With logging — autonomous loop (L4):**

```
Agent runs tests → Fails → Agent reads app logs automatically
  → Agent finds stack trace → Diagnoses root cause → Fixes → Re-runs → Pass
```

The agent closes the loop itself. It reads the test failure, checks the application logs, correlates the error, fixes the source code, and re-runs the test. You review the commit, not the process.

### Setting It Up

Three steps to unlock the autonomous loop.

**1. Give the agent access to logs.**

The simplest approach: your app logs to stdout or a file, and the agent reads it with `tail` or `cat`.

- **File-based:** app writes to `logs/app.log`, agent reads with `tail -n 50 logs/app.log`
- **Docker:** agent runs `docker logs <container> --tail 50`
- **Advanced:** connect a log aggregator MCP server so the agent can query structured logs directly

The key requirement is that the agent can read logs without your help.

**2. Create a combined instruction.**

Add this to your `CLAUDE.md` or `.github/copilot-instructions.md`:

```markdown
When a test fails:
1. Read the last 50 lines of the application log
2. Look for errors, stack traces, or warnings near the failure timestamp
3. Diagnose the root cause
4. Fix the code (not the test, unless the test is wrong)
5. Re-run the failing test to confirm the fix
```

This instruction turns a test failure from a dead end into a starting point. The agent knows what to do next without asking.

**3. See it in action — a worked example.**

You ask the agent to run the Playwright tests for your form submission flow. The agent runs them:

- **Test fails:** the submit button click doesn't produce the expected confirmation message. Playwright reports a timeout waiting for the `"Thank you"` text.
- **Agent reads the server log** (`logs/app.log`) and finds: `POST /api/submit returned 500 — TypeError: Cannot read property 'email' of undefined`
- **Agent opens the backend handler** (`routes/submit.js`). The route reads `req.body.email`, but the middleware that parses the request body was never registered for this route.
- **Agent adds the missing middleware**, saves the file.
- **Agent re-runs the failing test.** The form submits, the confirmation message appears. Test passes.

Total time: under a minute. You didn't copy a single error message.

> This is the difference between L2 and L4 maturity in practice. Instead of you being the messenger between the test output and the agent, the agent closes the loop itself. It's one of the most impactful workflow upgrades a team can adopt.

### Going Deeper

This section gives you everything you need to start using the testing + logging combo today. For more advanced strategies:

- **Chapter 11 (Debugging & Troubleshooting)** covers deeper log collection techniques, structured logging, and how agents navigate complex multi-service failures.
- **Chapter 15 (Power-Ups)** covers observability MCP servers that give agents direct access to log aggregators and monitoring tools.

You don't need those chapters to use what you learned here. Start with file-based logs and the five-step instruction above — that alone eliminates most of the back-and-forth in your debugging workflow.

---

## Try It Yourself

Two exercises — one UI, one API. Each follows the same arc: validate ad-hoc, then generate a repeatable test.

### Part A — UI Testing

1. **Set up Playwright MCP.** Add the Playwright MCP server to your agent configuration:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

2. **Ad-hoc validation.** Ask your agent: "Open [https://todomvc.com/examples/react/dist/](https://todomvc.com/examples/react/dist/), add three todos, mark the second one complete, and tell me what you see." The agent should report the state of all three items — two active, one completed.

3. **Generate a repeatable test.** Ask the agent: "Now write a Playwright `.spec.ts` test that does the same thing — adds three todos, completes the second, and asserts the correct state." Save the file.

4. **Run it.** Ask the agent to run the test with `npx playwright test`. Confirm it passes.

### Part B — API Testing

1. **Ad-hoc validation.** Ask your agent: "Send a POST to `https://jsonplaceholder.typicode.com/posts` with a title, body, and userId. Show me the response." The agent should report a `201` status and the created resource with an `id`.

2. **Generate a repeatable test.** Ask the agent: "Write a test that creates a post on JSONPlaceholder and asserts the response status and body." Pick your framework — Playwright API testing, pytest with `requests`, or a Postman collection.

3. **Run it.** Ask the agent to execute the test. Confirm it passes.

### Bonus — The Power Combo

Combine testing with log collection (The Power Combo):

1. Set up a local app with file-based logging.
2. Introduce a deliberate bug (a missing middleware, a wrong status code, a broken database query).
3. Tell the agent: "Run the tests. If anything fails, read the logs, diagnose the issue, and fix it."
4. Watch the agent close the loop — test, read, diagnose, fix, re-test — without your help.

This is the L4 workflow in practice. Once you've seen it work, you won't want to go back.

---

## Resources

### MCP Servers

- [Playwright MCP](https://github.com/microsoft/playwright-mcp) — Microsoft official (Apache 2.0)
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) — Google official
- [Browser MCP](https://browsermcp.io/) — Chrome extension
- [Selenium MCP](https://github.com/angiejones/mcp-selenium) — by Angie Jones
- [Postman MCP Server](https://github.com/postmanlabs/postman-mcp-server) — official (requires Postman account)
- [FastMCP](https://gofastmcp.com/integrations/openapi) — Python, OpenAPI → MCP with route control
- [AWS OpenAPI MCP Server](https://awslabs.github.io/mcp/servers/openapi-mcp-server) — AWS Labs, TypeScript

### Playwright AI

- [Playwright Test Agents (v1.56+)](https://playwright.dev/docs/test-agents) — built-in Planner, Generator, Healer
- [Playwright CLI vs MCP comparison](https://testdino.com/blog/playwright-cli-vs-mcp/) — token cost benchmarks

### Community

- [Playwright MCP burns 114K tokens per test](https://scrolltest.medium.com/playwright-mcp-burns-114k-tokens-per-test-the-new-cli-uses-27k-heres-when-to-use-each-65dabeaac7a0) — MCP vs CLI cost analysis
- [Playwright AI Ecosystem 2026](https://testdino.com/blog/playwright-ai-ecosystem/) — ecosystem overview
- [Postman Agent Mode Guide](https://blog.postman.com/testing-apis-with-postman-agent-mode-a-practical-guide/)
- [Microsoft: The Complete Playwright E2E Story](https://developer.microsoft.com/blog/the-complete-playwright-end-to-end-story-tools-ai-and-real-world-workflows)

### Related Chapters

- [Chapter 3 — Coding with Agents](../03_coding-with-agents/03_coding-with-agents.md) (TDD basics)
- [Chapter 7 — Skills and Agents](../07_skills-and-agents/07_skills-and-agents.md) (REST API testing skill, Hurl)
- [Chapter 11 — Debugging & Troubleshooting](../11_debugging/) (log collection)
- [Chapter 15 — Power-Ups](../15_power-ups/) (MCP overview)

---

## Tool Licensing & Pricing

Every tool in this chapter is free and open source — with one exception.

| Tool | Free? | Open Source? | License | Notes |
|------|-------|-------------|---------|-------|
| Playwright MCP | Yes | Yes | Apache 2.0 | Microsoft official |
| Playwright CLI | Yes | Yes | Apache 2.0 | Lighter-weight alternative |
| Chrome DevTools MCP | Yes | Yes | Open source | Google official |
| Browser MCP | Yes | Yes | Open source | Chrome extension |
| Selenium MCP | Yes | Yes | Open source | By Angie Jones |
| FastMCP | Yes | Yes | Apache 2.0 | Python, OpenAPI integration |
| AWS OpenAPI MCP Server | Yes | Yes | Apache 2.0 | AWS Labs, TypeScript |
| **Postman** | **Freemium** | **No** | **Proprietary** | Free: 1 user, 25 runs/month. Paid: $19+/user/month |
| Postman MCP Server | Yes | Yes | Open source | Requires Postman account + API key |
