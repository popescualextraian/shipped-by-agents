# shipped-by-agents

A developer's guide to AI-assisted and agentic coding.

## Purpose

Training documentation for developers and teams looking to understand, adopt, and get productive with AI coding agents. Each chapter is a standalone Markdown file paired with curated resources.

## Writing Style

- **Simple** — short sentences, plain language, no jargon without explanation
- **Concise** — say it once, say it clearly, move on
- **Practical** — lead with examples, not theory; show don't tell
- **Scannable** — use tables, bullet lists, and diagrams to break up walls of text
- **Direct** — address the reader as "you"; use active voice

## Chapters

| # | Topic | Time | Status |
|---|-------|------|--------|
| 0 | Introduction | 5 min | Done |
| 1 | What AI coding agents are and how they differ from assistants | 20 min | Done |
| 2 | Prompt design, context management, memory, and skills | 30 min | Done |
| 3 | Coding with AI Agents | 45 min | Done |
| 4 | The big picture: architecture of an AI coding agent | 45 min | Done |
| 5 | Benefits, limits, and risks of AI-assisted coding | TBD | Pending |
| 6 | From Level 0 to Level 1: your first real agent workflow | 45 min | Done |
| 7 | Creating reusable prompts, skills, or simple agents | 45 min | Done |
| 8 | Multi-agent workflows: orchestration, state, and human-in-the-loop | 45 min | Done |
| 9 | Automating user story creation | 30 min | Done |
| 10 | Testing with AI Agents | 45 min | Done |
| 11 | Debugging & Troubleshooting | TBD | Pending |
| 12 | Code Review & Refactoring | TBD | Pending |
| 13 | DevOps & CI/CD | TBD | Pending |
| 14 | Spec-Driven Development | TBD | Pending |
| 15 | Power-Ups: tools and enhancements for your agent workflow (MCP overview, Serena) | Varies | In Progress |
| 16 | Integration with external tools and data | TBD | Pending |
| 17 | Architecture & Design | TBD | Pending |
| 18 | Practical workflow examples and productivity tips | TBD | Pending |
| 19 | Building Your Agentic Development Harness | 60 min | Done |

## Quick Paths

| # | Quick Path | Time | Status |
|---|------------|------|--------|
| 1 | Daily Dev Workflow — user stories, docs, diagrams, coding, testing, debugging, review, refactoring | 15 min | Done |

## Conventions

- **Folder structure:** five top-level sections — `quick-paths/`, `technical/`, `repository/`, `process/`, `articles/`
- **Technical chapters:** one folder per chapter inside `technical/` — `technical/NN_short-slug/` (e.g., `technical/01_agents-vs-assistants/`)
- Each chapter folder contains the chapter markdown and any related assets (images, code samples)
- The main chapter file matches the folder name (e.g., `technical/01_agents-vs-assistants/01_agents-vs-assistants.md`)
- **Repository:** the shared repository — `repository/` with subfolders: `ideas/`, `patterns/`, `solutions/`, `lessons-learned/`
- **Process:** one folder per document inside `process/` — `process/NN_<short-slug>/` (e.g., `process/00_shipped-by-agents-process/`)
- **Quick Paths:** one folder per quick path inside `quick-paths/` — `quick-paths/NN_short-slug/` (e.g., `quick-paths/01_daily-dev-workflow/`)
- Quick paths are short, actionable recipes — each section follows: What, Setup, How, Links (official docs + our chapter)
- **Articles:** one folder per article inside `articles/` — `articles/<short-slug>/`
- Every chapter ends with a **Resources** section linking to relevant articles, docs, and tools
- Use ATX headings (`#`, `##`, `###`)
- Code examples in fenced blocks with language tags
- Keep chapters focused — one concept per section, prefer concrete over abstract

## Diagram Color Palette

All diagrams (SVG, Mermaid) use this palette derived from the project brand:

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary | Deep navy | `#0A2540` | Headers, labels, card top bars, pillar backgrounds |
| Accent | Teal | `#00BFA5` | Accent lines, level numbers, highlights, forward arrows |
| Secondary | Orange | `#E8722A` | Forge accent, feedback/return arrows, secondary highlights |
| Card bg | Light blue-gray | `#f7f9fb` | Card and container backgrounds |
| Card border | Light gray | `#e0e6ed` | Card strokes |
| Body text | Slate | `#4a5568` | Descriptions, body copy |
| Muted text | Silver | `#94a3b8` | Italic notes, secondary info |
| Arrow pill bg | Deep navy | `#0A2540` | Bidirectional arrow labels |
| Arrow pill text | Light slate | `#cbd5e1` | Text inside arrow pills |

**Mermaid style tokens** (copy into Mermaid diagrams):
- Node fills: `fill:#0A2540,color:#fff` (dark) or `fill:#f7f9fb,color:#0A2540` (light)
- Accent nodes: `fill:#00BFA5,color:#fff`
- Warning/secondary nodes: `fill:#E8722A,color:#fff`
- Muted/theoretical nodes: `fill:#4a4a4a,color:#fff`

**SVG export:** use `npx sharp-cli -i input.svg -o output.png -- resize 2400` for PNG exports.

**PyCharm compatibility:** reference SVGs with `<img src="./file.svg" width="100%"/>` (not markdown `![]()` syntax).

## Social Media Posts

Process for creating LinkedIn and Facebook posts to promote training content.

### Location and naming

- **Folder:** `social_posts/YYYY-MM-DD-<short-slug>/` — one folder per post
- Each folder contains: `post.md` (text + metadata), `image.png` (visual), and optional `mermaid-source.mmd`
- Legacy flat files (`social_posts/YYYY-MM-DD-slug.md`) exist for older posts

### File template

Each post file follows this structure:

```markdown
# <Post Title>

**Source:** Chapter N — <chapter name> (or "Original idea")
**Created:** YYYY-MM-DD
**Published:** LinkedIn YYYY-MM-DD | Facebook YYYY-MM-DD (or "Not yet")

---

## LinkedIn

<professional variant>

---

## Facebook

<casual/fun variant>
```

### Tone

- **LinkedIn:** professional, insightful, thought-leadership. Practical value and key takeaways.
- **Facebook:** casual, approachable, fun. Conversational, lighter language, humor welcome.

### Process

1. **Ideation** — user provides a topic, or agent suggests one based on chapter content
2. **Draft** — generate both LinkedIn and Facebook variants in a single file
3. **Refine** — iterate until both variants are approved
4. **Save** — store in `social_posts/` with metadata (source, created date)
5. **Publish update** — when posted, update the "Published" line with platform and date
