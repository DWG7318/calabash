---
name: loop-engineering-for-codex
description: Organize large Codex work into supervisor-outside role loops for multi-module or multi-project execution. Also known as LE. Use when a task needs multiple Codex threads or agents, small-loop worker/composite-checker coordination, large-loop planner/worker/checker/router separation, fixed go/cell planning, three-file supervisor planning, planner resource matching, file-based result queues, method logs, anti-interruption coordination, or when several project streams must run concurrently without the main thread becoming a message relay.
---

# Loop Engineering For Codex

Short name: LE.

## Purpose

Use this skill to run large work as durable loops instead of ad hoc thread chatter.

The main Codex thread is the supervisor outside the loop. It designs the full plan, opens the loop, later reads final checker/router messages, and performs final acceptance. The middle loop runs without the supervisor as a relay.

## Core Model

```text
small loop:
supervisor outside -> composite checker receives full plan
composite checker <-> worker repeat until complete or blocked
composite checker writes final markdown
supervisor reads final markdown

large loop:
supervisor outside -> planner receives full plan
planner -> worker -> checker -> router -> planner
repeat until router completes or blocks
router/checker writes final markdown
supervisor reads final markdown
```

Use one checker per worker. Keep the pairing stable for the project stream.

```text
module-a worker <-> module-a checker
module-b worker <-> module-b checker
module-c worker <-> module-c checker
```

This paired worker/checker structure is the small-loop transition form. It is practical when the environment only exposes two execution roles, but it is not the final scale architecture. The final large-loop form keeps supervisor outside the loop and separates four working roles inside the loop: planner, worker, checker, and router.

For scale modes, model allocation, and memory isolation, read `references/scale.md`.

## Role Boundaries

Main thread:

- Define the final objective, module boundary, go/cell blueprint, and acceptance standards.
- Hand the full plan to the composite checker in a small loop, or to the planner in a large loop.
- Avoid acting as the relay for normal worker/checker traffic.
- Read final checker markdown messages from the filesystem queue.
- Decide whether the whole loop is accepted, needs a new plan, or is blocked.
- Act as supervisor: design strong plans, launch loops, monitor file queues, audit outcomes, and protect owner attention.

Checker:

- Act as sub-project manager and strict QA for one worker.
- Internally separate three functions: checker, router, and planner.
- Own the go/cell progression from the first go/cell to the final go/cell.
- Assign one formal task or formal rework item at a time.
- Read worker outputs, diffs, tests, scans, and method logs.
- Reject incomplete work, unsafe methods, module-boundary drift, missing tests, or poor evidence.
- Route each result to the correct next path: terminate, rework, continue planning, complete, or block.
- Keep go/cell fixed. If the supervisor plan is wrong, contradictory, or missing required detail, route it as a plan defect instead of changing it locally.
- Write the final markdown message only when the whole assigned plan is complete or truly blocked.

Worker:

- Execute only formal tasks assigned by the composite checker in small-loop mode, or by the planner in large-loop mode.
- Do not self-select the next cell.
- Maintain an append-only method log for every go/cell/rework round.
- Deliver implementation evidence to the checker.
- Do not write the final checker message.

## Plan Design Rules

Give the checker a complete plan package, not a partial sprint.

Before launching a loop, the supervisor must produce three plan files:

1. Module solution file: a broad, guiding, comprehensive plan for the whole module.
2. Goal map file: all goals, each goal's purpose, stage acceptance, and completion method.
3. Cell plan file: all cells under each goal, with step-level method, scope, checks, and acceptance.

Do not launch a worker/checker loop until all three files exist and agree with each other.

LE artifact line limit:

- No LE-created plan, prompt, method-log segment, final queue markdown, or coordination markdown may exceed 999 lines.
- Detail must be preserved by splitting files, not by shortening the plan.
- If an artifact would exceed 999 lines, create an index file plus numbered shards.
- The three supervisor planning files may be index files that point to detailed shards.
- Suggested shard names: `<module>-solution-01.md`, `<module>-goals-01.md`, `<module>-cells-GO-01.md`, `<module>-cells-GO-02.md`.
- Suggested rotating log names: `<module>-worker-method-log-001.md`, `<module>-worker-method-log-002.md`.
- Suggested final-record appendices: `LE_YYYYMMDD-HHMMSS_<module>_<plan-version>_<result>_part-01.md`.
- Every index file must list its shards, line counts, and scope.
- Before launch, handoff, final acceptance, or relaunch after `plan_defect`, run a line-count check and fix any file above 999 lines.

The plan package must include:

