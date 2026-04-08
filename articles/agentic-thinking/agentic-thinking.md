# Think Like an Agent User: How to Find What You Should Automate

You have an AI coding agent. You use it daily. It writes code, generates tests, helps you debug. But here is a question most developers never ask themselves:

**What are you still doing by hand that the agent could do for you?**

Not in theory. Right now. In your actual daily work. The tasks you repeat without thinking, the copy-paste rituals, the manual checks, the things you do on autopilot because you have always done them that way.

This article is about building a habit: **introspection**. Regularly looking at your own workflow, spotting the manual steps, and asking — can I bring the agent into this?

The developers who get the most out of AI agents are not the ones who write the best prompts. They are the ones who keep finding new places to apply the agent. They treat their workflow as something that evolves, not something that is fixed.

---

## The Introspection Habit

Most developers fall into a pattern with their agent. They find two or three things it does well — writing boilerplate, generating tests, explaining unfamiliar code — and they stop there. The agent becomes a tool for a narrow set of tasks. Everything else stays manual.

The problem is not the agent. The problem is that nobody told you to look for more.

Here is a simple exercise. At the end of your work day, or at the end of a sprint, ask yourself:

1. **What did I do manually today that felt repetitive?**
2. **Where did I copy-paste something between tools?**
3. **What took me longer than it should have?**
4. **Where did I act as a middleman between two systems?**

Each honest answer is a potential automation. Not all of them will be worth pursuing. But some of them will save you hours every week — and you will never find them if you do not look.

---

## A Catalog of Things You Might Not Realise You Are Doing by Hand

Let us walk through the most common manual habits I see in teams that use AI agents. You will probably recognise yourself in at least a few of these.

### Testing from Postman

You write an endpoint. You open Postman. You create a request. You set the headers, the body, the auth token. You hit Send. You read the response. You tweak the request. You hit Send again. When it works, you move on.

But those Postman requests are test cases. They validate your API. And they live in Postman, disconnected from your codebase, invisible to your agent.

**What to do instead:** Ask your agent to generate integration tests from your API specifications. If you have existing Postman collections, ask the agent to convert them into automated test files that run in your CI pipeline. The agent can create tests, manage them alongside your code, and execute them — all within the same workflow. No more switching tools. No more manual test runs that nobody else can reproduce.

### Copy-Pasting Errors from Log Platforms

You run your application. Something fails. You open CloudWatch, Datadog, Kibana, or whatever logging platform your team uses. You scroll through logs. You find the relevant error. You copy it. You paste it into the agent. You ask for help.

You are the middleman between your logging system and your agent.

**What to do instead:** If an MCP integration exists for your log platform, connect it. The agent reads the logs directly, finds the relevant error, correlates it with the code it just changed, and proposes a fix. If no MCP exists, you can still improve: pipe error output from your test runs directly into the agent's context. Many agents can read stderr output when they run your tests. The less you copy-paste, the faster the feedback loop.

### Writing User Stories by Hand

You sit in a refinement session. The product owner describes a feature. You open JIRA. You type a title. You write the description. You add acceptance criteria. You estimate. You repeat for the next story. And the next.

Meanwhile, you have a Confluence page with the feature requirements, a conversation thread with the product owner, and an agent that can read all of it.

**What to do instead:** Point your agent at the requirements document. Ask it to draft user stories with acceptance criteria. Review and refine them — the agent does the heavy lifting, you do the thinking. With a JIRA integration, the agent can create the stories directly in your project board. You go from a forty-minute writing session to a ten-minute review session.

### Creating and Using Diagrams

You need an architecture diagram for a design document. You open draw.io or Mermaid Live. You drag boxes. You draw arrows. You realise you forgot a component. You rearrange everything. It takes thirty minutes and the result is decent but will be outdated next sprint.

**What to do instead:** Ask your agent to generate the diagram from the code. The agent reads the codebase and produces a Mermaid or SVG diagram that reflects the actual structure, not your memory of it. Update the diagram the same way: ask the agent, review the output, done.

But here is a deeper use for diagrams that most people miss: **use them to validate understanding**. When you ask the agent to draw a diagram of how a feature works, and the diagram is wrong, you have just discovered a knowledge gap. Say you ask for a sequence diagram of the authentication flow and the agent shows the token being validated by the API gateway when actually it is validated by the auth service. The diagram is not wrong because the agent is bad at diagrams. It is wrong because the agent's understanding of your architecture is wrong — and that understanding comes from the code it read and the instruction files you wrote. Treat incorrect diagrams as diagnostic tools. Ask: is the code misleading, or is the instruction file missing context? Fix whichever is the root cause. A wrong diagram is a visual test of the agent's knowledge — and failed tests are the most useful kind.

### Correcting the Agent on Things It Should Already Know

You ask the agent to implement a feature. It uses the wrong database client. You correct it. Next conversation, it does it again. You correct it again.

This is the clearest signal that your instruction file is incomplete. **If you have to tell the agent something more than once, it belongs in `CLAUDE.md`** (or your equivalent instruction file).

The rule is simple: if you asked, it was not understood from the instruction file. Every correction is a documentation gap. Fix the file, not the conversation.

---

## Learn From Every Session

