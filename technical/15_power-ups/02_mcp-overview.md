# MCP: Connecting Your Agent to Everything

## The Walled Garden Problem

Your AI agent is powerful — but trapped. It can read files, run shell commands, and edit code. That's it. Need to check a JIRA ticket? Copy-paste. Need to query CloudWatch logs? Switch to the AWS console. Need to look up who's assigned to a PR? Open GitHub in the browser.

You're the bridge between your agent and every other tool you use. Every context switch costs you time and breaks the agent's flow.

**MCP fixes this.**

```mermaid
graph LR
    subgraph before["Without MCP"]
        direction LR
        Y1["You"]
        A1["Agent"]
        Y1 -->|"prompt"| A1
        A1 -->|"reads files,<br/>runs commands"| A1
        Y1 -.->|"copy-paste<br/>context switch"| J1["JIRA"]
        Y1 -.->|"copy-paste<br/>context switch"| G1["GitHub"]
        Y1 -.->|"copy-paste<br/>context switch"| C1["CloudWatch"]
    end

    subgraph after["With MCP"]
        direction LR
        Y2["You"]
        A2["Agent"]
        Y2 -->|"prompt"| A2
        A2 -->|"jira_search"| J2["JIRA"]
        A2 -->|"create_issue"| G2["GitHub"]
        A2 -->|"query_logs"| C2["CloudWatch"]
    end

    style before fill:#f7f9fb,stroke:#e0e6ed,color:#0A2540
    style after fill:#f7f9fb,stroke:#e0e6ed,color:#0A2540
    style Y1 fill:#0A2540,color:#fff
    style A1 fill:#0A2540,color:#fff
    style J1 fill:#4a4a4a,color:#fff
    style G1 fill:#4a4a4a,color:#fff
    style C1 fill:#4a4a4a,color:#fff
    style Y2 fill:#0A2540,color:#fff
    style A2 fill:#00BFA5,color:#fff
    style J2 fill:#00BFA5,color:#fff
    style G2 fill:#00BFA5,color:#fff
    style C2 fill:#00BFA5,color:#fff
```

MCP — the **Model Context Protocol** — is an open standard that lets AI agents call external tools directly. Think of it as a plugin system: you register an MCP server, and your agent gets new tools automatically. A GitHub server gives it `create_issue` and `search_code`. An Atlassian server gives it `jira_search` and `confluence_get_page`. A database server gives it `execute_sql`.

If you went through Chapter 4, you saw the architecture. If you used the Atlassian MCP in Chapter 9, you've already used one. This chapter is the hands-on guide: how the protocol works, what servers are out there, how to set them up, and how to manage them.

---

## How MCP Works

The protocol is simple. Three roles:

| Role | What it does | Example |
|------|-------------|---------|
| **Host** | The application running the agent | Claude Code, GitHub Copilot |
| **Client** | Manages the connection to a server | Built into the host |
| **Server** | Exposes tools the agent can call | GitHub MCP, Serena, Atlassian |

At startup:

1. The host reads your MCP configuration
2. It launches each configured server
3. Each server announces its tools (name, description, parameters)
4. Those tool definitions get added to the agent's context window
5. The agent can now call them like any built-in tool

When the agent calls an MCP tool, the host routes the request to the right server, the server executes it, and the result comes back as a tool response. From the agent's perspective, `jira_search` works exactly like `Read` or `Bash` — it's just another tool.

```mermaid
sequenceDiagram
    participant You
    participant Host as Host (Claude Code)
    participant Client as MCP Client
    participant Server as MCP Server
    participant API as External API

    rect rgb(247,249,251)
        Note over Host,Server: Startup — tool discovery
        Host->>Server: Launch server process
        Server-->>Client: Here are my tools (name, schema)
        Client-->>Host: Tools added to context
    end

    rect rgb(247,249,251)
        Note over You,API: Runtime — tool call
        You->>Host: "Search JIRA for open bugs"
        Host->>Host: Agent decides to call jira_search
        Host->>Client: Tool call: jira_search({query: "..."})
        Client->>Server: Forward request
        Server->>API: JIRA REST API call
        API-->>Server: JSON response
        Server-->>Client: Tool result
        Client-->>Host: Result added to conversation
        Host-->>You: "Found 3 open bugs: ..."
    end
```