- Final objective.
- Owner-defined plan version policy and current authoritative plan version.
- Supervisor version suggestions, if any, clearly marked as non-authoritative.
- Module boundary and non-goals.
- Go stages from start to finish.
- Cells under each go.
- Inputs and expected outputs for every cell.
- Allowed files or allowed scopes for every cell.
- Forbidden scopes and module boundaries.
- Required tests, scans, and data consistency checks.
- Resource inventory: available skills, MCP/tools, CLIs, browser/computer tools, model/capability profiles, and missing resources.
- Resource research evidence: what was checked internally and externally before deciding that a resource exists, is missing, or is unsuitable.
- Worker method log path and requirements.
- Checker acceptance checklist.
- Rework, blocked, and escalation rules.
- Final checker markdown format.

Do not split the plan into "first round" and "second round" when the intended process is a loop to the final objective. The checker decides progression cell by cell.

Unknown resources are not acceptable in a launch plan. If a required skill, MCP/tool, external tool, or model capability is uncertain, the supervisor must research it before launch or explicitly mark the plan blocked. Use local skill/tool discovery first, then external/current research when the resource may exist outside the current environment.

Plan version policy is owner-defined. The supervisor must not invent or choose the authoritative version scheme. A valid owner-defined plan version must identify four components: project, project part/module, time, and iteration version such as `V1`, `V2`, `V3`, or `V4`. Separators and exact casing are owner-defined, but the four components are mandatory. The supervisor may suggest a concrete pattern such as `<project>-<part>-<YYYYMMDD>-V<N>`, but the owner must define or confirm the actual rule before it becomes authoritative. If a `plan_defect` forces changes to the three planning files, the supervisor must update all three files together and apply the owner-defined version rule. If no owner-defined rule exists, mark the revised plan as `owner_version_pending`, record the suggested options separately, and route `owner_decision` before relaunch.

## Supervisor Loop Control

The supervisor role belongs to the main thread or lead agent. The supervisor is outside the loop. It is not a relay, not a substitute checker, not a router, not a planner, and not a hidden worker.

The supervisor must:

- Convert owner intent into a precise module mission and fixed execution structure.
- Translate owner intent into complete go/cell plan packages.
- Produce and maintain the three supervisor planning files before launch.
- Define evidence, risk, dependency, and acceptance strategy before work begins.
- Choose the right worker/checker pairs and keep ownership boundaries clean.
- Start small loops by sending plans to composite checkers.
- Start large loops by sending plans to planners.
- Monitor file queues instead of relying on live thread interruptions.
- Read checker final messages sequentially and run any needed local final audit.
- Decide whether to accept the loop result, revise the plan, or mark the loop blocked.
- Preserve a calm operating rhythm when multiple loops run concurrently.

The supervisor must not:

- Micromanage worker/checker middle rounds.
- Send partial thoughts that interrupt active loops.
- Treat checker success claims as final without reading evidence.
- Open new loops before existing plans, queues, and ownership are clear.

For detailed supervisor techniques, read `references/supervisor.md`.

For deep supervisor responsibilities, read `references/supervisor-responsibilities.md`.

For the required three supervisor planning files, read `references/supervisor-planning-files.md`.

## Composite Checker Internal Functions

In small-loop mode, treat the checker as one thread performing three internal roles around the worker:

1. Planner: receive the fixed go/cell target from the supervisor plan or router path, then match resources.
2. Worker: execute the formal task and deliver evidence.
3. Checker: judge the worker result, evidence, tests, method log, and module boundary.
4. Router: choose whether to stop, rework, continue to planner, complete, or block.
5. Planner: if router continues or reworks, package the router-selected fixed go/cell or rework with skill, MCP/tool, and model choices.

The checker must not jump directly from review to worker instruction. After review, it must route first; if the route continues, the planner function must resource-package the fixed target before publishing the next worker instruction.

Router paths:

- Critical failure: stop the loop and write blocked markdown for the supervisor.
- Acceptable issue within retry policy: route back to planner for formal rework.
- Cell complete and loop not finished: route back to planner for the next formal task.
- Entire plan complete: write final passed markdown for the supervisor.
- Plan defect or owner-level decision needed: write blocked markdown or escalation markdown for the supervisor.

Planner duties:

- Match required skills for the fixed task.
- Find or select required MCP/tools for the fixed task.
- Select the model or reasoning level for the fixed task.
- Flag resource impossibility or plan defects to router instead of altering go/cell.
- Produce a complete formal task or formal rework message only after planning is complete.

Planner limits:

- Do not change go.
- Do not change cell.
- Do not change task objective, allowed scope, forbidden scope, tests, or acceptance criteria.
- Do not repair supervisor plan gaps locally. Route plan gaps through `plan_defect`.

Retry policy must be explicit. A repeated same blocker should not loop forever. By default, the same issue must not appear in two consecutive deliveries; if it does, router should block or escalate unless the plan defines a different limit.

