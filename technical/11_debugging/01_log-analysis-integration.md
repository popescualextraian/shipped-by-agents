# Integrating Remote Log Analysis with AI Agents

Your agent can read files, run tests, and edit code. But when a test fails because of a backend error, or a deployment breaks in staging, the logs are somewhere else — CloudWatch, Datadog, Splunk, Grafana. You're back to context-switching: open the console, craft a query, copy the results, paste them into the conversation.

This chapter covers how to close that gap.

---

## The Problem: Logs Don't Fit in a Prompt

When debugging with an agent, your first instinct might be: "just paste the logs." That works for 20 lines. It doesn't work for real-world log output.

**Why "here is the file" isn't enough:**

| Approach | Problem |
|----------|---------|
| Paste full log output | 10,000 lines = ~40,000 tokens. Your context window is now mostly logs, leaving little room for reasoning |
| Paste a filtered snippet | You're doing the filtering — the agent should be doing this work |
| Point to a log file path | The file is on a remote server. The agent can't `cat` it |
| Export and download locally | Manual process, stale by the time you paste it, still potentially huge |

The core issue is twofold:

1. **Logs are remote.** They live in cloud platforms, not on your local machine.
2. **Logs are big.** Even a single service can generate gigabytes per day. Dumping raw logs into an agent's context window wastes tokens and degrades response quality.

What you need is **structured, filtered, server-side access** — the agent queries the logging platform directly, gets back only the relevant results, and reasons about them within its normal context budget.

---

## How MCP Solves This

If you've read [Chapter 15.2 — MCP Overview](../15_power-ups/02_mcp-overview.md), you know the pattern: MCP servers give your agent tool-based access to external systems. The same approach works for logging platforms.

Instead of pasting logs, the agent calls a tool:

```
Agent → cloudwatch_query_logs({
  log_group: "/aws/lambda/orders-api",
  filter: "ERROR",
  time_range: "last 1 hour",
  limit: 50
}) → returns 50 matching log lines
```

The logging platform handles the heavy lifting — filtering, time-bounding, pagination — and returns only the relevant results. The agent sees 50 lines, not 50,000.

**What this buys you:**

- **Token efficiency** — server-side filtering means only relevant log lines reach the context window
- **Live data** — the agent queries current logs, not stale exports
- **Agent-driven investigation** — the agent decides what to search for, refines queries, follows leads
- **No context-switching** — debugging stays in the IDE

Every major logging platform now has an MCP server. Let's start with a hands-on example, then compare them all.

---

## Deep Dive: AWS CloudWatch

AWS CloudWatch is the most common logging platform for teams running on AWS. Its MCP server is official (from AWS Labs), well-maintained, and covers both log analysis and alarm troubleshooting.

### What You Get

The CloudWatch MCP server provides tools for **root cause analysis** using CloudWatch observability data — not just raw log search:

**Logs tools:**

| Tool | What it does |
|------|-------------|
| `describe_log_groups` | Lists available log groups |
| `analyze_log_group` | Detects anomalies, error patterns, and message patterns within a time range |
| `execute_log_insights_query` | Runs CloudWatch Insights queries (the full query language) |
| `get_logs_insight_query_results` | Retrieves results from an Insights query |

**Metrics tools:**

| Tool | What it does |
|------|-------------|
| `get_metric_data` | Retrieves metric data across any namespace/dimension |
| `get_metric_metadata` | Describes what a metric measures and recommended statistics |
| `analyze_metric` | Determines trend, seasonality, and statistical properties |

**Alarms tools:**

| Tool | What it does |
|------|-------------|
| `get_active_alarms` | Lists currently active alarms |
| `get_alarm_history` | Retrieves historical state changes |
| `get_recommended_metric_alarms` | Suggests alarm configs based on trend analysis |

### Prerequisites

1. **AWS credentials** configured locally — via `aws configure`, environment variables, or an AWS profile
2. **IAM permissions** — the MCP server needs:
   - `cloudwatch:DescribeAlarms`, `cloudwatch:DescribeAlarmHistory`, `cloudwatch:GetMetricData`, `cloudwatch:ListMetrics`
   - `logs:DescribeLogGroups`, `logs:StartQuery`, `logs:GetQueryResults`, `logs:StopQuery`
3. **Python 3.10+** and `uv` (the server is a Python package)

### Setup: Claude Code

