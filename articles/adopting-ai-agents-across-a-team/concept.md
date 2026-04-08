# Adopting AI Coding Agents Across a Team: A Practical Guide for Architects and Tech Leads

## The Licence Is Not Enough

We are at a turning point. Most development teams have started some form of AI-assisted coding: Claude, Copilot, Cursor. Some developers are enthusiastic. Most are cautiously experimenting. A few have already gone back to their old workflow.

As a solution architect, I have to ask the uncomfortable question: is buying licences enough? Should I just roll them out to every developer and call it done?

I believe, at least for the next couple of years, the answer is no. Notice how I said "couple of years." Things are evolving so fast that even two years feels like a long-term prediction. But that is another subject entirely. Let us move on to ours.

Here is the scenario. You are a lead developer or architect in your team. Management has gifted you and your teammates some Claude licences. The expectations are high. There is no enterprise standard yet. Everybody talks on Reddit, shares their experiences, but no team best practices have crystallised. No adoption playbook has arrived on your desk. What do you do? Where do you start?

Well, let me help you here. What follows is a step-by-step approach, extracted from real experience building and maintaining an open-source training repository called <span style="color:#00BFA5">***Shipped by Agents***</span>, and from coaching delivery teams through their first weeks of working with AI coding agents.

---

## Step 1: The Setup. Give Your Agent a Brain

You are the architect. You know the project: the structure, the tech stack, the custom frameworks, the dos and don'ts. But your agent has no idea. It has never seen your codebase. It does not know that you use FastAPI instead of Flask, or that your team mandates Pydantic response models on every endpoint. It has zero context.

This is the fundamental thing most teams miss: **an AI coding agent starts every single conversation from zero**. No memory of previous sessions. No accumulated knowledge. Every time you open a new session, the agent is a blank slate.

Think of it this way. You have hired a very talented developer who learns incredibly fast, but you only have them for one day. Tomorrow, an equally talented developer shows up, but they also know nothing about your project. The day after, the same thing. Every morning, a brilliant stranger sits at the desk and asks: "So, what are we building?"

How do you get the most out of this rotating cast of brilliant strangers? You write things down. You create strong, structured documentation that gets loaded into every conversation automatically.

In practice, this means a project instruction file: `CLAUDE.md` for Claude Code, `copilot-instructions.md` for GitHub Copilot, or `AGENTS.md` depending on your tool. This file is loaded into the agent's context window at the start of every session. It is the single most important artefact in your agent workflow.

### What Goes Into the Instruction File

You do not have to start from scratch. Claude Code has a `/init` command that scans your project and generates a starter file. But treat that output as a first draft, never as the finished product. A good instruction file covers:

1. **Tech stack and dependencies**, so the agent picks the right patterns, not the popular ones
2. **Project structure**: folder layout, where things live, what goes where
3. **Build and run commands**: exact commands, no guessing. `pytest`, not "run the tests"
4. **Coding conventions**: your rules, not generic best practices. "All API endpoints return Pydantic response models, never return raw dicts"
5. **Key business flows**: the happy path for every critical flow. If a new developer would get it wrong without being told, write it down
6. **Architecture rules**: layering, dependency direction, cross-service communication patterns
7. **Security rules**: how secrets are handled, input validation requirements, SQL injection prevention

Here is the simple test: if you removed a line from this file, would the agent start making mistakes? If yes, the line stays. If no, cut it. A bloated instruction file gets ignored, just like bloated documentation in any other context.

### This Is Your Most Important Investment

I cannot stress this enough. The instruction file is not a nice-to-have. It is infrastructure, as critical as your CI configuration or your linter rules. The quality of this file directly determines the quality of everything the agent produces.

If the agent keeps making the same mistake (generating raw dictionaries instead of Pydantic models, putting business logic in route handlers, using the wrong test framework), the fix is almost always in the instruction file, not in your prompt. Add a rule. Be specific. Use emphasis for critical rules.

Review this file with the same rigour you review code. Structure it. Make sure it covers the data flows, the custom frameworks, the APIs that matter. This file is loaded in memory each and every conversation, and it is the most important thing you can give your agent.

---

## Step 2: Share It, Maintain It, Treat It Like Code

Once you have a solid instruction file, commit it to your repository so every team member benefits. This is not your personal config. It is a shared team asset.

Treat it like code:
- **Written** by the developer who knows the project best
- **Reviewed** by the tech lead or architect
- **Approved** via pull request, just like any other code change
- **Maintained**, updated every time conventions change

When major changes happen to your project (a new framework, a changed architecture rule, a deprecated pattern), the instruction file must be updated. Otherwise your agent is working from stale documentation, and stale documentation produces stale code.

