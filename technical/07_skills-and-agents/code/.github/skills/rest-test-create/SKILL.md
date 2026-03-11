---
name: rest-test-create
description: Generate REST Assured test cases from a natural language description
argument-hint: Describe the endpoint or tests you want to create
---

# rest-test-create

Generate one or more REST Assured test methods from a natural language description and add them to the appropriate test class.

## Steps

### 1. Parse the request

Read the argument provided. Extract:
- The HTTP method (GET, POST, PUT, DELETE, PATCH)
- The endpoint path (e.g., `/users`, `/posts/{id}`)
- The expected behavior or scenario (e.g., "returns 200 with a list", "creates a resource and returns 201")

If the argument is ambiguous or missing key details, ask the user one focused clarifying question before proceeding.

### 2. Discover API structure

Determine what endpoints are available and how they are structured. Use this priority order:

1. **OpenAPI spec** — look for `openapi.json`, `openapi.yaml`, `swagger.json`, or `swagger.yaml` anywhere in the project. If found, parse it for the target endpoint's request/response schema.
2. **Existing tests** — scan `generated-tests/src/test/java/tests/*Test.java` for similar endpoints. Use the existing request/response patterns as a guide.
3. **Ask the user** — if neither source is available, ask: "What fields does the request body include, and what does the response look like?"

### 3. Match to an existing test class

Read `generated-tests/test-inventory.json` to see what classes and tags exist.

- If the endpoint belongs to a resource that already has a test class (e.g., `PostsApiTest` for `/posts`), add the new test methods to that class.
- If no matching class exists, create a new file following the naming convention: `<Resource>ApiTest.java` (e.g., `AlbumsApiTest.java`).

### 4. Check for duplicates

Before generating, check whether a test for the same endpoint and scenario already exists in the target class. If a duplicate is found, tell the user and ask whether to skip, replace, or create a variant.

### 5. Generate the test method(s)

Follow all project conventions:

- **Method naming:** `should_<expected>_when<condition>` — e.g., `should_returnAllAlbums_whenGetAlbums`
- **Annotations:** `@Test`, `@DisplayName("<HTTP method> <path> <behavior>")`, `@Tag("<resource>")` (only at class level if not already present)
- **Structure:** REST Assured fluent API with `given()` / `when()` / `then()`
- **Config:** base URL loaded from `test-config.properties` via `@BeforeAll` setup (copy the pattern from an existing test class)
- **Assertions:** check status code, key response fields (use `notNullValue()`, `equalTo()`, `hasSize()` as appropriate)
- **Imports:** include all required imports (`RestAssured`, `ContentType`, JUnit 5 annotations, Hamcrest matchers)

Use patterns from existing tests in the codebase wherever possible. Match the style and structure of the existing test classes.

If creating a new test class, include the full class skeleton with `@BeforeAll` setup loading config from `test-config.properties`.

### 6. Write the file

Write the generated test method(s) into the appropriate file:
- For an existing class: insert the new method(s) before the closing `}` of the class.
- For a new class: create the file at `generated-tests/src/test/java/tests/<ClassName>.java`.

### 7. Verify compilation

Run the following command from the project root:

```
cd generated-tests && mvn compile -q test-compile
```

If compilation fails:
- Read the error output carefully.
- Fix the issue (missing import, syntax error, wrong method signature).
- Run the compile check again.
- Repeat up to 3 times. If still failing after 3 attempts, report the error to the user and stop.

### 8. Update the inventory

Read `generated-tests/test-inventory.json`. Add an entry for each new test method:

```json
{
  "class": "<ClassName>",
  "method": "<methodName>",
  "displayName": "<@DisplayName value>",
  "tag": "<resource tag>",
  "endpoint": "<HTTP method> <path>",
  "created": "<today's date in YYYY-MM-DD format>"
}
```

Update `lastUpdated` to the current ISO timestamp. Write the updated file back.

### 9. Confirm to the user

Report what was created:
- File path(s) modified or created
- Method name(s) added
- Compilation result

## Notes

- Never remove or modify existing test methods.
- If multiple scenarios are implied in the argument (e.g., "test GET and POST for /albums"), generate all of them in one pass.
- Follow the exact same import and annotation style used in existing test classes.
- If a new class is created, its class-level `@Tag` should be the resource name in lowercase (e.g., `@Tag("albums")`).
