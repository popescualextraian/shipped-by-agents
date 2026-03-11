---
name: rest-test-run
description: Run REST Assured tests and report results. Supports filtering by tag, class, or method.
argument-hint: Optional filter: tag name, class name, or ClassName#methodName
---

# rest-test-run

Run REST Assured tests and report a clear summary of results. Supports running all tests or a filtered subset.

## Steps

### 1. Parse the filter argument

Inspect the argument (if any) to determine the run scope:

| Argument form | Example | Maven flag |
|---|---|---|
| No argument | _(empty)_ | _(none — run all tests)_ |
| Tag name | `posts` | `-Dgroups="posts"` |
| Class name | `PostsApiTest` | `-Dtest=PostsApiTest` |
| Method name | `PostsApiTest#should_returnAllPosts_whenGetPosts` | `-Dtest=PostsApiTest#should_returnAllPosts_whenGetPosts` |

**Disambiguation rule:** if the argument matches a known class name (ends with `Test` or exists in the inventory), treat it as a class filter. Otherwise treat it as a tag filter.

### 2. Build the Maven command

Construct the command:

```
cd generated-tests && mvn test <filter-flag>
```

Examples:
- All tests: `cd generated-tests && mvn test`
- By tag: `cd generated-tests && mvn test -Dgroups="posts"`
- By class: `cd generated-tests && mvn test -Dtest=PostsApiTest`
- By method: `cd generated-tests && mvn test -Dtest=PostsApiTest#should_returnAllPosts_whenGetPosts`

### 3. Run the tests

Execute the Maven command. Capture the full output including the Surefire summary block.

### 4. Parse the results

Extract from the output:
- Total tests run
- Passed count
- Failed count
- Skipped count
- Names of any failing tests (class + method)
- Failure messages and stack trace excerpts (first 5–10 lines per failure)

### 5. Report the summary

Present a clear summary:

```
Run: 8 | Passed: 7 | Failed: 1 | Skipped: 0

FAILED:
  PostsApiTest > should_createPost_whenPostPosts
  Expected: 201 but was: 400
  at PostsApiTest.java:78
```

If all tests pass:

```
All 8 tests passed.
```

### 6. Analyze failures (if any)

For each failing test:

1. Read the test source file to understand what assertion failed.
2. Check whether the failure is likely caused by:
   - A wrong expected value in the assertion
   - A test data issue (e.g., hardcoded ID that no longer exists)
   - An API behavior change
   - A connectivity issue (base URL wrong, API unreachable)
3. Briefly explain the likely cause in plain language.

### 7. Offer to fix (if any failures)

After explaining the failure(s), ask the user:

> "Would you like me to attempt a fix?"

If the user confirms:
- Make the minimal change needed to fix the test (do not change the test's intent).
- Re-run the same test(s) to verify the fix.
- Report whether the fix worked.
- If still failing after one fix attempt, report the remaining error and stop.

## Notes

- Always run from the `generated-tests/` directory — Maven requires `pom.xml` to be in the working directory.
- Do not modify test logic as part of a fix unless the user explicitly asks.
- If Maven is not installed or the command fails with a non-test error (e.g., `BUILD FAILURE` before test execution), report the setup issue clearly and stop.
- If the user provides a filter that matches no tests, report "No tests found matching '<filter>'" rather than treating it as a pass.