Run `/init` periodically on mature projects. Compare its output with your current file. You might discover gaps: new folders the agent does not know about, new conventions that were never written down.

---

## Step 3: Adopt a Workflow. Plan, Build, Review, Test

You have the tools. You have the documentation. Now you start implementing tasks. But is there a process to it?

Yes. And the process matters more than the tool.

The most common mistake teams make is treating the agent like a magic box. You type a request, it produces code, you paste it in. That is not an agent workflow. That is a chatbot with extra steps. The real productivity gain comes from a disciplined cycle: **Plan → Review → Build → Test → Review**.

### Plan First, Always

The single most effective habit for working with agents is this: **never let the agent write code before you have reviewed its plan**.

When you give the agent a task, ask it to explore the codebase first and present a plan. Most agent tools have a dedicated plan mode, a read-only mode where the agent can read files, search code, and analyse structure, but cannot make changes.

> "We need a new REST endpoint for bulk-importing users from a CSV file. The endpoint should follow our existing patterns. Create a plan first: which layers need changes, what validations are needed, and how errors should be reported back to the caller. I will review the plan before you write any code."

You spend two minutes reviewing a plan. You catch that the agent forgot about the email uniqueness constraint, or that it planned to put validation logic in the controller instead of the service layer. You correct it before a single line of code is written. A few minutes of back-and-forth in planning saves hours of rework later.

### Review the Specs Before Building

This is the step most teams skip, and it costs them the most. The agent has produced a plan. Before you say "go build it," you review. Not a cursory glance. A real review.

Does the plan respect your architecture? Does it use the right patterns? Does it touch only the files it should? Does it break anything it should not? Are the acceptance criteria clear and testable?

This is where your role as architect matters most. The agent is good at generating plans. It is not good at judging whether a plan fits your system's constraints, your team's conventions, or your business rules. That judgement is yours.

Think of it like reviewing a spec from a junior developer. The spec might be technically correct but architecturally wrong: it couples two services that should be independent, it adds a database column when a computed field would suffice, it ignores an existing utility that already does what it proposes to build from scratch.

Review the plan. Refine it. Push back. Ask the agent to adjust. Only after the plan is right do you approve execution. This single checkpoint, reviewing the specs before building, eliminates the majority of rework.

> **Tip:** When planning, focus on architecture, not specifications. Tell the agent which layers to touch, which patterns to follow, which dependencies to respect. The agent is good at filling in the implementation details. It is not good at deciding where things should live or how components should interact. That is your job.

### Build. Let the Plan Do the Work

Once the plan is approved, start a fresh conversation and hand the agent your plan. This is important: a new conversation means a clean context, fully dedicated to execution. The agent reads the plan, reads your instruction file, and starts implementing.

This is where you will see your first real speed increase. The thinking is done. The architecture decisions are made. Now the code writes itself, fast. A strong, clear plan with no room for interpretation gives you good code from the start. If the plan has independent parts, you can even run two agents in parallel, each handling a separate piece. Just tell the agent which part to build, or let it decide based on the plan.

### Don't Be Afraid to Throw It Away

Yes, I can hear you saying: "I don't always know exactly what I want to build." Well, that is the beauty of this approach. You can iterate.

Specify, build, look at the result. You don't like it? Throw it away. Specify again, with lessons learned from the first attempt. Specify, build, review, repeat.

In traditional development, you spend two or three days building something and then realise it could have been done better. But by then you have invested too much time and energy. You keep what you have and move on with a compromise. In agentic development, the same cycle takes thirty minutes. The cost of restarting is almost zero. This changes how you think about quality: you stop settling for "good enough on the first try" and start aiming for "right."

### Test as You Go

The agent should run tests after every meaningful change, not at the end, as an afterthought. When the agent writes a function, it writes the test. When it modifies a service, it runs the existing test suite. When tests fail, it reads the error, diagnoses the cause, and fixes it before moving on.

This is also where Test-Driven Development (TDD) becomes practical in a way it rarely was before. Writing tests first has always been the right approach, but many teams skipped it because it felt slow. With agents, TDD costs you almost nothing. Tell the agent to write the tests first based on your plan, then implement the code to make them pass. The agent does both, and the feedback loop is instant.

This is not aspirational. Modern coding agents do this natively. But you have to tell them to. Your instruction file should include the exact test commands. Your prompts should include "run the tests before considering this step complete."

### The Two-Developer Contrast

Here is what the difference looks like in practice.

**Developer A** types: *"Build the user dashboard."* The agent guesses the layout, invents component names that do not match the project, picks a data-fetching pattern the team never uses, and produces 400 lines of code that look impressive but do not fit anywhere. Developer A spends the afternoon untangling it.

