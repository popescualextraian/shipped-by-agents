# Two Roads to Agentic Coding: Competence Centers vs. Autonomous Agents

Everyone is experimenting with AI coding tools. Few are scaling them.

The gap between "some developers use Copilot" and "AI agents ship production code daily" is enormous. Most organizations are stuck in the middle — running pilots, debating tool choices, writing policy documents that no one reads.

Two companies have crossed that gap, and they did it in completely different ways.

**EPAM**, a 50,000-engineer services company, built an enablement machine — competence centers, maturity models, playbooks, and partnerships. Their bet: give teams the right frameworks, and adoption scales itself.

**Stripe**, a product company processing over $1 trillion in payments annually, built autonomous coding agents from scratch. Their agents write code, open pull requests, and pass CI — with no human interaction during the process. Their bet: invest deep in custom infrastructure, and the payoff compounds.

Both approaches work. But they work for different reasons, in different contexts, and with different trade-offs. If you're a CTO or engineering leader deciding how to adopt agentic coding, picking the wrong model will cost you months and millions.

This article breaks down both models, compares them head-to-head, and gives you a clear framework for choosing.

---

## The Enablement Model: EPAM's Competence Center Approach

EPAM's challenge is unique among engineering organizations. They don't have one codebase. They have hundreds — one for every client engagement. Their engineers rotate across projects, technologies, and domains. Any AI adoption strategy needs to work across all of that.

Their answer is **AI/Run**, a comprehensive framework that operates at three levels: organization, team, and individual.

### The AI Center of Excellence

At the core of EPAM's model sits a lean **AI Center of Excellence (CoE)** — roughly 5 people. This is not a centralized delivery team that builds features for others. It's a knowledge loop. The CoE evaluates new tools, develops adoption playbooks, and creates reusable artifacts that teams can pick up and run with.

The CoE's core activities:

- **Evaluate** — continuously test new AI tools and models as they emerge
- **Translate** — turn research findings into practical engineering guidance
- **Package** — create Day-1 and Day-30 playbooks that teams can follow independently
- **Measure** — track adoption through proficiency analytics and productivity dashboards

The key insight: the CoE doesn't do the work. It makes the work possible. Teams adopt AI tools themselves, following playbooks and supported by champions within their ranks.

### Maturity Levels

EPAM maps every team against an **L0–L3 maturity framework**:

| Level | Description | Typical behavior |
|-------|-------------|-----------------|
| L0 | No adoption | No AI tools in daily workflow |
| L1 | Individual experimentation | Some devs use Copilot or ChatGPT ad hoc |
| L2 | Team-level integration | AI tools embedded in team workflows, prompt libraries shared |
| L3 | Agentic workflows | AI agents handle defined tasks autonomously, humans review |

This mapping matters because it prevents the most common adoption mistake: treating every team the same. An L0 team needs awareness and access. An L2 team needs agent frameworks and governance. The CoE tailors its support accordingly.

### The Tool Stack

Rather than building everything in-house, EPAM combines proprietary and partner tools:

- **CodeMie** — EPAM's own SDLC-native agentic platform, available as VS Code and IntelliJ plugins. It provides context-aware intelligence, agent orchestration, and enterprise governance features.
- **Cursor partnership** — In January 2026, EPAM announced a strategic partnership with Cursor. The combination: Cursor's AI-native IDE with agentic workflows, plus EPAM's reference rulesets, curated context, training programs, and productivity measurement.
- **ELITEA and DIAL** — Additional proprietary platforms for broader AI orchestration beyond coding.

The philosophy is pragmatic. Build what you must (CodeMie for enterprise-specific needs), partner where it makes sense (Cursor for the IDE layer), and let teams choose what works.

### Results

EPAM's EngX GenAI Adoption program has demonstrated measurable outcomes across 40+ engineering teams:

- **15–50% efficiency gains** depending on the team and task type, with an average improvement of 42%
- **23% increase** in engineer skill assessments
- **18% reduction** in code review and rework time
- **500% ROI** within one year for the program investment
- One insurance client reduced migration analysis costs from **$75,000 to $550 per instance**, saving $7.45 million

### Why This Model Fits Service Companies

EPAM's model is built for the realities of outsourcing:

1. **Engineer rotation** — Playbooks and maturity models travel with teams across engagements. Custom-built agent infrastructure doesn't.
2. **Client diversity** — Different clients have different tech stacks, security requirements, and governance needs. A framework-based approach adapts. A fixed agent architecture breaks.
3. **Sellable methodology** — AI/Run isn't just internal. EPAM offers it to clients, helping them stand up their own CoEs. The enablement model is the product.
4. **Lower upfront investment** — A 5-person CoE plus tool partnerships costs a fraction of building a custom agent platform. The ROI timeline is shorter.

---

## The Build Model: Stripe's Autonomous Agents

Stripe's situation is the opposite of EPAM's. One company. One massive codebase — hundreds of millions of lines of Ruby with Sorbet typing, no Rails, and vast homegrown libraries that no pre-trained model has ever seen. Engineers don't rotate across codebases. They go deep on one.

Stripe didn't adopt someone else's AI coding tool. They built their own.

### Minions: One-Shot Coding Agents

Stripe's internal agents are called **Minions**. They are fully autonomous, one-shot coding agents. An engineer posts a task description in a Slack thread. A Minion picks it up, writes all the code, runs CI, and opens a pull request. No human interaction during the process. Engineers review every PR before merge.

The numbers: **1,000+ pull requests merged per week**, entirely written by AI agents.

Minions handle migrations, refactoring, alert responses, and routine maintenance. Engineers frequently spin up multiple Minions in parallel — especially valuable during on-call rotations when a single alert might require changes across several services.

### Blueprints: Deterministic Rails Around Creative AI

The core architectural insight is what Stripe calls **Blueprints** — orchestration flows that alternate between deterministic code nodes and open-ended LLM agent loops.

Here's what that means in practice: a Blueprint doesn't just say "write code to fix this." It defines a sequence of steps. Some steps are creative — the LLM writes code, reasons about the problem, explores solutions. Other steps are hardcoded gates — linting, type checking, test execution, git operations. The agent cannot skip these gates.

This pattern is captured in Stripe's most quotable insight: **"The walls matter more than the model."**

Reliability doesn't come from picking the best LLM. It comes from the scaffolding you build around it. A mediocre model inside a well-designed Blueprint will outperform a frontier model with no guardrails.

### Toolshed: 400+ Tools via MCP

Minions connect to internal systems through **Toolshed**, a central MCP (Model Context Protocol) server hosting over 400 internal tools. These span code search, documentation, ticket management, deployment systems, and more.

But here's the critical detail: the orchestrator never exposes all 400 tools at once. It does **deterministic prefetching** — scanning the task prompt for links and keywords, pulling relevant documentation and tickets, and curating a surgical subset of roughly 15 tools per run. This keeps the agent focused and reduces hallucination.

### Isolation and Security

Every Minion run gets its own **devbox** — an isolated VM identical to what human engineers use, but cut off from production and the internet. Devboxes spin up in approximately 10 seconds. MCP enables cryptographic permission enforcement at the protocol level.

For a company processing over $1 trillion in payments, this isolation isn't optional. It's existential. A coding agent with production access in a financial services company would be a regulatory nightmare.

Agents get at most **2 CI rounds** to produce a passing PR. If they can't get it right in two attempts, the task goes back to a human. This constraint prevents runaway compute costs and ensures agents don't waste time on tasks beyond their capability.

### Why This Model Fits Product Companies

Stripe's model makes sense when you have:

