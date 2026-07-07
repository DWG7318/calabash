# Supervisor Techniques For Loop Engineering

Use this reference when acting as the main-thread supervisor for one or more loops.

## Supervisor Identity

The supervisor is the loop entrance and exit:

- Entrance: convert owner intent into a complete plan package and give it to the first working role.
- Exit: read final markdown, audit evidence, and decide acceptance.

The supervisor should not be the middle of the loop. In small-loop mode, composite checker and worker own the middle. In large-loop mode, planner, worker, checker, and router own the middle.

## Core Duties

1. Clarify the final objective.
2. Define module boundaries and non-goals.
3. Translate owner intent into operational requirements and explicit assumptions.
4. Frame the module problem, primary user/caller, and job-to-be-done.
5. Define architecture contracts and integration boundaries.
6. Produce the module solution file.
7. Produce the goal map file.
8. Produce the cell plan file.
9. Research and record available skills, MCP/tools, local CLIs, external tools, and model/capability profiles.
10. Define evidence, acceptance, risk, and blocked standards before launch.
11. Choose small-loop or large-loop mode.
12. Create or confirm coordination paths.
13. Send the full plan to the composite checker in small-loop mode, or to the planner in large-loop mode.
14. Track loop state from files, not from interruption-prone chat.
15. Read final markdown messages sequentially.
16. Run final local audit when needed.
17. Decide accept, revise, or block.
18. Capture stable lessons for future templates or skills.

## Planning Standards

A supervisor plan is good only if the working loop can run without constant supervisor help.

Every module stream must have three planning files before launch:

- `<module>-solution.md`: full module direction, final target, boundary, architecture-level decisions, risk, and resource inventory.
- `<module>-goals.md`: fixed goals, goal positioning, stage acceptance, and completion method.
- `<module>-cells.md`: fixed cells under each goal, concrete method, allowed/forbidden scope, checks, and acceptance.

Every plan set must include:

- Final objective in operational terms.
- Owner intent, assumptions, and unresolved questions.
- Ownership boundary.
- Architecture contracts and public/internal surfaces.
- Go/cell map from start to final outcome.
- Cell-level inputs and outputs.
- Allowed and forbidden scopes.
- Required tests, scans, and data checks.
- Risk gates and owner-confirmation gates.
- Resource inventory and resource research evidence.
- Worker method log requirements.
- Checker rejection criteria.
- Blocked/escalation criteria.
- Final markdown format.

Avoid vague cells such as "improve quality" or "finish module." Use observable outcomes such as "add field lineage query API and smoke test."

## Multi-Loop Operations

When several loops run concurrently:

- Use file queues for final messages.
- Do not depend on thread messages for completion.
- Read one checker final message completely before opening the next.
- Keep a short supervisor board with loop id, checker, worker, status, last final message, and next supervisor decision.
- Do not send new instructions to a loop while another final result is being audited unless urgent.

Suggested board:

```md
| Loop | Checker | Worker | State | Last artifact | Supervisor decision |
|---|---|---|---|---|---|
| source | checker-source | worker-source | running | - | - |
| job | checker-job | worker-job | waiting | - | - |
| candidate | checker-candidate | worker-candidate | final-review | 20260706-candidate-passed.md | pending audit |
```

## Launch Checklist

Before sending a plan:

- Confirm the three planning files exist: module solution, goal map, and cell plan.
- Confirm no planning file or shard exceeds 999 lines.
- Confirm index files list shard paths, line counts, and scopes when the plan is split.
- Confirm the three planning files agree on final objective and module boundary.
- Confirm the owner-defined plan version policy and current authoritative plan version are recorded, including project, project part/module, time, and iteration version components; otherwise explicitly route `owner_decision` before launch.
- Confirm owner intent has been translated into operational requirements.
- Confirm assumptions and unresolved questions are explicit.
- Confirm architecture contracts and downstream consumers are identified.
- Confirm the correct checker/worker pair.
- Confirm whether the loop is small-loop or large-loop.
- Confirm the current role compression and target role separation.
- Confirm model or reasoning-level allocation per role.
- Confirm role memory is isolated and only formal artifacts are shared.
- Confirm local skills were checked.
- Confirm MCP/tools were searched when needed.
- Confirm external resources were researched when local resources are insufficient or uncertain.
- Confirm no required resource is left as unknown.
- Confirm legal, identity, credential, payment, tax, privacy, security, and production-risk gates are explicit when relevant.
- Confirm the first working recipient: composite checker for small-loop, planner for large-loop.
- Confirm thread tools or manual paste route.
- Confirm coordination directories exist.
- Confirm the plan is complete, not just a first slice.
- Confirm the plan does not mix module ownership.
- In small-loop mode, confirm the composite checker knows it owns go/cell progression with the worker.
- In large-loop mode, confirm the planner is the first working role and router controls continuation/completion decisions.
- Confirm the worker knows to execute only formal planner or composite-checker tasks.
- Confirm method logs and checker messages are file-based.

