---
name: 05-document
description: Document all changes, decisions, and usage instructions as the final workflow step
---

# Step 5: Documentation

## Goal
Record everything that was done, decided, and changed so that future developers
can understand and maintain the work.

## What You Need
- Analysis results: workflow-state/analysis-results.md
- Implementation plan: workflow-state/implementation-plan.md
- Implementation results: workflow-state/implementation-results.md
- Test results: workflow-state/test-results.md
- All modified files

## Process
1. Update inline code documentation (comments, JSDoc, docstrings)
2. Update the README if necessary
3. Update API documentation if applicable
4. Create or update user guides if needed
5. Document architectural decisions
6. Update the changelog
7. Write a summary of the entire workflow execution

## Verification
- [ ] Code comments are updated
- [ ] Function and class documentation is complete
- [ ] README is updated (if needed)
- [ ] API documentation is current
- [ ] Changelog is updated
- [ ] Architectural decisions are documented

## Output
1. Updated documentation files as appropriate
2. Write workflow-state/workflow-summary.md containing:
   - Overview of what was accomplished
   - All files changed
   - Key decisions made
   - Tests added
   - How to use the new functionality
   - Future considerations

## Workflow Complete
This is the final step. Review the workflow-summary.md and confirm all objectives are met.