1. **One codebase, forever** — The massive investment in custom tooling (Blueprints, Toolshed, devbox integration) pays off because it's amortized across every task, every day, indefinitely. Service companies can't justify this for a single engagement.
2. **Deep institutional context** — Stripe's codebase uses homegrown libraries that no public model understands. Custom tool integration (400+ internal tools via MCP) bridges that gap. Generic AI coding tools would struggle.
3. **Engineering culture that builds** — Stripe's DNA is building infrastructure. They forked Block's open-source Goose framework and rewrote the orchestration layer. Not every company has the talent or appetite for this.
4. **High-value repetitive tasks** — Migrations, refactoring, and alert responses across hundreds of millions of lines of code generate enormous leverage. 1,000+ PRs per week is transformative at Stripe's scale.

---

## Head-to-Head Comparison

| Dimension | EPAM (Enablement) | Stripe (Build) |
|-----------|-------------------|----------------|
| **Core unit** | Center of Excellence (5 people) | Custom agent platform (engineering team) |
| **Philosophy** | Enable humans to use AI better | Build AI that works autonomously |
| **Tooling strategy** | Partner + build (Cursor, CodeMie) | Build + fork (Goose, Blueprints, Toolshed) |
| **Governance** | Maturity models, playbooks, dashboards | Deterministic gates, isolation, CI constraints |
| **Agent autonomy** | Human-in-the-loop, AI-assisted | Fully autonomous, human reviews output |
| **Scale mechanism** | Frameworks replicate across teams/clients | Infrastructure serves one codebase deeply |
| **Investment** | Lower upfront, ongoing program costs | High upfront, lower marginal cost per task |
| **Time to first value** | Weeks (Day-1 playbooks) | Months (build + integrate agent infrastructure) |
| **Codebase assumption** | Multiple, diverse, rotating | Single, massive, permanent |
| **Key metric** | 42% average efficiency improvement | 1,000+ autonomous PRs merged per week |
| **Risk profile** | Lower — humans remain in control | Higher — autonomous agents in a payments company |

### The Fundamental Trade-Off

EPAM's model trades depth for breadth. It works across any tech stack, any client, any team maturity level. But it relies on humans to do the actual coding — AI assists, it doesn't replace the hands on the keyboard.

Stripe's model trades breadth for depth. It works spectacularly in one context — Stripe's codebase — but requires massive custom investment. The payoff is that AI does the coding, and humans shift to review and direction-setting.

---

## When to Use Which

This is not a matter of preference. Your organizational context determines which model fits.

### Choose the Enablement Model (EPAM-style) when:

- **You serve multiple clients or manage multiple codebases.** Frameworks and playbooks travel across contexts. Custom agent infrastructure doesn't.
- **Your engineers rotate across projects.** A maturity model and shared prompt libraries create consistency. Custom tooling creates lock-in to a specific codebase.
- **You need fast, measurable wins.** A CoE with Day-1 playbooks can show productivity gains in weeks. Building custom agents takes months before the first PR merges.
- **Your engineering culture is adopt-and-adapt, not build-from-scratch.** Not every organization has the appetite (or talent pool) to fork open-source frameworks and build orchestration layers.
- **You want to sell AI adoption as a service.** If you're a consulting or outsourcing company, the enablement model is both your internal strategy and your client offering.

### Choose the Build Model (Stripe-style) when:

- **You have one large, long-lived codebase.** The investment in custom agent infrastructure compounds over time. Every task the agent handles is a return on that investment.
- **Your codebase has deep institutional knowledge that public models don't understand.** Homegrown frameworks, custom libraries, internal APIs — if your code is unique, you need custom tool integration.
- **You have the engineering talent to build and maintain agent infrastructure.** This is not a weekend project. Stripe built Blueprints, Toolshed, devbox integration, and MCP-based security. You need a dedicated team.
- **You have high-volume repetitive tasks.** Migrations, refactoring, and maintenance across a massive codebase generate the most leverage. If your agents don't have thousands of tasks to run, the investment doesn't pay off.
- **You can tolerate a longer time to value.** Months of infrastructure investment before the first autonomous PR. But once it works, it works at 1,000+ PRs per week.