```bash
claude mcp add cloudwatch \
  -e AWS_PROFILE=your-profile \
  -e AWS_REGION=eu-west-1 \
  -- uvx awslabs.cloudwatch-mcp-server@latest
```

Or in `.mcp.json` for the whole team:

```json
{
  "mcpServers": {
    "cloudwatch": {
      "command": "uvx",
      "args": ["awslabs.cloudwatch-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "your-profile",
        "AWS_REGION": "eu-west-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

> **Windows note:** Replace `"command": "uvx"` with `"command": "uv"` and `"args"` with `["tool", "run", "--from", "awslabs.cloudwatch-mcp-server@latest", "awslabs.cloudwatch-mcp-server.exe"]`.

### Setup: GitHub Copilot

The config file location depends on your environment:

| Environment | Config file |
|-------------|------------|
| **VS Code** | `.vscode/mcp.json` (workspace) |
| **IntelliJ / JetBrains** | `.vscode/mcp.json` (same path, cross-IDE compat) |
| **Copilot CLI** | `~/.copilot/mcp-config.json` (global) |

```json
{
  "servers": {
    "cloudwatch": {
      "command": "uvx",
      "args": ["awslabs.cloudwatch-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "your-profile",
        "AWS_REGION": "eu-west-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "transportType": "stdio"
    }
  }
}
```

### Setup: Docker (Alternative)

For teams that prefer containerized MCP servers:

```json
{
  "mcpServers": {
    "cloudwatch": {
      "command": "docker",
      "args": [
        "run", "--rm", "--interactive",
        "-v", "~/.aws:/root/.aws",
        "-e", "AWS_PROFILE=your-profile",
        "awslabs/cloudwatch-mcp-server:latest"
      ]
    }
  }
}
```

### Setup: AWS Log Analyzer (Alternative)

AWS also provides a more flexible [Log Analyzer with MCP](https://github.com/awslabs/Log-Analyzer-with-MCP) that supports arbitrary CloudWatch Insights queries. If you need full query control rather than guided troubleshooting, consider this variant.

### A Real Debugging Scenario

You've deployed a new version of your orders API. Tests pass locally, but the staging environment returns 500 errors. Here's how the conversation goes with CloudWatch MCP connected:

```
You: "The orders API is returning 500s in staging. Check the CloudWatch logs
      for /aws/lambda/orders-api in the last 30 minutes."

Agent: [calls cloudwatch log analysis tool]
       → Finds 23 ERROR entries, all with the same pattern:
         "DynamoDB ConditionalCheckFailedException on table orders-v2"

Agent: "The errors are all DynamoDB ConditionalCheckFailedException on the
        orders-v2 table. This happens when a conditional write fails —
        likely a concurrency issue with the new optimistic locking.
        Want me to check the DynamoDB table configuration?"
```

The agent found the root cause in one query. Without MCP, you'd open the AWS console, navigate to CloudWatch, set the time range, type the filter, read through the results, then paste the relevant lines back into the conversation.

### Token Optimization Tips

- **Be specific about time ranges.** "Last 30 minutes" returns far less data than "today."
- **Use the agent's judgment.** Let it refine queries — a first broad search followed by a targeted filter is more efficient than dumping everything.
- **Limit result counts.** Most MCP tools accept a limit parameter. Start with 20–50 results and expand only if needed.
- **Filter by severity.** Ask for ERROR or WARN level first, then broaden if the issue isn't obvious.

### Official Links

- [CloudWatch MCP Server — docs](https://awslabs.github.io/mcp/servers/cloudwatch-mcp-server) — Full tool reference, setup, and IAM permissions
- [awslabs/mcp](https://github.com/awslabs/mcp) — AWS MCP monorepo (CloudWatch, CDK, Cost, Docs)
- [awslabs/Log-Analyzer-with-MCP](https://github.com/awslabs/Log-Analyzer-with-MCP) — Flexible CloudWatch Insights queries
- [CloudWatch MCP Server on PyPI](https://pypi.org/project/awslabs.cloudwatch-mcp-server/)

---

## Platform Comparison

Every major logging platform now has an MCP server. The tables below help you find the right one for your stack.

### Table 1: Platform Support & Access

| Platform | Official MCP? | Maintained by | Remote/Hosted? | Transport |
|----------|:---:|---|:---:|---|
| **AWS CloudWatch** | Yes | AWS Labs | No (local) | stdio |
| **Datadog** | Yes | Datadog | Yes (remote) | HTTP |
| **Elasticsearch / ELK** | Yes | Elastic | Yes (hosted option) | stdio |
| **Splunk** | Yes | Cisco / Splunk | Yes (Splunkbase) | stdio / SSE |
| **Grafana / Loki** | Yes | Grafana Labs | No (local) | stdio |
| **Azure Monitor** | Yes | Microsoft | No (local) | stdio |
| **Google Cloud Logging** | Yes | Google | Yes (managed) | stdio |
| **New Relic** | Yes | New Relic | Yes | stdio |
| **Dynatrace** | Yes | Dynatrace (OSS) | No (local) | stdio |

### Table 2: Capabilities & Features

| Platform | NL to Query? | Log Search | Metrics | Alerts | Key Differentiator |
|----------|:---:|:---:|:---:|:---:|---|
| **AWS CloudWatch** | No | Yes (analysis) | Yes | Yes | Alarm troubleshooting focus |
| **Datadog** | Yes | Yes | Yes | Yes | Richest toolset, modular tool selection |
| **Elasticsearch / ELK** | Via agent | Yes (Query DSL) | No | No | Raw search power, full Query DSL |
| **Splunk** | Yes (NL→SPL) | Yes | Yes | Yes | Enterprise RBAC, input/output guardrails |
| **Grafana / Loki** | Via agent | Yes (LogQL) | Yes (Prometheus) | Yes | Broadest observability stack |
| **Azure Monitor** | Yes (NL→KQL) | Yes | Yes | Yes | Part of broader Azure MCP ecosystem |
| **Google Cloud** | Via agent | Yes | Yes | TBD | IAM + Cloud Audit Logs built in |
| **New Relic** | Yes (NL→NRQL) | Yes | Yes | Yes | 35 tools, deployment impact analysis |
| **Dynatrace** | Via DQL | Yes | Yes | Yes | Full topology mapping + security analysis |

> **"NL to Query"** means the MCP server itself converts natural language to the platform's query language (SPL, KQL, NRQL). "Via agent" means the LLM generates the query syntax directly — still works, but depends on the model knowing the query language.

---

## Platform Quick References

For each platform: what the MCP does, how to configure it, and where to go for details.

> **Copilot config file location** — depends on your environment. See the [CloudWatch setup](#setup-github-copilot) above for the full table. In short: `.vscode/mcp.json` for VS Code and IntelliJ, `~/.copilot/mcp-config.json` for Copilot CLI.

---

### Datadog

Datadog's MCP is a **remote server** hosted by Datadog — no local process to manage. It stands out for **modular toolsets**: you enable only what you need (logs, metrics, traces, dashboards, monitors, incidents) to save context window space.

**Setup: Claude Code**

```bash
claude mcp add datadog \
  --transport http \
  https://mcp.datadoghq.com/sse \
  -H "DD-API-KEY: your-api-key" \
  -H "DD-APPLICATION-KEY: your-app-key"
```

**Setup: GitHub Copilot**

```json
{
  "servers": {
    "datadog": {
      "type": "http",
      "url": "https://mcp.datadoghq.com/sse",
      "headers": {
        "DD-API-KEY": "your-api-key",
        "DD-APPLICATION-KEY": "your-app-key"
      }
    }
  }
}
```

**Key strength:** Modular tool selection — enable only the toolsets you need to minimize context window usage. Supports logs, metrics, traces, dashboards, monitors, incidents, APM, error tracking, and more.

**Official links:**
- [Datadog MCP Server docs](https://docs.datadoghq.com/bits_ai/mcp_server/)
- [Datadog Remote MCP Server blog](https://www.datadoghq.com/blog/datadog-remote-mcp-server/)

---

### Elasticsearch / ELK

The Elastic MCP server exposes the full Elasticsearch Query DSL through a minimal tool set: `list_indices`, `get_mappings`, and `search`. It's not log-specific — it's a general Elasticsearch interface that works equally well for log data in ELK stacks.

**Setup: Claude Code**

```bash
claude mcp add elasticsearch \
  -e ES_URL=https://your-cluster.es.region.aws.elastic-cloud.com \
  -e ES_API_KEY=your-api-key \
  -- npx -y @elastic/mcp-server-elasticsearch
```

**Setup: GitHub Copilot**

```json
{
  "servers": {
    "elasticsearch": {
      "command": "npx",
      "args": ["-y", "@elastic/mcp-server-elasticsearch"],
      "env": {
        "ES_URL": "https://your-cluster.es.region.aws.elastic-cloud.com",
        "ES_API_KEY": "your-api-key"
      }
    }
  }
}
```

**Key strength:** Full Query DSL access — if you know Elasticsearch, there are no limits on what you can query. The agent can generate complex aggregations, filtered searches, and time-range queries.

**Official links:**
- [elastic/mcp-server-elasticsearch](https://github.com/elastic/mcp-server-elasticsearch)
- [Elastic MCP docs](https://www.elastic.co/docs/solutions/search/mcp)

---

### Splunk

Splunk's MCP server converts natural language to SPL (Search Processing Language), with enterprise-grade guardrails: input validation, output sanitization, and admin-controlled tool enable/disable.

**Setup: Claude Code**

```bash
claude mcp add splunk \
  -e SPLUNK_URL=https://your-instance.splunkcloud.com:8089 \
  -e SPLUNK_AUTH_TOKEN=your-token \
  -- uvx splunk-mcp-server
```

**Setup: GitHub Copilot**

```json
{
  "servers": {
    "splunk": {
      "command": "uvx",
      "args": ["splunk-mcp-server"],
      "env": {
        "SPLUNK_URL": "https://your-instance.splunkcloud.com:8089",
        "SPLUNK_AUTH_TOKEN": "your-token"
      }
    }
  }
}
```

**Key strength:** Enterprise RBAC — admins can enable/disable specific tools globally. Input SPL validation and output sanitization provide guardrails against expensive or sensitive queries. Outputs as JSON, CSV, or Markdown.

**Official links:**
- [Splunk MCP Server docs](https://help.splunk.com/en/splunk-cloud-platform/mcp-server-for-splunk-platform/about-mcp-server-for-splunk-platform)
- [splunk/splunk-mcp-server2](https://github.com/splunk/splunk-mcp-server2)
- [Splunk MCP on Splunkbase](https://splunkbase.splunk.com/app/7931)

---

### Grafana / Loki

Grafana offers two MCP servers: **mcp-grafana** (full Grafana stack — dashboards, alerts, Prometheus, Loki, incident management) and **loki-mcp** (lightweight, Loki-only log queries).

**Setup: Claude Code (full Grafana)**

```bash
claude mcp add grafana \
  -e GRAFANA_URL=http://localhost:3000 \
  -e GRAFANA_API_KEY=your-api-key \
  -- npx -y @modelcontextprotocol/server-grafana
```

**Setup: Claude Code (Loki only)**

```bash
claude mcp add loki \
  -e LOKI_URL=http://localhost:3100 \
  -- npx -y @grafana/loki-mcp
```

**Setup: GitHub Copilot — full Grafana**

```json
{
  "servers": {
    "grafana": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-grafana"],
      "env": {
        "GRAFANA_URL": "http://localhost:3000",
        "GRAFANA_API_KEY": "your-api-key"
      }
    }
  }
}
```

**Key strength:** Broadest observability coverage in a single MCP — dashboards, Prometheus metrics, Loki logs, alerting, incidents, and on-call schedules. Use `--disable-<category>` flags to trim tools you don't need. The Loki-only variant is a single tool for teams that just need log search.

**Official links:**
- [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana)
- [grafana/loki-mcp](https://github.com/grafana/loki-mcp)

---

### Azure Monitor

Part of Microsoft's broader Azure MCP server. Covers Log Analytics (KQL queries), resource health, performance metrics, and workbooks. Natural language to KQL conversion is built in.

**Setup: Claude Code**

```bash
claude mcp add azure \
  -- npx -y @azure/mcp@latest server start