**Developer B** types: *"We need a new REST endpoint for bulk-importing users from CSV. Follow our existing endpoint patterns. Create a plan first: which layers need changes, what validations apply, how errors get reported. I will review before you implement."* The agent reads the existing endpoints, presents a plan using the team's patterns, and Developer B catches two issues before any code is written. They build step by step: test first, then implementation, each piece reviewed before moving on. The feature ships clean.

Same tool. Same model. Wildly different outcomes. The difference is how the developer communicated.

---

## Step 4: Review and Integrate

The code is written. The tests pass. Now what?

This is where many teams stop and call it done. But code that passes its own tests is not the same as code that works in the system. You need to review the output, run integration tests, and make sure the new code plays well with everything else.

### Code Review Still Matters

The agent wrote the code, but you own it. Read through it the same way you would review a pull request from a colleague. Does it follow your conventions? Is it readable? Did the agent introduce unnecessary complexity or dependencies you did not ask for?

A common trap: the agent produces code that works but is over-engineered. Extra abstractions, utility functions for one-time operations, error handling for scenarios that cannot happen. If you see this, you can ask the agent to simplify. Most agent tools have dedicated commands for this. In Claude Code, `/simplify` scans the changed code for reuse opportunities, unnecessary complexity, and quality issues, then fixes them automatically. Use it. Over-engineered code is a recurring pattern with agents, and having a one-command fix for it is valuable.

> **Tip:** Make it a team rule: every developer runs `/review` on their own code before asking for a human review. The agent catches convention violations, missing tests, and obvious issues before a colleague ever sees the code. This saves review cycles and raises the baseline quality of every pull request.

### Do an Agentic Review Before Sending to a Human

This is the step I see developers skip the most, and it is one of the most important.

Before you send your task for human review, ask your agent to review it against the original requirements. Not just "does the code work," but: did I actually do what the task required? Am I following the business rules? Did I miss an edge case from the acceptance criteria? Does this match the specification I was given?

The agent has your plan, your instruction file, and the full context of what was asked. Use that. Let it compare the output to the input. Let it find the gaps before someone else does.

What happens if you skip this? Well, the task reaches your architect. He has already read this article, so he knows exactly what to do. He runs the agentic review himself, finds the issues, and sends the task back to you with a list of things to fix. You fix them, resubmit, and the review passes.

But if you had done the agentic review yourself? Your architect opens the pull request, reads through clean code that matches the requirements, and says: "Beautiful piece of work, John." Save yourself a round trip. Do the review before you ask for one.

---

## Step 5: Integration Tests

Unit tests confirm that individual pieces work. Integration tests confirm that pieces work together. Your agent can write and run both, but you need to tell it which matters for the task at hand.

For any change that touches APIs, database schemas, or cross-service communication, integration tests are not optional. Add this to your instruction file as a rule. The agent should run the full integration suite before considering a task complete, not just the unit tests for the files it changed.

Before merging, ask yourself: if a different developer looked at this code tomorrow, would they understand it? Would they trust it? If the answer is yes, merge it. If not, iterate. Remember, the cost of another round is thirty minutes, not three days.

---

## Start With These Five Steps. The Rest Will Follow.

That is the core workflow. Five steps: setup your instruction file, share and maintain it, plan-review-build-test, review your own code with the agent, run integration tests. Do this for a few sprints with your team. Get used to agentic development. Build the muscle memory.

After a few weeks, you will see improvements. Your code reviews will be cleaner. Your plans will be sharper. Your agents will produce better output because your instruction files will be better. But you will also feel there should be more to it. You will start hitting friction points that the basic workflow does not solve.

Good. That means you are ready to grow.

### Add Integrations, One Pain Point at a Time

You will notice that you keep copying user stories from JIRA into your agent manually. So you add the JIRA and Confluence MCP integration, and now the agent reads the stories and the documentation directly. One less manual step.

Then you notice something about your debugging workflow. You run an integration test. It fails. You open the logs in CloudWatch. You read through them. You copy the relevant lines. You paste them into the agent. You ask for a fix. The agent proposes something. You apply it. You run the test again. It fails again. You go back to CloudWatch. Repeat ten times.

Now think about this instead: you run the integration test and instruct the agent to read the error in case of failure, check the logs through the AWS CloudWatch MCP, and propose a fix. Which workflow is faster? The answer is obvious. And yes, the agent will sometimes propose the wrong fix. That is what the tests are for. The unit tests and integration tests are how the agent validates its own work, the same way you validate yours.

