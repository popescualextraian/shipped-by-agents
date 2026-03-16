---
name: workflow-orchestrator
description: Orchestrates a complete multi-step development workflow from analysis through documentation
argument-hint: "[detailed task description]"
---

# Workflow Orchestrator

## Overview
This skill coordinates a complete development workflow with five sequential steps,
from initial analysis to final documentation.

## Workflow Sequence

1. Analyze — gather requirements and assess the current state
2. Plan — produce a detailed implementation plan
3. Implement — execute the plan with checkpoints
4. Test — verify the implementation meets requirements
5. Document — record all changes and decisions

## Step Execution

### Step 1: Analysis
- Run the `/01-analyze-requirements` skill with the user's task description
- Wait for analysis to finish
- Summarize key findings from workflow-state/analysis-results.md

### Step 2: Planning
- Run the `/02-create-plan` skill
- Present the implementation plan to the user
- APPROVAL GATE: Do not proceed until the user explicitly approves

### Step 3: Implementation
- Create a git checkpoint tagged "pre-implementation"
- After receiving user approval, run the `/03-implement` skill
- Create a checkpoint after each completed phase
- Summarize implementation progress

### Step 4: Testing
- Run the `/04-test-validate` skill
- Report test results to the user
- If tests fail, ask whether to fix issues or roll back

### Step 5: Documentation
- Run the `/05-document` skill
- Present the final workflow summary
- Mark the workflow as complete

## Rules
1. Complete each step fully before moving to the next
2. Always save intermediate results to workflow-state/
3. Create git checkpoints before and after major changes
4. Reference outputs from previous steps explicitly
5. Stop and wait for user approval at marked gates
6. If a step fails, stop and ask the user how to proceed

## State Directory
All intermediate artifacts are stored in workflow-state/:
- analysis-results.md — requirements and impact analysis
- implementation-plan.md — detailed implementation plan
- implementation-results.md — what was actually implemented
- test-results.md — testing outcomes
- workflow-summary.md — final summary and documentation

## Usage
Invoke with: /workflow-orchestrator [detailed task description]

Example: /workflow-orchestrator Add user authentication with JWT tokens
