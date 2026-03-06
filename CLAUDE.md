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
| 3 | Coding with AI Agents | 30 min | Done |
| 4 | Benefits, limits, and risks of AI-assisted coding | TBD | Pending |
| 5 | Creating reusable prompts, skills, or simple agents | TBD | Pending |
| 6 | Using AI in the software lifecycle: design, coding, testing, documentation | TBD | Pending |
| 7 | Spec-driven development with AI | TBD | Pending |
| 8 | Integration with external tools and data | TBD | Pending |
| 9 | Practical workflow examples and productivity tips | TBD | Pending |

## Conventions

- **Folder structure:** one folder per chapter — `NN_short-slug/` (e.g., `01_agents-vs-assistants/`)
- Each folder contains the chapter markdown and any related assets (images, code samples)
- The main chapter file matches the folder name (e.g., `01_agents-vs-assistants/01_agents-vs-assistants.md`)
- Every chapter ends with a **Resources** section linking to relevant articles, docs, and tools
- Use ATX headings (`#`, `##`, `###`)
- Code examples in fenced blocks with language tags
- Keep chapters focused — one concept per section, prefer concrete over abstract

## Social Media Posts

Process for creating LinkedIn and Facebook posts to promote training content.

### Location and naming

- **Folder:** `social_posts/`
- **File naming:** `YYYY-MM-DD-<short-slug>.md`
- One file per post, containing both platform variants

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