For detailed checker/router/planner mechanics, read `references/checker-router-planner.md`.

## Go And Cell

Use `go` for a phase and `cell` for the smallest inspectable work package inside that phase.

Use this global ID format in every LE plan, task, method log, decision record, queue file, and final markdown:

- Goal ID: `GO-01`, `GO-02`, `GO-03`.
- Cell ID: `CELL-01.01`, `CELL-01.02`, `CELL-02.01`.
- Cell IDs must include their parent goal number before the dot. `CELL-01.03` means the third cell under `GO-01`.
- Full reference: `GO-01/CELL-01.03`.
- Round suffix for task/log cycles: `R01`, `R02`, `R03`, producing `GO-01/CELL-01.03/R01`.
- Use two digits for goal, cell, and round numbers from 01 to 99. If a sequence exceeds 99, expand only that sequence to three digits and keep it consistent.
- Do not use `GO-1`, `CELL-1.1`, bare `CELL-03`, "first goal", or "next cell" as authoritative IDs.
- Do not renumber go/cell IDs after launch. If the plan changes before launch, update all three planning files together. If the plan is wrong after launch, route `plan_defect`.

A good cell:

- Has one concrete outcome.
- Can be reviewed by reading a small diff plus evidence.
- Has explicit allowed and forbidden scope.
- Has focused tests or checks.
- Produces enough evidence for the checker to approve or reject it.

Avoid cells that mix unrelated backend, frontend, docs, schema, broad scans, and refactors unless the plan explicitly requires a release-level cell.

## Communication Rules

If Codex Desktop thread tools are needed, search for them before claiming they exist. Prefer `send_message_to_thread` for thread-to-thread messages. If thread tools are unavailable, output exact prompts for the user to paste manually.

For detailed direct-send/direct-receipt task footers, receipt tests, and incident diagnosis, use the global `codex-thread-bridge` skill when available.

Codex surface isolation risk:

- Do not assume messages sent through VSCode Codex, Codex Desktop, CLI, or another Codex surface are mutually visible.
- A worker can finish successfully while the checker does not receive the final answer if the worker/checker pair is split across surfaces or if one surface intercepts the communication channel.
- Treat "worker completed but checker did not continue" first as a communication-route defect, not as worker idleness.
- Repair only after a delivery failure is observed or strongly evidenced. The normal path is direct send and direct return, not waiting, polling, or active watching.
- A checker/planner must not actively wait for the worker after sending a task. Sending a valid thread message is expected to activate the receiver. After sending the task, the sender should end its turn unless it has local bookkeeping to finish.
- If the completion message does not arrive, use a one-time routing repair: inspect the paired worker thread tail, inspect local artifacts and method logs, or use the file queue. This is exception handling, not the steady-state loop.
- Record any cross-surface delivery gap and repair method in the final LE error/mistake process.

Direct thread communication receipt protocol:

- After finishing any cell, the worker's final visible reply in its own thread must be exactly: `完成，请检验`
- Do not replace the worker final visible reply with `已追发回执`, `回执失败，请人工转发：完成，请检验`, or any other receipt wording.
- If `send_message_to_thread` is actually callable in the worker environment, the worker should also send the same pure text `完成，请检验` to the controlling checker thread named in the task. This direct return message is the normal wake-up path.
- In an LE checker/worker loop, the receipt target must be the controlling checker thread. Do not set the supervisor/main thread as the worker receipt target for middle-loop cells.
- The worker must not hand-write `<codex_delegation>`, `source_thread_id`, `input`, or other XML wrappers. Codex Desktop wraps cross-thread messages when appropriate.
- Whether extra thread sending succeeds, fails, is unavailable, or returns a desktop-only error, the worker's final visible reply must still be exactly: `完成，请检验`
- The supervisor must judge thread-tool availability by an actual successful call, not by tool search results alone.
- If a thread tool call returns `Codex thread coordination is only available in the Codex desktop app.`, treat the current entry point as VSCode Codex or another non-Desktop surface. Do not change the worker receipt protocol; use a manual copy/paste task prompt or a file-queue route.
- Normal direct receipt flow is: checker/planner sends a formal task to worker; worker sends `完成，请检验` back through `send_message_to_thread` when possible; worker also ends its own thread with `完成，请检验`; checker treats the receipt only as "ready to validate" and must still run local acceptance.
- No role should use active waiting, repeated polling, or long blocking waits as the normal way to receive another role's work. Waiting wastes context and creates false stalls. Reliable direct message delivery plus fixed receipt text is the goal.
- After sending a worker task, the supervisor should not continue unrelated work in that same turn. Prefer making the worker task the final supervisor message so state does not drift.

