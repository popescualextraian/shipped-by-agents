#!/usr/bin/env python3
"""User story reference manager — manage references and render story drafts."""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATES_DIR = SKILL_DIR / "templates"

DEFAULT_DATA_DIR = "user-stories"


def find_data_dir():
    """Find user-stories data directory by walking up from cwd."""
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / DEFAULT_DATA_DIR
        if (candidate / "references.json").exists():
            return candidate
    return cwd / DEFAULT_DATA_DIR


def load_references(data_dir):
    """Load references.json from data directory."""
    ref_path = data_dir / "references.json"
    if not ref_path.exists():
        print(f"Error: No references.json found at {ref_path}")
        print("Run 'init <project-key>' first.")
        sys.exit(1)
    with open(ref_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_references(data_dir, data):
    """Save references.json to data directory."""
    ref_path = data_dir / "references.json"
    with open(ref_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"References saved: {ref_path}")


def next_ref_id(data):
    """Generate next reference ID (ref-001, ref-002, ...)."""
    existing = [r["id"] for r in data.get("references", [])]
    nums = []
    for rid in existing:
        match = re.match(r"ref-(\d+)", rid)
        if match:
            nums.append(int(match.group(1)))
    next_num = max(nums, default=0) + 1
    return f"ref-{next_num:03d}"


def slugify(text):
    """Convert text to a filesystem-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:80].strip("-")


# ── Commands ──────────────────────────────────────────────────────────────────


def cmd_init(args):
    """Initialize user-stories data directory with references.json."""
    data_dir = Path.cwd() / DEFAULT_DATA_DIR
    if (data_dir / "references.json").exists():
        print(f"Already initialized: {data_dir}")
        return

    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "refs").mkdir(exist_ok=True)
    (data_dir / "stories").mkdir(exist_ok=True)

    template = TEMPLATES_DIR / "references.template.json"
    with open(template, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["jira_project_key"] = args.project_key
    if args.jira_url:
        data["jira_base_url"] = args.jira_url

    save_references(data_dir, data)
    print(f"Initialized: {data_dir}")
    print(f"Project key: {args.project_key}")
    if args.jira_url:
        print(f"JIRA URL: {args.jira_url}")


def cmd_add(args):
    """Add a reference entry."""
    data_dir = find_data_dir()
    data = load_references(data_dir)

    ref_id = next_ref_id(data)
    ref_type = args.type

    entry = {
        "id": ref_id,
        "type": ref_type,
        "title": args.title,
        "description": args.description or "",
        "path": args.location if ref_type == "local-md" else None,
        "url": args.location if ref_type == "confluence" else None,
        "original_url": None,
        "added": date.today().isoformat(),
        "downloaded": None,
    }

    data["references"].append(entry)
    save_references(data_dir, data)
    print(f"Added reference: {ref_id} — {args.title} ({ref_type})")


def cmd_remove(args):
    """Remove a reference by ID."""
    data_dir = find_data_dir()
    data = load_references(data_dir)

    found = None
    for i, r in enumerate(data["references"]):
        if r["id"] == args.id:
            found = i
            break

    if found is None:
        print(f"Error: Reference '{args.id}' not found.")
        sys.exit(1)

    entry = data["references"].pop(found)
    save_references(data_dir, data)
    print(f"Removed: {entry['id']} — {entry['title']}")


def cmd_list(args):
    """List references."""
    data_dir = find_data_dir()
    data = load_references(data_dir)

    refs = data["references"]
    if args.type:
        refs = [r for r in refs if r["type"] == args.type]

    if not refs:
        print("No references found.")
        return

    print(f"Project: {data['jira_project_key']}")
    if data.get("jira_base_url"):
        print(f"JIRA: {data['jira_base_url']}")
    print()
    print(f"{'ID':<10} {'Type':<12} {'Title':<35} {'Description'}")
    print("-" * 90)
    for r in refs:
        print(f"{r['id']:<10} {r['type']:<12} {r['title']:<35} {r.get('description', '')}")
    print(f"\nTotal: {len(refs)} reference(s)")


def cmd_get_ref(args):
    """Print single reference details."""
    data_dir = find_data_dir()
    data = load_references(data_dir)

    for r in data["references"]:
        if r["id"] == args.id:
            print(json.dumps(r, indent=2))
            return

    print(f"Error: Reference '{args.id}' not found.")
    sys.exit(1)


def cmd_mark_downloaded(args):
    """Update a Confluence reference after local download."""
    data_dir = find_data_dir()
    data = load_references(data_dir)

    for r in data["references"]:
        if r["id"] == args.id:
            if r["type"] != "confluence":
                print(f"Warning: {args.id} is type '{r['type']}', not 'confluence'.")
            r["original_url"] = r.get("url")
            r["type"] = "local-md"
            r["path"] = args.local_path
            r["url"] = None
            r["downloaded"] = date.today().isoformat()
            save_references(data_dir, data)
            print(f"Marked downloaded: {args.id} -> {args.local_path}")
            return

    print(f"Error: Reference '{args.id}' not found.")
    sys.exit(1)


def render_story_md(story):
    """Render a story dict to markdown using the template."""
    template_path = TEMPLATES_DIR / "user-story.template.md"
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    rendered = template

    # Simple scalar fields
    rendered = rendered.replace("{{title}}", story.get("title", "Untitled"))
    rendered = rendered.replace("{{project_key}}", story.get("project_key", ""))
    rendered = rendered.replace("{{epic_link}}", story.get("epic_link", ""))
    rendered = rendered.replace("{{priority}}", story.get("priority", "Medium"))
    rendered = rendered.replace("{{labels}}", ", ".join(story.get("labels", [])))
    rendered = rendered.replace("{{story_points}}", str(story.get("story_points", "")))

    # Required description fields
    rendered = rendered.replace("{{current_situation}}", story.get("current_situation", ""))
    rendered = rendered.replace("{{desired_situation}}", story.get("desired_situation", ""))

    # Optional sections — render block if present, remove if not
    for field in ["design_description", "deliverables", "implementation_notes", "out_of_scope"]:
        value = story.get(field)
        if value:
            rendered = rendered.replace(f"{{{{{field}}}}}", value)
            rendered = rendered.replace(f"{{{{#{field}}}}}", "")
            rendered = rendered.replace(f"{{{{/{field}}}}}", "")
        else:
            rendered = re.sub(
                rf"\{{\{{#{field}\}}\}}.*?\{{\{{/{field}\}}\}}",
                "",
                rendered,
                flags=re.DOTALL,
            )

    # Acceptance criteria — checklist items
    ac_items = story.get("acceptance_criteria", [])
    if ac_items:
        ac_lines = [f"- [ ] {item}" for item in ac_items]
        ac_block = "\n".join(ac_lines)
        rendered = re.sub(
            r"\{\{#acceptance_criteria_items\}\}.*?\{\{/acceptance_criteria_items\}\}",
            ac_block,
            rendered,
            flags=re.DOTALL,
        )
        rendered = rendered.replace("{{#acceptance_criteria}}", "")
        rendered = rendered.replace("{{/acceptance_criteria}}", "")
    else:
        rendered = re.sub(
            r"\{\{#acceptance_criteria\}\}.*?\{\{/acceptance_criteria\}\}",
            "",
            rendered,
            flags=re.DOTALL,
        )

    # Subtasks — title-only list
    subtask_items = story.get("subtasks", [])
    if subtask_items:
        st_lines = [f"- {item}" for item in subtask_items]
        st_block = "\n".join(st_lines)
        rendered = re.sub(
            r"\{\{#subtask_items\}\}.*?\{\{/subtask_items\}\}",
            st_block,
            rendered,
            flags=re.DOTALL,
        )
        rendered = rendered.replace("{{#subtasks}}", "")
        rendered = rendered.replace("{{/subtasks}}", "")
    else:
        rendered = re.sub(
            r"\{\{#subtasks\}\}.*?\{\{/subtasks\}\}",
            "",
            rendered,
            flags=re.DOTALL,
        )

    # References
    ref_lines = []
    for ref in story.get("references", []):
        ref_lines.append(f"- [{ref.get('title', '')}]({ref.get('link', '#')}) — {ref.get('description', '')}")
    ref_block = "\n".join(ref_lines) if ref_lines else "- None"
    rendered = re.sub(
        r"\{\{#references\}\}.*?\{\{/references\}\}",
        ref_block,
        rendered,
        flags=re.DOTALL,
    )

    # Clean up blank lines (collapse 3+ consecutive newlines to 2)
    rendered = re.sub(r"\n{3,}", "\n\n", rendered)

    return rendered


def cmd_render_story(args):
    """Render a user story from JSON input and save to stories/."""
    data_dir = find_data_dir()
    stories_dir = data_dir / "stories"
    stories_dir.mkdir(exist_ok=True)

    story = json.loads(args.json_data)
    rendered = render_story_md(story)

    slug = slugify(story.get("title", "untitled"))
    filename = f"{slug}.md"
    filepath = stories_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Story saved: {filepath}")
    print()
    print(rendered)


def cmd_save_story(args):
    """Save or update a local story draft with a JIRA issue key."""
    data_dir = find_data_dir()
    stories_dir = data_dir / "stories"
    stories_dir.mkdir(exist_ok=True)

    story = json.loads(args.json_data)
    issue_key = args.issue_key

    # Prepend issue key to title for the local copy
    story_copy = dict(story)
    story_copy["title"] = f"[{issue_key}] {story.get('title', 'Untitled')}"

    rendered = render_story_md(story_copy)

    filename = f"{issue_key.lower()}.md"
    filepath = stories_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Story saved: {filepath}")
    print()
    print(rendered)


def cmd_list_stories(args):
    """List local story drafts."""
    data_dir = find_data_dir()
    stories_dir = data_dir / "stories"

    if not stories_dir.exists():
        print("No stories directory found.")
        return

    files = sorted(stories_dir.glob("*.md"))
    if not files:
        print("No story drafts found.")
        return

    print(f"{'File':<40} {'Size':<10} {'Modified'}")
    print("-" * 65)
    for f in files:
        stat = f.stat()
        size = f"{stat.st_size} B"
        modified = date.fromtimestamp(stat.st_mtime).isoformat()
        print(f"{f.name:<40} {size:<10} {modified}")
    print(f"\nTotal: {len(files)} story draft(s)")


# ── CLI ───────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="User Story Reference Manager — manage references and render story drafts"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    p_init = subparsers.add_parser("init", help="Initialize user-stories data directory")
    p_init.add_argument("project_key", help="JIRA project key (e.g. PROJ)")
    p_init.add_argument("--jira-url", help="JIRA base URL (e.g. https://org.atlassian.net)")

    # add
    p_add = subparsers.add_parser("add", help="Add a reference")
    p_add.add_argument("type", choices=["local-md", "confluence"], help="Reference type")
    p_add.add_argument("location", help="File path (local-md) or URL (confluence)")
    p_add.add_argument("title", help="Reference title")
    p_add.add_argument("description", nargs="?", default="", help="One-line description")

    # remove
    p_remove = subparsers.add_parser("remove", help="Remove a reference by ID")
    p_remove.add_argument("id", help="Reference ID (e.g. ref-001)")

    # list
    p_list = subparsers.add_parser("list", help="List references")
    p_list.add_argument("--type", choices=["local-md", "confluence"], help="Filter by type")

    # get-ref
    p_get = subparsers.add_parser("get-ref", help="Get single reference details")
    p_get.add_argument("id", help="Reference ID")

    # mark-downloaded
    p_mark = subparsers.add_parser("mark-downloaded", help="Mark Confluence ref as downloaded")
    p_mark.add_argument("id", help="Reference ID")
    p_mark.add_argument("local_path", help="Local path to downloaded file")

    # render-story
    p_render = subparsers.add_parser("render-story", help="Render story from JSON")
    p_render.add_argument("json_data", help="JSON string with story fields")

    # save-story
    p_save = subparsers.add_parser("save-story", help="Save story draft with JIRA key")
    p_save.add_argument("issue_key", help="JIRA issue key (e.g. PROJ-123)")
    p_save.add_argument("json_data", help="JSON string with story fields")

    # list-stories
    subparsers.add_parser("list-stories", help="List local story drafts")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "remove": cmd_remove,
        "list": cmd_list,
        "get-ref": cmd_get_ref,
        "mark-downloaded": cmd_mark_downloaded,
        "render-story": cmd_render_story,
        "save-story": cmd_save_story,
        "list-stories": cmd_list_stories,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
