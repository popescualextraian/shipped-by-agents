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

**This is ad-hoc validation, not a test suite.** Nothing gets saved. Nothing is repeatable. The agent checks your work right now, in this moment. Think of it as a colleague who opens your branch, tries the feature, and tells you what they found. If you need repeatable tests, that's Section 2.

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

**Cost awareness:** at current Claude pricing, one browser validation session costs roughly $0.30–0.50 in tokens. Use browser MCP for quick validation during development — to check a form, verify a layout, or confirm a fix. It is not a test suite replacement. When you find yourself validating the same thing twice, that's your signal to write a real test (Section 2 covers that).

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

Since version 1.56, Playwright ships three built-in AI agents that handle the explore-generate cycle without a separate coding agent:

| Agent | What It Does |
|-------|-------------|
| **Planner** | Explores the app, writes a markdown test plan describing each flow |
| **Generator** | Converts the plan into `.spec.ts` files with proper selectors and assertions |
| **Healer** | Runs existing tests, detects failures, and auto-patches broken selectors |

These agents are specialized. They know Playwright's API deeply and produce idiomatic test code.

**When to use built-in agents vs. a general-purpose coding agent (Claude Code, Copilot):**

- Use **Playwright's built-in agents** when your stack is Playwright and you want fast, focused test generation with minimal setup.
- Use a **general-purpose coding agent** when you work with multiple frameworks, need to coordinate test code with app code, or want the agent to fix the source code (not just the tests) when something breaks.

You can combine both — let Playwright's Generator create the initial specs, then use your coding agent to refine them alongside your application code.

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