## Monitoring Without Interruption

The supervisor may check:

- `coordination/checker-messages/` for final messages.
- `coordination/worker-method-logs/` for method progress when debugging.
- Git status for unexpected changes.
- Test artifacts named in checker final messages.

The supervisor should not poll worker/checker threads for ordinary progress unless the user asks or a loop appears stalled.

## Anti-Stall Moves

If a loop appears stalled:

1. Check whether a final or blocked markdown exists.
2. Check the worker method log timestamp.
3. Check whether the planner or composite checker has issued a formal task or formal rework.
4. If no activity is visible, send a short status request to the composite checker in small-loop mode or the planner/router in large-loop mode, not the worker.
5. Ask the controlling role to either continue the loop or write a blocked markdown.

Do not bypass the loop controller and take over the worker unless the controlling role is unavailable or the owner explicitly changes the structure.

## Final Acceptance

When a final markdown appears, the supervisor must read it as evidence, not as truth.

Audit:

- Does the final queue filename start with `LE_` and follow `LE_YYYYMMDD-HHMMSS_<module>_<plan-version>_<result>.md`?
- Does the main final queue file and every appendix file have 999 lines or fewer?
- If appendices exist, does the main final queue file list every appendix path, line count, and scope?
- Do the three planning files exist and agree with the final checker message?
- Does the result satisfy the owner intent and operational requirements?
- Did the loop preserve architecture contracts and downstream compatibility?
- Does the final message cover every planned go/cell?
- Do changed files stay within allowed scope?
- Are tests and scans named and plausible?
- Was the worker method log read?
- Did the checker reject or resolve method problems?
- Did the router path make sense for each major decision?
- Did planner avoid changing go/cell and only assign skill, MCP/tool, and model resources?
- Did retry history avoid repeating the same issue in consecutive deliveries?
- Does the final message objectively record the complete error/mistake process, or mark it `none_observed`?
- Does the final message objectively record the complete solution process?
- Does the final message objectively record methods used, failed methods, method changes, and working methods?
- Does the final message avoid future method-upgrade advice and speculative recommendations?
- Did the role model/capability profile preserve checker independence?
- Did role memory stay isolated except for formal artifacts?
- Were risk gates and owner-confirmation gates respected?
- Are remaining risks acceptable?
- Is the objective acceptance evidence sufficient?

If evidence is weak, revise the plan or ask the controlling role for a blocked/follow-up markdown.

## Owner Communication

Report to the owner in compact terms:

- What loop finished or blocked.
- What evidence was reviewed.
- What decision was made.
- What happens next.

Do not flood the owner with worker/checker middle-round chatter.

## Supervisor Failure Modes

Avoid these mistakes:

- Becoming a message relay.
- Sending half-formed plans.
- Launching without the three planning files.
- Leaving required resources as unknown.
- Treating resource discovery as optional when local resources are insufficient.
- Hiding assumptions instead of writing them down.
- Omitting architecture contracts and then letting worker infer them.
- Defining cells without evidence standards.
- Treating risk gates as something checker can figure out later.
- Launching workers directly instead of opening the loop through composite checker or planner.
- Allowing multiple checkers to own the same worker.
- Forgetting that small-loop checker compresses planner, checker, and router.
- Forgetting that small-loop is a transition state, not the final scale architecture.
- Letting worker and checker share the same memory or unchecked assumptions.
- Using the same model/capability profile for worker and checker when alternatives exist.
- Accepting results without reading method logs.
- Accepting final messages without reviewing router path and planner resource assignments.
- Expanding the plan mid-loop without telling the checker.
- Revising go/cell after launch without updating all three planning files.
- Using thread chat as a completion queue during concurrent loops.
- Confusing blocked, failed, and incomplete.

## Useful Supervisor Prompts

Start a loop:

```text
Use $loop-engineering-for-codex. Small-loop mode: you are the composite checker for <module>. Here are the three supervisor planning files: <module>-solution.md, <module>-goals.md, and <module>-cells.md. Own the fixed go/cell progression with your paired worker. Do not report to the main thread until you write the final markdown.
```

Start a large loop:

```text
Use $loop-engineering-for-codex. Large-loop mode: you are the planner for <module>. Here are the three supervisor planning files: <module>-solution.md, <module>-goals.md, and <module>-cells.md. Start with the first fixed formal task to the worker, then follow planner -> worker -> checker -> router -> planner until final markdown is written.

Planner limit: do not change go/cell, task objective, scope, tests, acceptance criteria, or sequence. Only assign skill, MCP/tool, and model/reasoning resources. If the plan is flawed, return `plan_defect` through router.
```

Ask for non-interrupting status:

```text
Status request only. Do not change files. If the loop is active, summarize the current go/cell and next controlling-role action in this thread. If blocked, write the blocked markdown in the checker-message queue.
```

Request a stronger final artifact:

```text
Your final checker message is missing required evidence. Do not continue to a new cell. Update or replace the final markdown with test results, method-log review, data checks, and remaining risks.
```