Then you want to test the UI, so you add the Playwright MCP server. Now the agent can open your application in a browser, click through flows, and verify that what it built actually works end to end.

Then you get a security report with CWE findings that need fixing. The agent does not have the latest vulnerability fixes in its training data. So you add Context7, an MCP server that fetches current documentation for libraries and frameworks. Now the agent looks up the latest security advisories and applies the correct fix, not the one from six months ago.

Each integration solves a real friction point you hit during your daily work. You do not add them all on day one. You add them when the pain justifies it. That is how you grow: incrementally, driven by real needs, not by a checklist someone gave you.

### From Manual to Automated. Becoming Truly Agentic

At some point, something shifts. You have been running this workflow for a while. The instruction file is solid. The integrations are in place. The plan-review-build-test cycle is second nature. And you start thinking: "This is working quite well. Why am I still spending time on this part? And that part?"

That is the signal. When your agentic flow is strong enough that the individual steps are reliable, it is time to compose them. You take the steps that you have been running manually, one conversation at a time, and you chain them into automated processes. Plan, build, test, review, deploy. Not as separate actions you trigger by hand, but as a pipeline where you validate the output at the end, not at every step.

This is the leap from using agents to being truly agentic. You are no longer typing prompts and reviewing output in a loop. You are defining processes, validating outcomes, and letting the agents handle the execution. The human stays in control of the "what" and the "whether," while the agents handle the "how."

You do not get here on day one. You get here after your team has built trust in the workflow, after your instruction files are battle-tested, after your integrations cover the friction points that used to slow you down. But when you get here, the productivity multiplier is real.

---

## The Principle Behind It All: Symbiosis, Not Replacement

Everything described in this article is built on one idea: humans and AI agents are better together than apart. The human decides direction, reviews, thinks critically. The agent accelerates, executes, manages repetition.

It is not "AI will solve everything." It is not "AI will never replace programmers." It is something more practical: here is how we work together, here is how we scale it, here is how we maintain quality.

Your documentation does not just describe the code anymore. It drives the code. Your specifications do not just communicate intent to other humans. They communicate intent to agents that execute it. The quality of your thinking directly determines the quality of your output. In a sense, this is the purest form of engineering: define the problem precisely, and the solution follows.

The barrier to entry is lower than most teams expect. Start with the five steps. Add integrations when the pain tells you to. Automate when trust is earned. You do not need to prepare for six months. You need to start.

If your team is in the phase of "we have licences, but we don't know what to do with them", this is where you begin.

---

## Scaling Beyond Your Team

So your team is running well. The workflow is solid, the results are visible, and naturally you want to spread this across the organisation. You become the advocate. You present at internal meetups, you share your numbers, you offer to help other teams get started.

But here is the reality: your organisation is large. What worked for your team, your project, your tech stack, your clients, does not automatically transfer. The team next door has a different codebase, different constraints, different problems. The instruction file that makes your agent brilliant is useless for their legacy monolith. The integrations you rely on do not exist in their ecosystem.

One team's success is a proof of concept, not a rollout plan.

### Finding Your Path Forward

There are several ways to approach this, depending on your organisation's size, ambition, and budget.

**Learn from the community.** Open-source resources like the <span style="color:#00BFA5">***Shipped by Agents***</span> repository try to capture what works across different teams and contexts. New articles, patterns, and lessons learned get published regularly. It is free to use, free to adapt, and designed so that we all learn together. Start here if you want practical guidance without commitment.

**Build your own.** You can design your own organisational adoption framework. Define the roles, the processes, the metrics. Build internal training materials tailored to your specific tech stack. This works, but it takes time, dedicated people, and a willingness to iterate on the process itself, not just the code.

**Wait for the standard.** At some point, a standard will emerge. The same way Agile grew from a manifesto into certified frameworks with training programmes and consultancies, agentic development will get its own formalised methodology. It is not here yet. If your organisation can afford to wait, that is an option, but you will be behind those who started earlier.

**Acquire it.** You work for a large corporation. They can afford to buy what they need. Companies like <span style="color:#8E103E">**.msg Systems**</span> already offer training packs, structured adoption processes, coaching programmes, and enterprise-grade guidance for AI-assisted development. This comes with monitoring, quantification, traceability, and accountability built in. If your organisation needs those guarantees, and most enterprises do, acquisition is the fastest path to a scalable, repeatable process across dozens of teams.

No single approach fits every organisation. Most will combine several: start with open-source learning, build internal expertise, and bring in external support where the stakes or the scale demand it.

---

*The complete <span style="color:#00BFA5">**Shipped by Agents**</span> training material is open-source and available on GitHub: github.com/popescualextraian/shipped-by-agents*