### Transports: How Servers Connect

MCP servers connect to hosts through **transports** — the communication channel between them.

**Stdio** (standard input/output) — The host launches the server as a local process and communicates through stdin/stdout. This is the most common transport. The server runs on your machine, starts and stops with your session.

**Streamable HTTP** — The server runs as a web service and the host connects over HTTP. The server can optionally upgrade responses to Server-Sent Events (SSE) for streaming. This is for remote, shared servers — a team-wide MCP server running on your infrastructure, for example.

```mermaid
graph TB
    subgraph stdio["Stdio Transport (local)"]
        direction LR
        H1["Host<br/>(Claude Code)"] -->|"stdin"| S1["MCP Server<br/>(local process)"]
        S1 -->|"stdout"| H1
        S1 -->|"HTTPS"| API1["External API"]
    end

    subgraph http["Streamable HTTP Transport (remote)"]
        direction LR
        H2["Host<br/>(Claude Code)"] -->|"HTTP POST"| S2["MCP Server<br/>(web service)"]
        S2 -->|"HTTP response<br/>or SSE stream"| H2
        S2 -->|"internal"| API2["Backend Service"]
    end

    style stdio fill:#f7f9fb,stroke:#e0e6ed,color:#0A2540
    style http fill:#f7f9fb,stroke:#e0e6ed,color:#0A2540
    style H1 fill:#0A2540,color:#fff
    style S1 fill:#00BFA5,color:#fff
    style API1 fill:#4a4a4a,color:#fff
    style H2 fill:#0A2540,color:#fff
    style S2 fill:#E8722A,color:#fff
    style API2 fill:#4a4a4a,color:#fff
```

Most servers you'll use are stdio. You'll encounter streamable HTTP when your team runs shared MCP servers or when using cloud-hosted services that offer MCP endpoints directly.

> **Historical note:** The MCP spec originally defined a separate HTTP+SSE transport (spec version 2024-11-05). This was replaced by streamable HTTP in the 2025-03-26 spec revision. SSE required long-lived connections and couldn't handle resumable streams. Streamable HTTP uses standard HTTP requests with optional SSE upgrade — simpler, more reliable. Some older servers still use the legacy SSE transport; most clients support both.

---

## The MCP Server Catalog

There are thousands of MCP servers. Here are the ones worth knowing about — battle-tested, well-maintained, and immediately useful.

```mermaid
graph TB
    Agent["Your Agent"]

    subgraph devtools["Development"]
        GitHub["GitHub<br/>PRs, issues, Actions"]
        Serena["Serena<br/>Code intelligence"]
        AzDO["Azure DevOps<br/>Work items, pipelines"]
    end

    subgraph project["Project Management"]
        JIRA["JIRA<br/>Issues, sprints"]
        Confluence["Confluence<br/>Documentation"]
    end

    subgraph infra["Infrastructure & Ops"]
        CW["CloudWatch<br/>Logs, metrics"]
        AzMon["Azure Monitor<br/>Log Analytics"]
        CDK["AWS CDK<br/>Infrastructure"]
    end

    subgraph data["Data & Docs"]
        DB["DBHub<br/>Postgres, MySQL, SQLite"]
        Ctx7["Context7<br/>Live docs"]
        PW["Playwright<br/>Browser automation"]
    end

    Agent --> devtools
    Agent --> project
    Agent --> infra
    Agent --> data

    style Agent fill:#0A2540,color:#fff
    style devtools fill:#f7f9fb,stroke:#e0e6ed,color:#0A2540
    style project fill:#f7f9fb,stroke:#e0e6ed,color:#0A2540
    style infra fill:#f7f9fb,stroke:#e0e6ed,color:#0A2540
    style data fill:#f7f9fb,stroke:#e0e6ed,color:#0A2540
    style GitHub fill:#00BFA5,color:#fff
    style Serena fill:#00BFA5,color:#fff
    style AzDO fill:#00BFA5,color:#fff
    style JIRA fill:#00BFA5,color:#fff
    style Confluence fill:#00BFA5,color:#fff
    style CW fill:#E8722A,color:#fff
    style AzMon fill:#E8722A,color:#fff
    style CDK fill:#E8722A,color:#fff
    style DB fill:#00BFA5,color:#fff
    style Ctx7 fill:#00BFA5,color:#fff
    style PW fill:#00BFA5,color:#fff
```

