---
name: rest-test-list
description: List all existing REST Assured test cases from the inventory
---

# rest-test-list

List all existing REST Assured tests in this project, grouped by test class.

## Steps

### 1. Read the inventory

Read the file `generated-tests/test-inventory.json`.

- If the file exists and contains a non-empty `tests` array, proceed to **Step 3**.
- If the file is missing, empty, or the `tests` array is empty, proceed to **Step 2**.

### 2. Rebuild the inventory from source

Scan all files matching `generated-tests/src/test/java/tests/*Test.java`.

For each file, extract:
- The class name (from the filename or `class` declaration)
- Every `@Test` method: method name, `@DisplayName` value, `@Tag` value(s)
- The `@Tag` annotation at class level (this is the resource tag)

Build a JSON structure matching this format and write it to `generated-tests/test-inventory.json`:

```json
{
  "lastUpdated": "<current ISO timestamp>",
  "tests": [
    {
      "class": "PostsApiTest",
      "method": "should_returnAllPosts_whenGetPosts",
      "displayName": "GET /posts returns all posts with status 200",
      "tag": "posts",
      "endpoint": "GET /posts",
      "created": "<date found in file or today>"
    }
  ]
}
```

Infer the `endpoint` field from the `@DisplayName` text where possible (it usually starts with the HTTP method and path). If you cannot infer it, leave it as an empty string.

### 3. Present the summary table

Group the tests by `class`. For each class, show:

```
PostsApiTest (5 tests)  [tag: posts]
  - GET /posts returns all posts with status 200
  - GET /posts/{id} returns a single post
  - POST /posts creates a new post and returns 201
  - PUT /posts/{id} updates an existing post
  - DELETE /posts/{id} returns 200

CommentsApiTest (2 tests)  [tag: comments]
  - GET /posts/{id}/comments returns comments for a post
  - GET /comments?postId={id} returns filtered comments

UsersApiTest (1 test)  [tag: users]
  - GET /users returns all users with status 200
```

After the list, print a one-line summary:

```
Total: <N> tests across <M> test classes.
```

## Notes

- Use the `displayName` field for the indented list items, not the method name.
- Sort classes alphabetically.
- If a class has no `@DisplayName` on its test methods, fall back to the method name.
- Do not run any tests — this skill is read-only.
