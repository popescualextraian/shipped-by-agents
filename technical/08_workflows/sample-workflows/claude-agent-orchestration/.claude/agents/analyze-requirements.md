---
name: analyze-requirements
description: Examines project requirements and codebase state to determine what needs to be built. Explores project structure, identifies affected areas, maps dependencies, assesses risks, and writes a comprehensive analysis to guide the planning phase.
tools: Bash, Glob, Grep, Read, Write
model: sonnet
---

# Agent: Analyze Requirements

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