Here is a practice that compounds over time: **have a real conversation with the agent during your task, and at the end, ask it to reflect.**

During the work, the agent will make mistakes. It will pick the wrong pattern, misunderstand a requirement, use a deprecated API. That is normal. Correct it, explain why, move on. But do not let those corrections vanish when the session ends.

At the end of the task, ask the agent: *"What did not go well in this session? What did you get wrong, and what would have helped you get it right?"* The agent will list the friction points. Some will be prompt issues. Some will be missing context. Some will be gaps in the instruction file.

Now you have a list of improvements. A new rule for `CLAUDE.md`. A missing integration. A pattern the agent did not know about. Each session makes the next one better.

**Make this systematic.** Use `/insights` after every session — not just the ones that went badly. Good sessions contain lessons too: approaches that worked, patterns the agent handled well, conventions it followed correctly. Capturing what works is just as important as capturing what does not.

One thing to watch for: session length. When a conversation gets too long and unfocused, the agent's output quality drops — a bloated context window produces worse results, not better. If you are past fifty exchanges and the agent starts losing the thread, start a fresh session with a clear prompt. Shorter, focused sessions beat marathon debugging conversations.

Over weeks, this turns your instruction file from a rough draft into a battle-tested knowledge base. The agent stops making the same mistakes. Your prompts get shorter because the context is already loaded. The quality of the output goes up without you doing more work per session.

---

## The Feedback Loop That Most Teams Miss

Individual introspection is powerful. Team-level introspection is transformative.

Most teams already do sprint retrospectives. They talk about what went well, what did not, and what to improve. But they almost never include their agent workflow in that conversation.

Add one question to your retro: **"Where did we do something manually that the agent could have done?"**

Collect the answers across two or three sprints and you will see patterns:
- Three developers are all copy-pasting from the same logging tool — time to add that integration
- Two people corrected the agent on the same architectural rule — time to update the instruction file
- One developer found a workflow that saves an hour per task — time to share it with the team

This is how team-level improvement happens. Not from a top-down mandate. From the accumulated observations of people doing real work.

---

## A Practical Example: The Debugging Loop

Let me walk through a concrete before-and-after to show how introspection changes a workflow.

**Before (the manual loop):**
1. Run integration test — it fails
2. Open CloudWatch in the browser
3. Search for the relevant log group
4. Filter by timestamp
5. Read through log entries
6. Find the error
7. Copy the error message and stack trace
8. Paste into the agent
9. Agent proposes a fix
10. Apply the fix
11. Run the test again — it fails again
12. Go back to step 2
13. Repeat five to ten times

Each iteration takes three to five minutes of manual log navigation. A tricky bug can eat an hour just in copy-paste overhead.

**After (the integrated loop):**
1. Run integration test — it fails
2. Agent reads the error output directly
3. Agent queries CloudWatch via MCP integration
4. Agent correlates the log entry with the code change
5. Agent proposes a fix
6. Agent applies the fix and reruns the test
7. If it fails again, the agent reads the new error and iterates

Same debugging process. But the manual steps — opening the browser, navigating the UI, copying text, switching windows — are gone. The agent handles the feedback loop. You review the fix when it works, not at every intermediate step.

You would never have built this integration on day one. You built it because you noticed, after the tenth debugging session, that you were spending more time navigating CloudWatch than thinking about the bug. That is introspection at work.

---

## What to Look For: A Quick Reference

When you do your introspection — daily, weekly, or per sprint — here are the signals to watch for:

| Signal | What It Means | Action |
|--------|--------------|--------|
| You copy-paste between tools | You are the middleman | Find or build an integration |
| You correct the agent on the same thing twice | The instruction file has a gap | Update `CLAUDE.md` |
| You explain something the code should make obvious | The code structure is misleading | Refactor, or add context to the instruction file |
| You ask the agent to search extensively for something | The agent lacks knowledge of the codebase | Add architecture notes to the instruction file |
| A generated diagram is wrong | The agent's model of your system is wrong | Diagnose: is it the code or the instruction file? |
| You manually run a check before every commit | The check should be automated | Add it to your agent's workflow or CI |
| You switch to a browser to verify something | The agent could verify it for you | Look for an MCP integration or script it |
| A session went smoothly | Something worked well | Capture the pattern — it is worth preserving |

---

## Start Small, But Start

You do not need to automate everything tomorrow. You do not need to integrate every tool on day one. You need to build one habit: **notice what you are doing manually**.

Pick one thing from your last work day. One manual step, one copy-paste ritual, one repeated correction. Find a way to bring the agent into it. That is your first improvement.

Then do it again next week. And the week after. Over time, the compound effect is remarkable. Your workflow gets faster, your instruction files get richer, your agent gets smarter — not because the model improved, but because you improved the context it works with.

The best agent users are not the ones with the fanciest setups. They are the ones who keep asking: *"What am I still doing by hand?"*

---

*For a structured checklist to run this introspection with your team, see the [Agentic Workflow Review](../../process/01_agentic-workflow-review/01_agentic-workflow-review.md) process document.*

*The complete <span style="color:#00BFA5">**Shipped by Agents**</span> training material is open-source and available on GitHub: github.com/popescualextraian/shipped-by-agents*
