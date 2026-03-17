<!--
=== Template Configuration ===

This section tells the agent how to use this template. The agent reads it
before creating or pushing stories. Update this section to change defaults,
JIRA mappings, or add project-specific fields.

Project: PROJ
JIRA URL: https://your-org.atlassian.net/jira
Default epic: PROJ-42

JIRA field mapping (markdown field → JIRA field):
  - "# title" heading        → summary
  - Body below metadata       → description
  - **Priority:** value       → priority (e.g. {"name": "Medium"})
  - **Labels:** value         → labels (comma-separated → array)
  - **Story Points:** value   → story_points
  - **Epic:** value           → epic_link (also set via additional_fields {"epic_link": "..."})

Custom fields:
  - Epic Link: customfield_10001
  - AC Checklist: customfield_11100 — acceptance criteria items formatted as checklist text

Subtasks:
  If a Subtasks section exists, create each item as a Sub-task issue
  linked to the parent story.

Issue type: Story (default). Change per story if needed.

=== End Configuration ===
-->

# {{title}}

**Project:** {{project_key}}
**Epic:** {{epic_link}}
**Priority:** {{priority}}
**Labels:** {{labels}}
**Story Points:** {{story_points}}

---

## Current Situation

{{current_situation}}

## Desired Situation

{{desired_situation}}

{{#design_description}}
---

## Design Description

{{design_description}}
{{/design_description}}

{{#deliverables}}
---

## Deliverables

{{deliverables}}
{{/deliverables}}

{{#implementation_notes}}
---

## Implementation Notes

{{implementation_notes}}
{{/implementation_notes}}

{{#out_of_scope}}
---

## Out of Scope

{{out_of_scope}}
{{/out_of_scope}}

{{#acceptance_criteria}}
---

## Acceptance Criteria

{{#acceptance_criteria_items}}
- [ ] {{item}}
{{/acceptance_criteria_items}}
{{/acceptance_criteria}}

{{#subtasks}}
---

## Subtasks

{{#subtask_items}}
- {{item}}
{{/subtask_items}}
{{/subtasks}}

---

## References

{{#references}}
- [{{title}}]({{link}}) — {{description}}
{{/references}}
