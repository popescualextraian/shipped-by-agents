---
name: 01-analyze-requirements
description: Analyze project requirements and codebase state to determine what needs to be built or changed
argument-hint: "[description of task]"
---

# Step 1: Analyze Requirements

## Goal
Examine the project requirements and current codebase to build a clear picture
of what needs to happen, what's affected, and what could go wrong.

## What You Need
- Project documentation (if available)
- Access to the current codebase
- The user's feature request or requirement description

## Process
1. Read through relevant documentation and project files
2. Explore the existing codebase structure and conventions
3. Identify which files and components will be affected
4. Map out dependencies and constraints
5. Flag potential risks or open questions

## Verification
- [ ] Requirements are clearly understood
- [ ] Affected files and components are identified
- [ ] Dependencies are mapped
- [ ] Risks are documented
- [ ] Any open questions are noted

## Output
Write workflow-state/analysis-results.md containing:
- A summary of what needs to be done
- List of files to modify or create, with reasons
- Dependency analysis
- Risk assessment
- Open questions that need user input (if any)

## What Happens Next
After analysis is complete, the orchestrator will move to Step 2 (Planning),
or pause to address open questions first.