```

Uses your Azure CLI credentials — run `az login` first.

**Setup: GitHub Copilot**

```json
{
  "servers": {
    "azure": {
      "command": "npx",
      "args": ["-y", "@azure/mcp@latest", "server", "start"]
    }
  }
}
```

**Key strength:** Integrated into the Azure ecosystem — query Log Analytics, check resource health, retrieve metrics, and manage workbooks through a single MCP server. NL-to-KQL conversion lets you query without knowing KQL syntax.

**Official links:**
- [Azure MCP Server docs](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/tools/azure-monitor)
- [microsoft/mcp](https://github.com/microsoft/mcp)

---

### Google Cloud Logging

Google's observability MCP covers Cloud Logging, Metrics, Traces, and Error Reporting. IAM-based access control and Cloud Audit Logs integration are built in.

**Setup: Claude Code**

```bash
claude mcp add gcloud-observability \
  -- npx -y @google-cloud/observability-mcp
```

Uses your `gcloud` credentials — run `gcloud auth login` first.

**Setup: GitHub Copilot**

```json
{
  "servers": {
    "gcloud-observability": {
      "command": "npx",
      "args": ["-y", "@google-cloud/observability-mcp"]
    }
  }
}
```

**Key strength:** Unified observability (logs, metrics, traces, errors) with Google Cloud IAM for access control. Audit trail built in via Cloud Audit Logs.

**Official links:**
- [@google-cloud/observability-mcp on npm](https://www.npmjs.com/package/@google-cloud/observability-mcp)
- [Cloud Logging MCP reference](https://docs.cloud.google.com/logging/docs/reference/v2_mcp/mcp)

---

### New Relic

The most tool-rich MCP server in this list — 35 tools organized by category. Converts natural language to NRQL, checks alert status, analyzes deployment impact, and identifies probable error causes.

**Setup: Claude Code**

```bash
claude mcp add newrelic \
  -e NEW_RELIC_API_KEY=your-api-key \
  -- npx -y @newrelic/mcp-server
