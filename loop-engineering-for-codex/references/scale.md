# Scale Architecture: Small Loop And Large Loop

Use this reference when deciding whether a project should run as a small loop or a large loop, and how to isolate role models and memory.

## Supervisor Is Outside The Loop

Supervisor does not participate in the working loop.

Supervisor duties:

- Create the overall plan.
- Produce the three supervisor planning files: module solution, goal map, and cell plan.
- Research and record available skills, MCP/tools, local CLIs, external resources, and model/capability profiles before launch.
- Open the loop by handing the plan to the correct first working role.
- Monitor stable file queues.
- Read final markdown.
- Perform final acceptance or decide a new plan is needed.

Supervisor is not the middle runner, message relay, checker, router, planner, or worker.

## Direct Communication And No Active Waiting

Use direct role-to-role messages as the normal activation path.

In a checker/worker small loop:

```text
checker -> worker
worker -> checker
```

The supervisor must not become the standing relay between checker and worker.

Rules:

- After a checker sends a valid formal task to the worker, the checker should end its turn instead of actively waiting.
- After a worker completes a cell, the worker's visible final reply must be exactly `完成，请检验`.
- If direct thread tools are available, the worker should also send the exact text `完成，请检验` to the controlling checker thread.
- The receipt target for middle-loop worker completions is the controlling checker, not the supervisor.
- Do not use `wait_agent`, repeated polling, or long blocking waits as the normal receive mechanism.
- If a receipt does not arrive, diagnose it later as a communication incident: read thread tails or file artifacts, repair the route once if needed, and record the incident in the final LE markdown.
- A receipt only means ready for validation. The checker still verifies local files, tests, scans, method logs, and boundaries.
- The supervisor consumes final checker/router markdown files from the queue and performs final acceptance only after the loop exits.

## Small Loop

Small loop is the transition state.

Supervisor is outside. The working loop is only:

```text
composite checker <-> worker
```

Expanded sequence:

```text
supervisor outside -> composite checker receives full plan
composite checker as planner -> worker
worker -> composite checker for checking
composite checker as router -> composite checker as planner
repeat until complete or blocked
composite checker writes final markdown
supervisor outside reads final markdown
```

The composite checker performs three internal roles:

```text
planner + checker + router
```

Use small loop when:

- The environment currently exposes only one checker and one worker per stream.
- The project needs momentum before building a fuller agent organization.
- The work can be safely controlled by one checker that explicitly separates its internal functions.

Small loop is not the ideal final architecture. It is a compressed form of the large loop.

## Large Loop

Large loop is the target scale architecture.

Supervisor remains outside. The first working role is planner.

Working loop:

```text
planner -> worker -> checker -> router -> planner
```

Opening and closing:

```text
supervisor outside -> planner receives full plan
planner -> worker
worker -> checker
checker -> router
router -> planner for continue/rework
router -> final markdown for complete/block
supervisor outside reads final markdown
```

Role duties:

- Supervisor: define final objective, produce the three planning files, research resources, open the loop through planner, monitor file queues, audit final results, and protect owner attention.
- Planner: receive the fixed task target, match skill/MCP/tool/model resources, and assign formal work to worker without changing go/cell.
- Worker: execute formal tasks and formal rework, maintain method logs, and deliver evidence.
- Checker: judge quality, evidence, tests, method logs, boundary compliance, and risk.
- Router: select the next path based on checker result: stop, rework, continue, complete, plan defect, or owner decision.

Use large loop when:

- The project has high cost of mistakes.
- Multiple loops run concurrently.
- The plan is complex enough that checking, routing, and planning can interfere with each other.
- Independent memory and independent judgment are more important than speed.

## Migration Path

Start with small loop only as a controlled compression:

```text
composite checker = planner + checker + router
```

Migrate to large loop when:

- The composite checker becomes overloaded.
- Router decisions become complex or high-risk.
- Planner resource matching becomes a major part of the work.
- The same loop repeatedly stalls or repeats mistakes.
- The owner needs stronger independence between quality judgment, routing, and planning.

## Model Allocation

Each role may use a different model or reasoning level.

Recommended default:

- Supervisor: high or xhigh reasoning for plan quality and final audit.
- Planner: high reasoning when matching skills/tools/models for the fixed task.
- Worker: medium or task-appropriate reasoning; raise only for hard implementation cells.
- Checker: different model from worker when possible; otherwise higher reasoning than worker.
- Router: high or xhigh reasoning when routing can stop, escalate, or alter the project path.

Important rule:

- The checker model must differ from the worker model when the environment allows different models.
- If only one model family is available, separate the capability profile: different thread, different system instructions, different reasoning effort, and stricter evidence requirements.
- Do not let worker and checker share the same informal context and assumptions; that weakens independent checking.

Reasoning-level fallback:

```text
worker: medium
planner: high
checker: high or xhigh
router: high or xhigh
supervisor: high or xhigh for plan/audit
```

## Memory Isolation

Each role must have separate memory.

Do not share private role memory across:

- Supervisor
- Planner
- Worker
- Checker
- Router

Why:

- Worker memory can bias the checker into accepting worker assumptions.
- Checker memory can cause the worker to optimize for the checker instead of the task.
- Router memory must stay focused on path decisions and retry history.
- Planner memory must preserve resource-selection rationale without inheriting implementation tunnel vision.
- Supervisor memory must preserve owner intent and final acceptance context.

Allowed shared artifacts:

- Formal plan package.
- Formal task and formal rework messages.
- Worker method log.
- Checker finding.
- Router decision record.
- Planner resource assignment.
- Final markdown.
- Explicit test, scan, and data artifacts.

Forbidden shared artifacts:

- Hidden scratch memory.
- Unreviewed assumptions.
- Private chain-of-thought or internal reasoning.
- Secrets, credentials, tokens, cookies, verification codes, full identity numbers, full phone numbers, payout accounts.

## Memory Storage Pattern

Use separate files or threads per role.

Suggested project layout:

```text
coordination/
  plans/
  checker-messages/
  worker-method-logs/
  checker-decision-records/
  supervisor-audits/
```

Large-loop optional layout:

```text
coordination/
  role-memory/
    supervisor/
    planner/
    worker/
    checker/
    router/
```

Only promote information from one role to another through formal artifacts.

## Independence Rules

Planner independence:

- Must not change go, cell, task objective, scope, tests, acceptance criteria, or sequence.
- Must report flawed supervisor plans to router as `plan_defect` instead of repairing them locally.
- Must match resources before issuing a task.

Checker independence:

- Must inspect worker evidence as if it came from another author.
- Must not rely on worker confidence.
- Must read method logs and verify method quality.

Router independence:

- Must not automatically choose the route preferred by worker, checker, or planner.
- Must apply retry policy.
- Must stop or escalate if repeated issues appear.

Supervisor independence:

- Must not accept final markdown as truth.
- Must audit evidence and decide accept, revise, or block.
