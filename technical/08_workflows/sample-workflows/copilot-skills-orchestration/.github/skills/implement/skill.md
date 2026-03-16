---
name: implement
description: Execute the approved implementation plan phase by phase with checkpoints and deviation tracking
---

# Step 3: Implementation

## Goal
Execute the approved implementation plan, working through each phase in order
while maintaining checkpoints and documenting progress.

## What You Need
- Approved plan: workflow-state/implementation-plan.md
- Analysis results: workflow-state/analysis-results.md

## Process
1. Review the approved implementation plan
2. Create a git checkpoint before starting
3. Implement Phase 1 changes
4. Create a checkpoint after Phase 1
5. Continue through remaining phases
6. Create a final checkpoint after all changes

## Rules
- Follow the plan unless you discover a blocking issue
- If deviating from the plan, explain why and get user approval
- Create checkpoints between phases to allow rollback
- Test each phase before moving to the next
- Document any unexpected challenges or changes

## Verification
- [ ] Checkpoint created before starting
- [ ] Phase 1 completed and tested
- [ ] Phase 2 completed and tested
- [ ] All file changes completed
- [ ] Code follows project standards
- [ ] No linter errors introduced

## Output
Write workflow-state/implementation-results.md containing:
- List of all files modified or created
- Summary of changes made in each file
- Any deviations from the original plan, with explanations
- Issues encountered and how they were resolved
- Status of each phase

## What Happens Next
After implementation is complete, the orchestrator will move to Step 4 (Testing).
