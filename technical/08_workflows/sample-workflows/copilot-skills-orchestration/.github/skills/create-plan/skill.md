---
name: create-plan
description: Create a detailed implementation plan with phases, file changes, and testing strategy based on analysis results
---

# Step 2: Create Implementation Plan

## Goal
Transform the analysis results into a detailed, actionable implementation plan
with concrete steps and file-level changes.

## What You Need
- Results from Step 1: workflow-state/analysis-results.md
- Access to the current codebase

## Process
1. Review the analysis results from the previous step
2. Break the implementation into logical phases
3. Define specific file changes for each phase
4. Identify what tests are needed
5. Estimate complexity and flag potential issues
6. Plan checkpoint locations for rollback safety

## Verification
- [ ] Implementation is broken into clear phases
- [ ] Each phase has specific file changes defined
- [ ] Testing strategy is defined
- [ ] Rollback strategy is considered
- [ ] Dependencies are ordered correctly

## Output
Write workflow-state/implementation-plan.md containing:
- Phase-by-phase implementation plan
- Specific files to modify in each phase
- Code structure and architecture decisions
- Test cases to implement
- Checkpoint strategy

## Approval Gate
STOP HERE. Present the plan to the user for approval before proceeding to Step 3.

## What Happens Next
After the user approves the plan, the orchestrator will move to Step 3 (Implementation).
