# Curated Resources — Shipped by Agents

Companion resources for each section of the training. Each entry links to enterprise-grade tutorials, courses, and references — plus the corresponding chapter in our repo.

> **Repo:** [shipped-by-agents](https://github.com/popescualextraian/shipped-by-agents)

---

## 1. Foundations — What AI Coding Agents Are

**Chapters covered:** 0 (Introduction), 1 (Agents vs Assistants)

| Resource | Type | Cost | Description |
|----------|------|------|-------------|
| [Generative AI for Everyone](https://www.coursera.org/learn/generative-ai-for-everyone) — DeepLearning.AI / Coursera (Andrew Ng) | Course | Free audit / Paid cert | Accessible overview of what generative AI is, how it works, and what it can and cannot do — the ideal conceptual foundation. |
| [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/) — DeepLearning.AI (Andrew Ng) | Course | Free | Teaches four core agentic design patterns (Reflection, Tool Use, Planning, Multi-Agent) from first principles in Python — vendor-neutral. |
| [What is a ReAct Agent?](https://www.ibm.com/think/topics/react-agent) — IBM Think | Reference | Free | Authoritative explainer of the ReAct (Reasoning + Acting) framework, the thought-action-observation loop, and how it differs from simple prompting. |
| [AI Coding Tools Comparison 2026](https://www.sitepoint.com/ai-coding-tools-comparison-2026/) — SitePoint | Reference | Free | Comprehensive tool comparison tested in real workflows — great landscape overview. |
| [Choose a Design Pattern for Your Agentic AI System](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) — Google Cloud | Reference | Free | Official architecture guidance for choosing between assistants and autonomous agents. |
| **[Introduction](00_introduction/00_introduction.md)** — shipped-by-agents | Chapter 0 | Free | Why this guide exists, who it's for, and how to use it. |
| **[Agents vs Assistants](01_agents-vs-assistants/01_agents-vs-assistants.md)** — shipped-by-agents | Chapter 1 | Free | The spectrum from autocomplete to autonomous agents, and how the agent loop works. |

---

## 2. Prompt Design & Context Engineering

**Chapters covered:** 2 (Prompt & Context Engineering)

| Resource | Type | Cost | Description |
|----------|------|------|-------------|
| [Anthropic Interactive Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) | Hands-on (Jupyter) | Free | Official Anthropic course — 9 chapters covering prompt design, XML structuring, chain-of-thought, tool use, and agentic prompting. |
| [ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) — DeepLearning.AI + OpenAI | Course | Free | Andrew Ng & Isa Fulford teaching zero-shot, few-shot, and chain-of-thought prompting with hands-on notebooks. |
| [Claude Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) — Anthropic Docs | Reference | Free | Up-to-date official guide covering clarity, examples, XML structuring, extended thinking, and agentic system prompting. |
| **[Prompt Design & Context Engineering](02_prompt-and-context-engineering/02_prompt-and-context-engineering.md)** — shipped-by-agents | Chapter 2 | Free | Write prompts that produce reliable results, and manage what your agent sees. |

---

## 3. Coding with AI Agents

**Chapters covered:** 3 (Coding with Agents), 6 (A Development Workflow)

| Resource | Type | Cost | Description |
|----------|------|------|-------------|
| [Mastering GitHub Copilot for Paired Programming](https://github.com/microsoft/Mastering-GitHub-Copilot-for-Paired-Programming) — Microsoft | Course (GitHub) | Free | Official Microsoft multi-module course covering AI pair programming workflows, context management, and best practices. |
| [Claude Code](https://github.com/anthropics/claude-code) — Anthropic (82K+ stars) | Tool + Docs | Free | The reference implementation for CLI-based agentic coding — includes docs, skills, hooks, and subagent patterns. |
| [Cursor — Complete AI-Powered Software Development Workflow](https://www.udemy.com/course/ai-driven-development-workflow/) — Udemy | Course | Paid | Covers the complete spec-to-deployment workflow with an AI coding agent, including iteration and error handling. |
| **[Coding with AI Agents](03_coding-with-agents/03_coding-with-agents.md)** — shipped-by-agents | Chapter 3 | Free | Use built-in agents, skills, memory, and workflows like plan-first and TDD. |
| **[A Development Workflow](06_a-development-workflow/06_a-development-workflow.md)** — shipped-by-agents | Chapter 6 | Free | Structure your daily dev workflow around AI agents — from setup to shipping. |

---

## 4. The Development Process — Plan, Build, Review

**Chapters covered:** 3 (Coding with Agents), 6 (A Development Workflow) — methodology focus

| Resource | Type | Cost | Description |
|----------|------|------|-------------|
| [Humans and Agents in Software Engineering Loops](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html) — Martin Fowler | Article series | Free | Defines three interaction models (in-the-loop, out-of-the-loop, on-the-loop) and introduces "harness engineering" for governing the plan-build-review cycle. Part of a broader series including [harness engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) and [context engineering for coding agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html). |
| [The Three Developer Loops](https://itrevolution.com/articles/the-three-developer-loops-a-new-framework-for-ai-assisted-coding/) — IT Revolution (Gene Kim & Steve Yegge) | Article | Free | Framework splitting AI-assisted development into inner loop (seconds: task decomposition, verification), middle loop (hours: context, sessions), and outer loop (weeks: architecture, CI/CD). Based on the book *Vibe Coding* (paid). |
| [Spec-Driven Development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) — ThoughtWorks | Article | Free | The methodology of writing structured specs first, then using AI agents to generate code — covering the full spec-implement-validate-refine cycle. Also on the [ThoughtWorks Technology Radar](https://www.thoughtworks.com/en-us/radar/techniques/spec-driven-development). |
| **[Coding with AI Agents](03_coding-with-agents/03_coding-with-agents.md)** — shipped-by-agents | Chapter 3 | Free | Plan-first development, TDD with agents, the build-validate-iterate cycle. |
| **[A Development Workflow](06_a-development-workflow/06_a-development-workflow.md)** — shipped-by-agents | Chapter 6 | Free | Five maturity levels from copy-paste to agent-orchestrated development. |

---

## 5. Architecture of AI Coding Agents

**Chapters covered:** 4 (The Big Picture)

| Resource | Type | Cost | Description |
|----------|------|------|-------------|
| [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/) — DeepLearning.AI (Andrew Ng) | Course | Free | Builds four agent patterns from scratch in Python — Reflection, Tool Use, Planning, Multi-Agent — no framework dependency. |
| [The AI Agent Loop](https://blogs.oracle.com/developers/what-is-the-ai-agent-loop-the-core-architecture-behind-autonomous-ai-systems) — Oracle Developers | Article | Free | Enterprise-grade deep dive into the five-stage agent loop, ReAct pattern, Tree-of-Thoughts, and context management. |
| [State of Agent Engineering Report](https://www.langchain.com/state-of-agent-engineering) — LangChain (2025) | Report | Free | Industry survey (1,340 respondents) on real-world agent architectures, production adoption, tool integration, and model choices. |
| **[The Big Picture](04_the-big-picture/04_the-big-picture.md)** — shipped-by-agents | Chapter 4 | Free | The four-layer architecture: You, Context, Agent (ReAct), Capabilities. |

---

## 6. Building Skills & Custom Agents

**Chapters covered:** 7 (Reusable Prompts, Skills & Agents)

| Resource | Type | Cost | Description |
|----------|------|------|-------------|
| [A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — OpenAI | Guide (PDF) | Free | Official OpenAI guide covering agent design, tool definitions, orchestration patterns, and guardrails — distilled from real deployments. |
| [Claude Code Custom Subagents](https://code.claude.com/docs/en/sub-agents) — Anthropic | Docs | Free | Official documentation for creating custom subagents with dedicated system prompts, tool access, and permissions. |
| [CrewAI](https://github.com/crewAIInc/crewAI) (45.9K+ stars) | Framework | Free | Leading open-source multi-agent orchestration framework for building role-based, collaborative AI agents with reusable tasks and tools. |
| **[Reusable Prompts, Skills & Agents](07_skills-and-agents/07_skills-and-agents.md)** — shipped-by-agents | Chapter 7 | Free | Create custom skills and agents — hands-on with a REST Assured test agent. |

---

## 7. Multi-Agent Workflows

**Chapters covered:** 8 (Multi-Agent Workflows)

| Resource | Type | Cost | Description |
|----------|------|------|-------------|
| [Multi AI Agent Systems with crewAI](https://learn.deeplearning.ai/courses/multi-ai-agent-systems-with-crewai/) — DeepLearning.AI | Course | Free | Andrew Ng + CrewAI founder covering role-playing, memory, guardrails, and multi-agent collaboration patterns. |
| [Introduction to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) — LangChain Academy | Course | Free | Official LangChain course on state management, memory, human-in-the-loop, and checkpointing in graph-based agent workflows. |
| [Agentic AI with LangChain and LangGraph](https://www.coursera.org/learn/agentic-ai-with-langchain-and-langgraph) — Coursera | Course | Paid | Structured course on building agentic AI applications including multi-agent orchestration patterns. |
| **[Multi-Agent Workflows](08_workflows/08_workflows.md)** — shipped-by-agents | Chapter 8 | Free | Orchestrate multi-step workflows with state management and human-in-the-loop. |

---

## 8. Automating User Stories & Enterprise Integration

**Chapters covered:** 9 (Story Creation)

| Resource | Type | Cost | Description |
|----------|------|------|-------------|
| [Atlassian Remote MCP Server](https://www.atlassian.com/platform/remote-mcp-server) — Atlassian | Platform | Free (with Atlassian Cloud) | Official MCP server connecting AI agents to Jira, Confluence, and Compass with OAuth 2.1 and enterprise governance. |
| [atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) — Atlassian (GitHub) | Open Source | Free | Official open-source MCP server for creating/updating issues, searching content, and automating workflows across Jira and Confluence. |
| [Practical Multi AI Agents with crewAI](https://learn.deeplearning.ai/courses/practical-multi-ai-agents-and-advanced-use-cases-with-crewai/) — DeepLearning.AI | Course | Free | Real-world agent applications including automated project planning and content creation at scale. |
| **[Automating User Story Creation](09_story-creation/09_story-creation.md)** — shipped-by-agents | Chapter 9 | Free | Apply skill-building to non-coding tasks — user stories, MCP integration, Atlassian connectivity. |

---

## 9. Testing with AI Agents

**Chapters covered:** 10 (Testing with AI Agents)

| Resource | Type | Cost | Description |
|----------|------|------|-------------|
| [playwright-mcp](https://github.com/microsoft/playwright-mcp) — Microsoft | Open Source | Free | Official Playwright MCP server enabling AI agents to drive browser sessions via structured accessibility snapshots. |
| [The Complete Playwright End-to-End Story](https://developer.microsoft.com/blog/the-complete-playwright-end-to-end-story-tools-ai-and-real-world-workflows) — Microsoft Developer Blog | Article | Free | Official Microsoft guide covering the full Playwright ecosystem including AI-powered workflows and MCP integration. |
| [Playwright E2E Automation with TypeScript, MCP & AI Agents](https://www.udemy.com/course/playwright-e2e-automation-framework-webapidevice-2025/) — Udemy | Course | Paid | Comprehensive course on Playwright automation with MCP server integration and AI-assisted test generation. |
| **[Testing with AI Agents](10_testing-with-agents/10_testing-with-agents.md)** — shipped-by-agents | Chapter 10 | Free | UI validation with Playwright MCP, API testing with FastMCP, maintaining test suites. |

---

## 10. MCP & Power-Ups

**Chapters covered:** 15 (Power-Ups), 11 (Debugging — Log Analysis)

| Resource | Type | Cost | Description |
|----------|------|------|-------------|
| [Introduction to Model Context Protocol](https://anthropic.skilljar.com/introduction-to-model-context-protocol) — Anthropic Skilljar | Course | Free | Anthropic's official MCP course — build servers and clients from scratch in Python, covering tools, resources, and prompts primitives. |
| [MCP Specification & Docs](https://modelcontextprotocol.io/specification/2025-11-25) — Linux Foundation | Reference | Free | The official MCP specification and documentation, maintained by the Linux Foundation. |
| [MCP Reference Servers](https://github.com/modelcontextprotocol/servers) — MCP Steering Group | Open Source | Free | Official reference MCP server implementations plus links to the MCP Registry for discovering community servers. |
| **[MCP Overview](15_power-ups/02_mcp-overview.md)** — shipped-by-agents | Chapter 15.2 | Free | MCP fundamentals, server catalog (GitHub, Atlassian, AWS, Azure, databases), setup and security. |
| **[Serena Setup](15_power-ups/01_serena-setup.md)** — shipped-by-agents | Chapter 15.1 | Free | LSP-powered code intelligence — setup for Python, Java, and enterprise Docker. |
| **[Log Analysis Integration](11_debugging/01_log-analysis-integration.md)** — shipped-by-agents | Chapter 11.1 | Free | Connect your agent to CloudWatch, Datadog, Splunk, Grafana, and more via MCP. |

---

## Quick-Start Bundles

For those who want a structured learning path rather than individual picks:

| Bundle | Covers | Cost |
|--------|--------|------|
| **DeepLearning.AI Agent track** — [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/) + [Multi AI Agent Systems](https://learn.deeplearning.ai/courses/multi-ai-agent-systems-with-crewai/) + [Practical Agents](https://learn.deeplearning.ai/courses/practical-multi-ai-agents-and-advanced-use-cases-with-crewai/) | Foundations through multi-agent orchestration | Free |
| **Anthropic developer path** — [Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) + [Claude Code](https://github.com/anthropics/claude-code) + [MCP Course](https://anthropic.skilljar.com/introduction-to-model-context-protocol) | Prompting, coding, and tool integration | Free |
| **Microsoft practical path** — [Copilot Paired Programming](https://github.com/microsoft/Mastering-GitHub-Copilot-for-Paired-Programming) + [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Coding and testing workflows | Free |