### GitHub

> PRs, issues, code search, Actions — your entire GitHub workflow without leaving the agent.

**Server:** [github/github-mcp-server](https://github.com/github/github-mcp-server)

**What you get:** Create and manage issues and PRs, search code across repos, monitor GitHub Actions, review Dependabot alerts, manage discussions and notifications.

**Setup (streamable HTTP — recommended):**

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp \
  -H "Authorization: Bearer YOUR_GITHUB_PAT"
```

**Setup (stdio with Docker):**

```bash
claude mcp add github \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=YOUR_PAT \
  -- docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server
```

Your PAT needs at minimum: `repo`, `read:packages`, `read:org` scopes.

**Try it:**
```
Use the GitHub MCP to list open PRs in this repo
```

---

### Atlassian (JIRA + Confluence)

> Search issues, create stories, read Confluence pages — all from within the agent.

**Server:** [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian)

**What you get:** Full JIRA access (search, create, update, transition issues, manage sprints), full Confluence access (search, read, create, update pages), attachment handling.

**Setup:**

```bash
claude mcp add atlassian \
  -e JIRA_URL=https://your-org.atlassian.net \
  -e JIRA_EMAIL=your@email.com \
  -e JIRA_API_TOKEN=your-token \
  -e CONFLUENCE_URL=https://your-org.atlassian.net/wiki \
  -e CONFLUENCE_EMAIL=your@email.com \
  -e CONFLUENCE_API_TOKEN=your-token \
  -- uvx mcp-atlassian
```

Get your API token from [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens).

**Try it:**
```
Search JIRA for open bugs assigned to me
```

Chapter 9 covers a full workflow built on this server — user story creation from Confluence requirements to JIRA tickets.

---

### Serena (Code Intelligence)

> IDE-level code navigation for your agent — go-to-definition, find references, symbol overview.

**Server:** [oraios/serena](https://github.com/oraios/serena)

**What you get:** `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, `rename_symbol` — the same precision your IDE gives you, available to the agent. Supports 42+ languages.

**Setup:**

```bash
claude mcp add serena \
  -- uvx --from git+https://github.com/oraios/serena \
  serena start-mcp-server --context claude-code --project "/path/to/your/project"
```

Then create the project config:

```bash
uvx --from git+https://github.com/oraios/serena serena project create --language python
```

**Try it:**
```
Use Serena to find all references to processOrder
```

For the full setup guide including Java support, Docker, and troubleshooting, see [Chapter 15 — Serena Setup](./01_serena-setup.md).

---

### Playwright (Browser Automation)

> Navigate pages, click buttons, fill forms, take screenshots — browser automation through the agent.

**Server:** [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)

**What you get:** 34 tools including `browser_navigate`, `browser_click`, `browser_type`, `browser_fill_form`, `browser_take_screenshot`, `browser_snapshot`. Uses the browser's accessibility tree by default — faster and more token-efficient than screenshots.

**Setup:**

```bash
claude mcp add playwright -- npx @playwright/mcp@latest
```

**Try it:**
```
Use Playwright to navigate to our staging environment and take a screenshot of the login page
```

---

### Context7 (Live Documentation)

> Up-to-date, version-specific docs injected directly into your agent's context.

**Server:** [upstash/context7](https://github.com/upstash/context7)

**What you get:** Fetches current documentation and code examples from official library sources. No more hallucinated APIs or outdated methods — the agent gets the real docs for the version you're using.

**Setup:**

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

**Try it:**
```
Use context7 to look up the latest React Router API for nested routes
```

---

### Database (Postgres, MySQL, SQLite)

> Query your database directly from the agent — schema exploration, SQL execution, data analysis.

**Server:** [bytebase/dbhub](https://github.com/bytebase/dbhub) — supports Postgres, MySQL, MariaDB, SQL Server, SQLite.

**What you get:** `execute_sql`, `search_objects` (schema exploration). Has a read-only safety mode.

**Setup (Postgres):**

```bash
claude mcp add-json dbhub '{
  "command": "npx",
  "args": ["-y", "@bytebase/dbhub"],
  "env": {
    "DSN": "postgres://user:password@localhost:5432/dbname?sslmode=disable",
    "READONLY": "true"
  }
}'
```

**Setup (SQLite):**

```bash
claude mcp add-json dbhub '{
  "command": "npx",
  "args": ["-y", "@bytebase/dbhub"],
  "env": {
    "DSN": "file:///path/to/database.db",
    "READONLY": "true"
  }
}'
```

> **Tip:** Start with `READONLY: true`. You can always relax it later. An agent with write access to your production database is a decision you want to make deliberately.

**Try it:**
```
Use dbhub to show me the schema of the users table
```

---

### AWS (CloudWatch, CDK, Cost Analysis)

> Query logs, analyze costs, get AWS documentation — without leaving your agent session.

**Server:** [awslabs/mcp](https://github.com/awslabs/mcp) — AWS's official MCP monorepo with servers for multiple services.

**CloudWatch Logs** — Query log groups, filter events, run CloudWatch Insights queries:

```bash
claude mcp add cloudwatch-logs \
  -e AWS_PROFILE=your-profile \
  -- npx -y @awslabs/cloudwatch-logs-mcp-server
```

**AWS CDK** — Help with CDK constructs, best practices, infrastructure-as-code:

```bash
claude mcp add aws-cdk -- npx -y @awslabs/cdk-mcp-server
```

**Cost Analysis** — Query AWS Cost Explorer, analyze spending patterns:

```bash
claude mcp add aws-cost -- npx -y @awslabs/cost-analysis-mcp-server
```

**AWS Documentation** — Search and retrieve AWS docs:

```bash
claude mcp add aws-docs -- npx -y @awslabs/aws-documentation-mcp-server
```

All AWS servers use your local AWS credentials. Pass `AWS_PROFILE` for named profiles, or let the SDK pick up your default credentials.

**Try it:**
```
Use the CloudWatch MCP to show me error logs from the /aws/lambda/orders-api log group in the last hour
```

---

### Azure (Monitor, DevOps, Storage)

> Query Log Analytics, manage Azure DevOps work items, browse storage — your Azure toolkit.

**Azure MCP** — [Azure/azure-mcp](https://github.com/Azure/azure-mcp) — Microsoft's official multi-service MCP server.

**What you get:** Azure Monitor / Log Analytics (KQL queries), Azure Resource Graph, Storage (blobs, containers), Cosmos DB, Resource Management.

```bash
claude mcp add azure-mcp -- npx -y @azure/mcp@latest server start
```

Uses your Azure CLI credentials — run `az login` first.

**Azure DevOps** — [microsoft/azure-devops-mcp](https://github.com/microsoft/azure-devops-mcp) — Work items, repos, pipelines, PRs:

```bash
claude mcp add azure-devops -- npx -y @microsoft/azure-devops-mcp@latest
```

**Try it:**
```
Use the Azure MCP to run a KQL query against our Log Analytics workspace for errors in the last 24 hours
```

---

## Finding More Servers

The catalog above covers the essentials, but thousands more exist. Here's where to look:

| Registry | What it is | Size |
|----------|-----------|------|
| [Official MCP Registry](https://registry.modelcontextprotocol.io/) | The canonical registry, backed by Anthropic, GitHub, Microsoft | ~100 servers (curated, in preview) |
| [Glama](https://glama.ai/mcp/servers) | Largest directory, automated quality scans | 14,000+ servers |
| [PulseMCP](https://www.pulsemcp.com/) | Popularity metrics, marks official vs community | 7,600+ servers |
| [Smithery](https://smithery.ai/) | Has its own CLI, can generate install commands | 2,000+ servers |
| [mcp.so](https://mcp.so/) | Community directory, aggregates from multiple sources | Varies |

**How to evaluate a server:**

1. **Check maintenance** — When was the last commit? Are issues being responded to?
2. **Check tool count** — Each tool adds to your context window. A server with 50 tools might not be worth the token cost
3. **Check permissions** — What does the server need access to? Does it request more than necessary?
4. **Check the source** — Is it from the official vendor (GitHub, AWS, Microsoft) or a community contributor?
5. **Try before you commit** — Add the server, run `/mcp` in Claude Code to verify it loaded, test one tool

---

## Setting Up and Managing Servers

### Configuration Scopes

MCP servers can be configured at different levels:

| Scope | Config location | Shared via git? | Use case |
|-------|----------------|-----------------|----------|
| **Project** | `.mcp.json` (repo root) | Yes | Team tools everyone needs |
| **User** | `~/.claude.json` | No | Your personal servers |
| **Per-session** | `claude mcp add` during session | No | Temporary, testing |

**For Claude Code**, the `claude mcp add` command writes to your project-level `.mcp.json` by default. Add `--global` for user-level config.

**For GitHub Copilot**, MCP config lives in `.vscode/mcp.json` (workspace) or your user-level `mcp.json`.

### Adding a Server

The basic pattern:

```bash
claude mcp add <name> -- <command> [args...]
```

With environment variables:

```bash
claude mcp add <name> -e KEY=value -e KEY2=value2 -- <command> [args...]
```

With HTTP transport:

```bash
claude mcp add --transport http <name> <url> -H "Authorization: Bearer TOKEN"
```

### Verifying Your Setup

After adding a server:

```bash
claude mcp list          # See all registered servers
claude mcp get <name>    # Check a specific server's config
```

Inside a Claude Code session, run `/mcp` to see which servers are connected and what tools they provide.

### Context Window Trade-offs

Every MCP server adds tool definitions to your context window. Each tool definition includes a name, description, and parameter schema. A server with 10 tools might consume 2,000–5,000 tokens — before you've even used it.

**How Claude Code handles this:** When MCP tools exceed about 10% of context, Claude Code switches to **Tool Search** — it loads tool descriptions on demand instead of all at once. You'll see deferred tools listed as names only until the agent needs them.

**Practical limits:**

- 3–5 servers is the sweet spot for most workflows
- Beyond 8–10 servers, you'll notice context pressure even with deferred loading
- If you need many servers, configure them per-project rather than globally — only load what the current project actually needs

---

## Security

Adding an MCP server means trusting it with:

1. **Tool execution** — The server runs code on your machine (stdio) or processes your requests (HTTP)
2. **Credentials** — Many servers need API tokens, database passwords, or cloud credentials
3. **Data access** — The server sees whatever data passes through its tools

```mermaid
graph LR
    subgraph your_machine["Your Machine (trust boundary)"]
        Agent["Agent"]
        Server["MCP Server"]
        Creds["Credentials<br/>.mcp.json"]
        Agent -->|"tool calls"| Server
        Creds -.->|"tokens, keys"| Server
    end

    Server -->|"API calls with<br/>your credentials"| Ext["External Services<br/>GitHub, JIRA, AWS, ..."]

    style your_machine fill:#f7f9fb,stroke:#E8722A,stroke-width:2px,color:#0A2540
    style Agent fill:#0A2540,color:#fff
    style Server fill:#E8722A,color:#fff
    style Creds fill:#4a4a4a,color:#fff
    style Ext fill:#4a4a4a,color:#fff
```

### What to Watch For

**Source verification** — Prefer official servers from the service vendor (GitHub's own server, AWS's own servers, Microsoft's own servers). Community servers can be excellent, but review their code first.

**Credential scope** — Give servers the minimum permissions they need. Use read-only database connections. Create API tokens with limited scopes. Use AWS profiles with restricted IAM roles.

**Network access** — Stdio servers run locally but often make outbound API calls. Know where your data goes. For sensitive environments, audit the server's network behavior.

**Token storage** — MCP config files (`.mcp.json`, `~/.claude.json`) store environment variables including tokens. Don't commit tokens to git. Use environment variable references or secrets managers where possible.

### A Practical Checklist

Before adding a server:

- [ ] Is it from an official or well-known source?
- [ ] Have you reviewed what tools it exposes?
- [ ] Are you giving it minimum necessary credentials?
- [ ] Is the config file in `.gitignore` if it contains secrets?
- [ ] Does your team agree on which servers are approved?

> **Enterprise environments** may need additional controls: approved server lists, Docker-based isolation, network policies. See the [Serena article's Docker section](./01_serena-setup.md#enterprise-setup-with-docker) for an example of containerized MCP deployment.

---

## Key Takeaways

1. **MCP is a plugin system for AI agents.** Servers expose tools, agents call them. One protocol, any service.
2. **Start with one server.** Pick the one that saves you the most context-switching — GitHub, Atlassian, or CloudWatch depending on your daily workflow.
3. **Stdio for local, streamable HTTP for remote.** Most servers are stdio. You'll use HTTP for team-shared or cloud-hosted servers.
4. **Watch the context cost.** Each server adds token overhead. Three to five servers is the sweet spot.
5. **Security is your responsibility.** Review servers before installing. Minimize credential scope. Don't commit tokens.
6. **The ecosystem is huge and growing.** Thousands of servers exist. The registries help you find them; the checklist helps you evaluate them.

---

## Resources

- [Model Context Protocol — Official Specification](https://modelcontextprotocol.io/) — The protocol spec, transport details, and server registry
- [Claude Code — MCP Documentation](https://docs.anthropic.com/en/docs/claude-code/mcp) — Configuring MCP servers in Claude Code
- [GitHub MCP Server](https://github.com/github/github-mcp-server) — Official GitHub integration
- [mcp-atlassian](https://github.com/sooperset/mcp-atlassian) — JIRA and Confluence integration
- [Serena](https://github.com/oraios/serena) — LSP-powered code intelligence
- [Playwright MCP](https://github.com/microsoft/playwright-mcp) — Browser automation
- [Context7](https://github.com/upstash/context7) — Live documentation lookup
- [DBHub](https://github.com/bytebase/dbhub) — Multi-database access
- [AWS MCP Servers](https://github.com/awslabs/mcp) — CloudWatch, CDK, Cost Analysis, AWS Docs
- [Azure MCP](https://github.com/Azure/azure-mcp) — Azure Monitor, Storage, Cosmos DB, Resource Graph
- [Azure DevOps MCP](https://github.com/microsoft/azure-devops-mcp) — Work items, repos, pipelines
- [Chapter 4 — The Big Picture](../04_the-big-picture/04_the-big-picture.md) — MCP architecture overview
- [Chapter 9 — Automating User Story Creation](../09_story-creation/09_story-creation.md) — Atlassian MCP in practice
- [Chapter 15 — Serena Setup](./01_serena-setup.md) — Detailed Serena configuration guide
