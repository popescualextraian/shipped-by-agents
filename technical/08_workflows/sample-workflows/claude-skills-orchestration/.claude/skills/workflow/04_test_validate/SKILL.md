---
name: 04-test-validate
description: Validate the implementation by running tests, checking quality, and verifying requirements are met
---

# Step 4: Test and Validate

## Goal
Verify that the implementation works correctly, meets all requirements,
and doesn't break existing functionality.

## What You Need
- Implementation results: workflow-state/implementation-results.md
- Implementation plan: workflow-state/implementation-plan.md
- The files modified in Step 3

## Process
1. Review all files modified in Step 3
2. Run the existing test suites
3. Write or update tests for new functionality
4. Perform a manual testing checklist
5. Check for linter or type errors
6. Verify all requirements from Step 1 are satisfied
7. Check edge cases and error handling

## Verification
- [ ] All existing tests pass
- [ ] New tests are written for new functionality
- [ ] New tests pass
- [ ] No linter or type errors
- [ ] Edge cases are handled
- [ ] Error handling is implemented
- [ ] All original requirements are satisfied
- [ ] Performance is acceptable

## Output
Write workflow-state/test-results.md containing:
- Test execution summary
- List of tests added or modified
- Issues found and their current status
- Coverage report (if applicable)
- Validation checklist results

## What Happens Next
If tests pass, the orchestrator will move to Step 5 (Documentation).
If tests fail, the orchestrator will ask the user whether to fix or roll back.
