---
name: orchestrator
description: Orchestrates a complete multi-step development workflow from analysis to documentation
argument-hint: "[detailed task description]"
---

# Workflow Orchestrator

## Overview
This prompt coordinates a complete development workflow with five sequential steps,
from initial analysis to final documentation.

## Workflow Sequence

1. Analyze — gather requirements and assess the current state
2. Plan — produce a detailed implementation plan
3. Implement — execute the plan with checkpoints
4. Test — verify the implementation meets requirements
5. Document — record all changes and decisions

## Step Execution

### Step 1: Analysis
- Follow instructions from #file:./01_analyze_requirements.prompt.md using the user's task description
- Wait for analysis to finish
- Summarize key findings from workflow-state/analysis-results.md

### Step 2: Planning
- Follow instructions from #file:./02_create_plan.prompt.md
- Present the implementation plan to the user
- APPROVAL GATE: Do not proceed until the user explicitly approves

### Step 3: Implementation
- Create a checkpoint tagged "pre-implementation"
- Follow instructions from #file:./03_implement.prompt.md
- Create a checkpoint after each completed phase
- Summarize implementation progress

### Step 4: Testing
- Follow instructions from #file:./04_test_validate.prompt.md
- Report test results to the user
- If tests fail, ask whether to fix issues or roll back

### Step 5: Documentation
- Follow instructions from #file:./05_document.prompt.md
- Present the final workflow summary
- Mark the workflow as complete

## Rules
1. Complete each step fully before moving to the next
2. Always save intermediate results to workflow-state/
3. Create checkpoints before and after major changes
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
