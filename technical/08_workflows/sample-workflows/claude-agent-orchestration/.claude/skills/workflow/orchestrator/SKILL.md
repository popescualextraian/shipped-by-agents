---
name: workflow-orchestrator
description: Orchestrates a complete development workflow by delegating steps to specialized sub-agents
argument-hint: "[detailed task description]"
---

# Workflow Orchestrator

## Overview
This skill coordinates a full development workflow by dispatching each step
to a specialized sub-agent. Each agent works in isolation and writes results
to shared state files.

## Workflow Sequence

1. Analyze — understand requirements and current state
2. Plan — create a detailed implementation plan
3. Implement — execute the plan with checkpoints
4. Test — validate the implementation
5. Document — complete all documentation

## Step Execution

### Step 1: Analysis
- Dispatch the Agent tool with subagent_type: "analyze-requirements", passing the user's task description
- Wait for the agent to complete
- Summarize key findings from workflow-state/analysis-results.md

### Step 2: Planning
- Dispatch the Agent tool with subagent_type: "create-plan"
- Present the implementation plan to the user
- APPROVAL GATE: Do not proceed until the user explicitly approves

### Step 3: Implementation
- Create a git checkpoint tagged "pre-implementation"
- After receiving approval, dispatch the Agent tool with subagent_type: "implement"
- Create a checkpoint after each completed phase
- Summarize implementation progress

### Step 4: Testing
- Dispatch the Agent tool with subagent_type: "test-validate"
- Report test results to the user
- If tests fail, ask whether to fix issues or roll back

### Step 5: Documentation
- Dispatch the Agent tool with subagent_type: "document"
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
