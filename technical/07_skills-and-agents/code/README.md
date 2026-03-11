# REST Assured Test Agent — Working Code

Companion code for Chapter 7: Creating Reusable Prompts, Skills & Simple Agents.

## Prerequisites

- Java 17+
- Maven 3.8+

## Quick Start

cd generated-tests
mvn test

## Run specific tests

# By tag
mvn test -Dgroups="posts"

# By class
mvn test -Dtest=PostsApiTest

# By method
mvn test -Dtest=PostsApiTest#should_returnAllPosts_whenGetPosts

## Project Structure

- `generated-tests/` — Maven project with REST Assured test classes
- `.claude/skills/` — Claude Code skill files (rest-test-list, rest-test-create, rest-test-run, rest-test-agent)
- `.github/skills/` — Copilot skill files
- `.github/agents/` — Copilot agent file (rest-test-agent)

## Target API

All tests run against [JSONPlaceholder](https://jsonplaceholder.typicode.com).
Configure the base URL in `generated-tests/src/test/resources/test-config.properties`.
