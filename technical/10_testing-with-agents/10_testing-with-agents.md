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
