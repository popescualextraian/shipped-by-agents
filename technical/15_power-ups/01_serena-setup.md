# Serena: Giving Your Agent a Developer's Eyes

## The Problem with Grep

When your agent needs to understand a function, it searches for the name. It runs something like `grep "processOrder"` across your codebase. It finds the definition — but also every log message that mentions it, every comment that references it, every string that contains it. Ten results come back, maybe three are relevant.

You wouldn't work that way. In your IDE, you Ctrl+click a function and go straight to its definition. You right-click "Find Usages" and get only real references — no false positives. Your IDE understands the code structure, not just the text.

**Serena gives your agent that same capability.**

[Serena](https://github.com/oraios/serena) is an open-source MCP server by Oraios AI. It wraps language servers (the same engines that power your IDE's intelligence) and exposes their capabilities as tools your AI agent can call. Instead of grep and string matching, your agent gets symbol-level operations — the same precision you expect from an IDE.

If you haven't encountered MCP before: it's a standard protocol that lets AI agents call external tools. Think of it as a plugin system — you register an MCP server, and the agent gets new tools automatically. Serena is one such plugin.

Serena supports 42+ languages beyond Python and Java — TypeScript, Go, Rust, C#, and many more. See the [full list in the docs](https://oraios.github.io/serena/).

| Without Serena | With Serena |
|---|---|
| `grep "functionName"` — matches everywhere | `find_symbol` — straight to the definition |
| Read entire file to understand a class | `get_symbols_overview` — structure at a glance |
| String replace and hope nothing breaks | `rename_symbol` — codebase-wide safe rename |
| Guess where something is used | `find_referencing_symbols` — real references only |

---

## Prerequisites

Before you start:

- **`uv` package manager** — install with `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux) or `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows). If you went through Chapter 6, you already have this.
- **Claude Code** installed and working (or GitHub Copilot CLI)
- **A Python or Java project** to test with

---

## What Gets Installed

The setup commands use `uvx` — a tool runner from the `uv` package manager. Here's what actually happens:

1. **`uvx` creates an isolated Python environment** — not in your project, not system-wide. It clones Serena from GitHub, builds it, and installs its dependencies in this sandbox.
2. **Everything is cached locally.** After the first run, `uvx` reuses the cached version. It doesn't re-download every time.
3. **No telemetry, no phone home.** Serena runs entirely on your machine. No external API calls, no analytics, no data leaves your environment during normal operation.
4. **Language servers may download on first use.** Python's Pyright is bundled — no extra download. Java's Eclipse JDT Language Server (~200MB) downloads from GitHub on first activation. TypeScript LSP fetches from npm. After that first download, they're cached locally.

> **Tip for reproducibility:** The commands in this guide track Serena's `main` branch. To pin a specific version, add a tag: `git+https://github.com/oraios/serena@v0.1.4`

---

## Setting Up Serena for a Python Project

### Step 1: Add Serena to Claude Code

Register Serena as an MCP server for your project:

```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project "/path/to/your/project"
```

Replace `/path/to/your/project` with your actual project path.

> **Using GitHub Copilot CLI?** Add Serena to your MCP configuration file instead. The command and arguments are the same — only the registration method differs. Check your tool's docs for how to register MCP servers.

### Step 2: Create the project configuration

Navigate to your project directory and initialize Serena:

```bash
uvx --from git+https://github.com/oraios/serena serena project create --language python
```

This generates `.serena/project.yml` in your project root. It tells Serena which language to use, what files to ignore, and what write access to grant.

### Step 3: Understand the configuration

The generated `.serena/project.yml` looks something like this:

```yaml
language: python
file_encoding: utf-8
ignore_rules:
  - "*.pyc"
  - "__pycache__"
  - ".venv"
```

You can customize ignore rules and other settings here. For personal overrides you don't want committed to git, create a `.serena/project.local.yml` — it takes precedence over `project.yml`.

### Step 4: Tell your agent to use Serena