### The Decision Matrix

| Your situation | Recommended model |
|---------------|-------------------|
| Service/outsourcing company | Enablement |
| Product company, < 50 engineers | Enablement (with lighter tooling) |
| Product company, 50–500 engineers | Hybrid — CoE + selective agent automation |
| Product company, 500+ engineers, single codebase | Build |
| Multiple products, shared platform | Hybrid — Build for the platform, Enablement for product teams |

---

## The Hybrid Reality

Most organizations aren't purely EPAM or purely Stripe. The real world is messier.

A mid-size product company (200 engineers, one main codebase) probably can't justify building a Stripe-scale agent platform. But they also shouldn't stop at playbooks. The hybrid path:

1. **Start with enablement.** Stand up a small CoE (2–3 people). Evaluate tools. Create playbooks. Get teams to L2 maturity.
2. **Identify high-leverage automation targets.** Find the repetitive tasks that consume the most engineering hours — migrations, dependency updates, boilerplate generation, test writing.
3. **Build narrow agents for those targets.** You don't need 400 tools and a custom orchestration framework. Start with one Blueprint-style workflow for one task type. Use an existing agent framework (Claude Code, Goose, or similar) with custom rules and tool integrations.
4. **Measure ruthlessly.** Track PRs merged, time saved, error rates. If the agent ROI is positive, expand. If not, stay in enablement mode.

The key insight from both models: **adoption without structure fails.** Whether that structure is a maturity model and playbooks (EPAM) or deterministic gates and isolation (Stripe), you need walls. Letting engineers figure it out on their own produces scattered adoption, inconsistent quality, and security gaps.

---

## Key Takeaways

**For CTOs at service companies:**
- Invest in a lean CoE (5 people max) that creates reusable playbooks, not a centralized AI team that builds for others
- Map your teams to maturity levels and tailor support accordingly
- Partner with tool vendors (Cursor, Copilot, Claude Code) rather than building proprietary agent infrastructure
- Make your AI adoption methodology a sellable offering to clients

**For CTOs at product companies:**
- If your codebase is large and unique, generic AI coding tools will underperform. Custom tool integration via MCP is worth the investment.
- "The walls matter more than the model." Invest in deterministic guardrails (linting gates, CI constraints, isolation) before investing in better models.
- Start with high-volume repetitive tasks (migrations, refactoring) where autonomous agents deliver the clearest ROI
- Human review of every AI-generated PR is non-negotiable. Autonomy in generation, human judgment on merge.

**For everyone:**
- The gap between AI experimentation and AI at scale is an organizational problem, not a technology problem
- Structure beats tools. A mediocre tool with a good adoption framework outperforms a frontier tool with no framework.
- Measure everything. Gut feelings about AI productivity are unreliable. Track PRs, cycle time, error rates, and engineer satisfaction.
- Pick your model based on your context — not based on which company's blog post impressed you more

---

## Resources

- [EPAM AI/Run Framework](https://www.epam.com/services/artificial-intelligence/ai-native-engineering)
- [Architecting an AI CoE for Adoption — EPAM](https://www.epam.com/insights/ai/blogs/building-an-ai-engineering-coe-for-ai-adoption)
- [EPAM + Cursor Strategic Partnership](https://www.epam.com/about/newsroom/press-releases/2026/epam-and-cursor-announce-strategic-partnership-to-build-and-scale-ai-native-teams-for-global-enterprises)
- [Minions: Stripe's Coding Agents — Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
- [Minions: Stripe's Coding Agents — Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- [EPAM: Mapping the GenAI Coding Landscape](https://www.epam.com/insights/ai/blogs/ai-agents-for-software-development)
- [Block/Goose — Open-source Agent Framework](https://github.com/block/goose)