```

**Setup: GitHub Copilot**

```json
{
  "servers": {
    "newrelic": {
      "command": "npx",
      "args": ["-y", "@newrelic/mcp-server"],
      "env": {
        "NEW_RELIC_API_KEY": "your-api-key"
      }
    }
  }
}
```

**Key strength:** Deployment impact analysis and probable cause identification — useful when debugging post-deploy issues. 35 tools covering logs, metrics, alerts, errors, and application performance.

**Official links:**
- [New Relic MCP overview](https://docs.newrelic.com/docs/agentic-ai/mcp/overview/)
- [New Relic MCP tool reference](https://docs.newrelic.com/docs/agentic-ai/mcp/tool-reference/)

---

### Dynatrace

Open-source MCP server that exposes Dynatrace's DQL (Dynatrace Query Language) for logs, events, spans, metrics, and problems. Stands out for full topology mapping and security vulnerability analysis.

**Setup: Claude Code**

```bash
claude mcp add dynatrace \
  -e DT_ENVIRONMENT_URL=https://your-env.live.dynatrace.com \
  -e DT_API_TOKEN=your-token \
  -- npx -y @dynatrace-oss/dynatrace-mcp-server
```

**Setup: GitHub Copilot**

```json
{
  "servers": {
    "dynatrace": {
      "command": "npx",
      "args": ["-y", "@dynatrace-oss/dynatrace-mcp-server"],
      "env": {
        "DT_ENVIRONMENT_URL": "https://your-env.live.dynatrace.com",
        "DT_API_TOKEN": "your-token"
      }
    }
  }
}
```

**Key strength:** Full topology awareness — the agent can see how services connect, trace requests across microservices, and correlate log entries with deployment events and security vulnerabilities.

**Official links:**
- [dynatrace-oss/dynatrace-mcp](https://github.com/dynatrace-oss/dynatrace-mcp)
- [Dynatrace MCP Server blog](https://www.dynatrace.com/news/blog/dynatrace-mcp-server-allow-ai-interact-dynatrace-access-production-insights/)

---

## Best Practices

### Token Optimization

Log data is the easiest way to blow through your context window. These patterns help:

1. **Enable only what you need.** Datadog lets you pick toolsets. Grafana lets you disable categories. Don't load 35 tools when you need 3.
2. **Filter server-side.** Always specify time ranges, severity levels, and search terms in the query — don't fetch everything and let the agent filter.
3. **Start narrow, then broaden.** Ask for errors in the last 30 minutes before querying the full day. Let the agent refine iteratively.
4. **Limit result counts.** Most MCP tools accept limits. Start with 20–50 results. You can always request more.

### Security

Your agent is now one tool call away from your production logs. Treat this like any other production access — with guardrails.

**Use read-only credentials. Always.**

This is the single most important rule. Your agent needs to *read* logs, not write, delete, or modify anything. Every platform supports this:

| Platform | How to enforce read-only |
|----------|------------------------|
| **AWS CloudWatch** | Create an IAM user/role with only `logs:Describe*`, `logs:Get*`, `logs:StartQuery`, `logs:GetQueryResults`, `cloudwatch:Describe*`, `cloudwatch:GetMetricData`, `cloudwatch:ListMetrics`. No `Put*`, `Delete*`, or `Create*` permissions. |
| **Datadog** | Generate an API key + app key pair where the app key has only the `logs_read` scope. Avoid keys with `logs_write_*` or admin scopes. |
| **Elasticsearch** | Create a dedicated user with the `viewer` or `read_only` built-in role. Or use a custom role limited to `read` on specific indices. |
| **Splunk** | Assign the `user` role (read-only) rather than `power` or `admin`. Use Splunk's MCP-level tool enable/disable to restrict further. |
| **Grafana** | Use a service account with the `Viewer` role. For Loki-only access, restrict the datasource permissions. |
| **Azure Monitor** | Assign the `Log Analytics Reader` RBAC role on the workspace. No `Contributor` or `Owner`. |
| **Google Cloud** | Grant `roles/logging.viewer` and `roles/monitoring.viewer`. Not `logging.admin`. |
| **New Relic** | Create a user API key with the `Read only` base role. |
| **Dynatrace** | Generate an API token with only `Read logs`, `Read metrics`, `Read problems` scopes. No write scopes. |

> **Why this matters:** An agent with write access to your logging platform could accidentally delete log groups, modify alerts, or create expensive queries that impact your bill. Read-only credentials make this impossible.

**More security practices:**

1. **Dedicated service accounts.** Don't reuse your personal credentials. Create a service account or API key specifically for the MCP server. This makes it easy to rotate, audit, and revoke.
2. **Don't commit tokens.** Use environment variables, not hardcoded values. If your `.mcp.json` contains secrets, add it to `.gitignore`.
3. **Scope to what you need.** If you only debug one service, limit the credentials to that service's log group / index / namespace. Don't give the agent access to all logs across all environments.
4. **RBAC where available.** Splunk lets admins control which MCP tools are enabled globally. Use this in team environments to prevent agents from running expensive searches.
5. **Audit access.** Google Cloud, Dynatrace, and Datadog provide audit trails for API calls. Enable them — you'll want to know what your agent queried.
6. **Separate prod from dev.** Use different credentials (and ideally different MCP configs) for production vs. staging environments. Your daily debugging should hit staging; prod access should be deliberate.

### Choosing the Right MCP for Your Stack

- **Already on AWS?** Start with CloudWatch MCP — it's official, covers logs and alarms, and uses your existing credentials.
- **Multi-cloud or SaaS observability?** Datadog or New Relic — both are remote servers that work regardless of where your infrastructure runs.
- **Self-hosted ELK?** Elasticsearch MCP gives you full Query DSL access. Pair with Grafana MCP if you use Grafana for dashboards.
- **Enterprise with compliance needs?** Splunk's RBAC and guardrails are purpose-built for controlled environments.
- **Want everything in one place?** Grafana MCP covers the most ground — logs (Loki), metrics (Prometheus), alerts, incidents, on-call.

---

## Resources

- [AWS CloudWatch MCP Server](https://github.com/awslabs/mcp) — Official AWS MCP monorepo
- [AWS Log Analyzer with MCP](https://github.com/awslabs/Log-Analyzer-with-MCP) — Flexible CloudWatch Insights queries
- [Datadog MCP Server](https://docs.datadoghq.com/bits_ai/mcp_server/) — Official remote MCP server
- [Elasticsearch MCP Server](https://github.com/elastic/mcp-server-elasticsearch) — Official Elastic integration
- [Splunk MCP Server](https://github.com/splunk/splunk-mcp-server2) — Official Splunk MCP with enterprise guardrails
- [Grafana MCP Server](https://github.com/grafana/mcp-grafana) — Full Grafana observability stack
- [Grafana Loki MCP](https://github.com/grafana/loki-mcp) — Lightweight Loki-only log queries
- [Azure MCP Server](https://github.com/microsoft/mcp) — Azure Monitor, Log Analytics, and more
- [Google Cloud Observability MCP](https://www.npmjs.com/package/@google-cloud/observability-mcp) — Cloud Logging, Metrics, Traces
- [New Relic MCP](https://docs.newrelic.com/docs/agentic-ai/mcp/overview/) — 35-tool observability MCP
- [Dynatrace MCP](https://github.com/dynatrace-oss/dynatrace-mcp) — Open-source, topology-aware observability
- [Chapter 15.2 — MCP Overview](../15_power-ups/02_mcp-overview.md) — MCP fundamentals and server catalog
- [MCP Observability Best Practices](https://www.merge.dev/blog/mcp-observability) — Patterns for monitoring MCP server usage