Installing Serena makes the tools available, but your agent won't automatically prefer them over its built-in tools. Claude Code will still default to Grep and Read unless you nudge it. Add a line to your project's `CLAUDE.md`:

```markdown
When exploring code structure, finding symbol definitions, or looking up references, prefer Serena's MCP tools (find_symbol, find_referencing_symbols, get_symbols_overview, rename_symbol) over Grep/Read for better precision.
```

Without this, the agent will use what it already knows — and you'll wonder why you installed Serena at all.

### One Server Per Project

Serena is **stateful**. It indexes your project's symbols and keeps that state in memory. This means:

- You can't share one Serena instance across multiple projects
- Each project needs its own MCP server registration
- If you work on multiple repos, register Serena separately for each one

Map it per-project. If you have tightly coupled repos that form a single codebase, you can group them — but the default is one server, one project.

---

## Extending to Java

If you also work with Java projects, the setup builds on what you just did. The MCP registration command is the same — only the project configuration differs.

### Extra requirement: JDK

Java support uses the Eclipse JDT Language Server under the hood. You need a JDK installed and `JAVA_HOME` set:

```bash
echo $JAVA_HOME
# Should print your JDK path. If empty, set it before proceeding.
```

### Create the Java project config

```bash
uvx --from git+https://github.com/oraios/serena serena project create --language java
```

### Java-specific settings

Java projects may need additional configuration in the **global** Serena config at `~/.serena/serena_config.yml` (this is separate from the per-project `.serena/project.yml`):

```yaml
ls_specific_settings:
  java:
    gradle_wrapper_enabled: true
    use_system_java_home: true
```

Key options:

| Setting | Default | What it does |
|---|---|---|
| `gradle_wrapper_enabled` | `false` | Use the project's Gradle wrapper |
| `use_system_java_home` | `false` | Use system JAVA_HOME for the language server |
| `maven_user_settings` | `~/.m2/settings.xml` | Path to Maven settings |
| `gradle_user_home` | `~/.gradle` | Gradle home directory |