The supervisor sends the plan to the composite checker in small-loop mode, or to the planner in large-loop mode. Normal middle-loop communication stays inside the working loop.

Normal intermediate traffic does not go to the main thread. The supervisor must not be used as a standing relay for worker receipts or checker task routing.

Final results go to the main thread by markdown file, not by thread message, when several loops may run concurrently. This prevents one thread message from interrupting or overwriting another stream.

## Task Publish Lock

The planner or composite checker must publish worker tasks only after finishing all current work.

Before sending a task or rework instruction, the planner or composite checker must have:

- Finished reading the worker delivery.
- Finished checking diffs, tests, scans, data, and method log.
- Formed a complete decision: pass, rework, blocked, or next cell.
- Written a clear task or rework instruction.

The planner or composite checker must not send half-formed thoughts, provisional instructions, or a worker task while still matching resources or reviewing.

Worker execution instructions must start with one of:

```text
Formal task: GO-01/CELL-01.01/R01
Formal rework: GO-01/CELL-01.01/R02
```

If a planner or composite-checker task message does not start with one of those headings, the worker must treat it as discussion only and must not execute.

## Method Logs

Each worker must maintain one append-only markdown method log for its loop.

The method log must record every go/cell/rework round:

- Objective.
- Understanding and assumptions.
- Method used.
- Why this method was selected.
- Files changed.
- Commands run.
- Results.
- Failed attempts and reasons.
- Risks and boundaries.
- Evidence handed to checker.
- Next adjustment.

The checker must read the method log during each review. The checker may reject a cell because of bad method even if the result appears to work.

Do not record secrets, verification codes, cookies, tokens, plaintext passwords, identity numbers, full phone numbers, payout accounts, or private credentials in method logs or checker messages.

## File Queue

Use a project-local coordination folder unless the user specifies another location:

```text
coordination/
  checker-messages/
  worker-method-logs/
  plans/
```

The checker writes a final message only after the complete assigned loop is finished or truly blocked.

Final checker/router markdown files are LE audit records, not only status signals. Use this filename format:

```text
LE_YYYYMMDD-HHMMSS_<module>_<plan-version>_<result>.md
```

Examples:

```text
LE_20260706-231455_personal-info_project-personal-info-20260706-V1_passed.md
LE_20260706-231455_source-management_owner-version-pending_plan-defect.md
```

Filename rules:

- Prefix every final queue file with `LE_` to mark it as a Loop Engineering artifact.
- Use local time for `YYYYMMDD-HHMMSS`.
- Use the owner-defined authoritative plan version. If the owner has not defined one, use `owner-version-pending` and route `owner_decision` before relaunch.
- Use filesystem-safe slugs for `<module>` and `<plan-version>` in the filename; preserve the exact owner-defined version inside the markdown metadata.
- Use one result value: `passed`, `blocked`, `plan-defect`, `owner-decision`, or `stopped`.

If the objective final record would exceed 999 lines, keep the main final queue file under 999 lines and move detailed timelines into `_part-01.md`, `_part-02.md`, and later appendices using the same base filename. The main final queue file must list all appendix files and line counts.

Every final markdown must objectively record:

- LE metadata: loop mode, module, plan version, result, checker, worker, planner/router if separate, and source planning files.
- Completion evidence: go/cell range, changed files, tests, scans, data checks, and boundary checks.
- Complete error/mistake process: every detected mistake, repeated issue, bad assumption, failed attempt, missed test, boundary drift, or plan defect, with when/how it was found.
- Complete solution process: how each issue was fixed or routed, what method changed, what verification proved it, and what remains unresolved.
- Complete method record: methods used, method changes, failed methods, working methods, and objective evidence for each.

Do not include future method-upgrade advice, recommendations, or speculative process improvements in the final markdown. If no error or mistake was observed, write `none_observed` in the error process section and still record the methods used.

The main thread reads these files sequentially as a stable result queue.

## Blocked And Escalation Rules

Worker/checker loops should solve normal implementation problems internally.

Escalate to the main thread only by checker markdown when:

- The plan is wrong or incomplete.
- Required owner input is missing.
- The module boundary is ambiguous.
- The same blocker survives repeated worker/checker turns.
- A security, legal, credential, payment, identity, or production-risk decision is needed.

Do not escalate ordinary test failures or code quality issues. Those belong inside the checker-worker loop.

## Templates

For reusable prompt and markdown templates, read `references/templates.md`.

For supervisor status, queue, and acceptance patterns, read `references/supervisor.md`.

For deep supervisor responsibility layers, read `references/supervisor-responsibilities.md`.

For three-file supervisor planning artifacts, read `references/supervisor-planning-files.md`.

For checker/router/planner internals, read `references/checker-router-planner.md`.

For small-loop versus large-loop architecture, read `references/scale.md`.