> **IntelliJ / PyCharm user?** Serena also has a [JetBrains plugin](https://plugins.jetbrains.com/plugin/28946-serena/) that uses IntelliJ's own code analysis engine as the backend instead of Eclipse JDT. Set `language_backend: JetBrains` in your config if you prefer that route.

---

## Verify It Works

Open your project with Claude Code and ask:

```
Use Serena to find all references to <pick a function in your project>
```

You should see the agent call `find_symbol` or `find_referencing_symbols` instead of falling back to grep. The results should be precise — actual code references, not string matches.

**If it doesn't work:**

- Run `claude mcp list` to confirm Serena is registered
- Check that `.serena/project.yml` exists in your project root
- For Java: verify `JAVA_HOME` is set (`echo $JAVA_HOME`)
- For Python: ensure Pyright can resolve your imports (check virtual environment activation)
- For large repos: the initial indexing may take time — give it a minute on first use
- Try asking the agent to `restart_language_server` if things seem stale

---

## The Dashboard

Serena comes with a local web dashboard at `http://127.0.0.1:24282/dashboard/index.html`. It starts automatically with the MCP server — no extra setup needed.

<img src="./serena-dashboard.png![img.png](img.png)" width="100%"/>

The dashboard shows you at a glance: which project is active, which language is configured, what context and modes are running, and how many tools are available. You can also see tool usage stats, the execution queue, and the last execution status — useful for confirming the language server initialized successfully. It's a quick way to verify your setup without going through the agent.

---

## How It Works

Under the hood, Serena is a thin bridge between your agent and a real language server.

```
You → Agent → Serena (MCP tools) → Language Server → Your code
```

When you ask your agent to find references to a function, Serena translates that into a standard LSP request — the same protocol your IDE uses. The language server (Pyright for Python, Eclipse JDT for Java) parses your code, builds a semantic model of symbols, imports, and references, and returns precise results. Serena passes those results back as structured data the agent can act on.

The key insight: Serena doesn't analyze your code itself. It delegates to battle-tested language servers that already understand your language's semantics. It just makes their intelligence accessible to AI agents through MCP, instead of only to IDEs through LSP.

This is why it works out of the box with complex project structures — monorepos, multiple modules, shared libraries. The language server resolves all of that the same way your IDE does.

---

## Why Not a Direct LSP Server?

If Serena wraps a language server, you might wonder: why not wire the language server directly as an MCP tool and skip the middleman?

You can. Several MCP servers do exactly this — [jonrad/lsp-mcp](https://github.com/jonrad/lsp-mcp), [Tritlo/lsp-mcp](https://github.com/Tritlo/lsp-mcp), [mcpls](https://github.com/bug-ops/mcpls), and others. They expose raw LSP operations (hover, go-to-definition, references) as MCP tools. It works for simple projects.

The trouble starts with real-world project structures. Consider a monorepo with multiple Lambda functions and shared libraries:

```
project/
  lambda-orders/
  lambda-payments/
  lambda-notifications/
  commons/
```

Most direct LSP bridges take a single `root_dir`. That means each Lambda folder gets its own LSP instance — and none of them know about `commons/`. Cross-folder imports break. To fix it, you need a `pyrightconfig.json` in each subfolder with `extraPaths` pointing to commons, or a root-level config declaring all source roots. Multiply that by every developer on the team, and it gets tedious fast.

| Approach | Multi-folder setup | Cross-folder imports |
|---|---|---|
| Direct LSP bridge (single root) | One instance per subfolder | Needs per-folder LSP config |
| Direct LSP bridge (parent root) | One instance, but LSP may miss subfolder markers | Hit or miss without explicit config |
| VSCode-based MCP | Works if you use VSCode multi-root workspaces | Native support, but requires VSCode running |
| **Serena** | Point at parent directory, done | Language server resolves imports from project root |

Serena's advantage isn't technical magic — it's **less configuration**. You point it at the project root, it initializes the language server with that root, and the LSP handles the rest. The same way your IDE does when you open the parent folder.

For simple single-folder projects, a direct LSP bridge works fine. For anything with shared code across folders, Serena saves you from fighting LSP configuration.

---

## Enterprise Setup with Docker

The `uvx` approach works well for individual developers, but enterprise environments often need tighter control — sandboxed execution, auditable images, and no surprise network calls.

Serena provides an official Docker image for this: `ghcr.io/oraios/serena`. It bundles Python, Node.js, Rust toolchains, and the Serena server in a single container.

**What Docker gives you over `uvx`:**

| Concern | `uvx` (direct) | Docker |
|---|---|---|
| Isolation | Python venv only — shell commands run on host | Full OS-level container — shell commands are sandboxed |
| File access | Anything the user account can reach | Only explicitly mounted volumes |
| Network control | No restrictions | Docker network policies apply |
| Auditability | Depends on git branch state | Pin the image digest, scan it, mirror to internal registry |
| Language servers | Downloaded on demand from GitHub/npm | Node.js and Rust pre-installed; others still download on first use |

**Basic Docker setup:**

```bash
docker run --rm -i --network host -v /path/to/project:/workspaces/project ghcr.io/oraios/serena:latest serena start-mcp-server --context claude-code --project /workspaces/project
```

**Recommendations for enterprise rollout:**

- **Mirror the image** to your internal container registry instead of pulling from `ghcr.io` directly
- **Pin a specific image digest** rather than using `latest` for reproducibility
- **Pre-download language servers** into the image or a shared volume to avoid runtime network calls
- **Mount only the project directory** — keep the blast radius small

See the [Serena Docker docs](https://oraios.github.io/serena/) for Docker Compose examples and advanced configuration.

---

## Resources

- [Serena on GitHub](https://github.com/oraios/serena) — source code, issues, and releases
- [Serena Documentation](https://oraios.github.io/serena/) — full docs, all supported languages, advanced configuration
- [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/) — package manager setup
- [Serena JetBrains Plugin](https://plugins.jetbrains.com/plugin/28946-serena/) — IntelliJ/PyCharm backend alternative
