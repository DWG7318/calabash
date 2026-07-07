# Loop Engineering Templates

## Supervisor Plan Package

```md
# Loop plan package: <module>

## Required planning files
- Module solution: `coordination/plans/<module>-solution.md`
- Goal map: `coordination/plans/<module>-goals.md`
- Cell plan: `coordination/plans/<module>-cells.md`
- Files agree on final objective and module boundary: yes / no
- Line limit checked: yes / no
- Every file and shard has 999 lines or fewer: yes / no
- Shard index:
  - `<path>`: `<line-count>` lines, scope `<scope>`

## Plan version control
- Owner-defined version policy:
- Project:
- Project part/module:
- Version time:
- Iteration version:
- Current authoritative plan version:
- Previous plan version:
- Revision reason: initial / plan_defect / owner_revision
- Owner confirmed version policy: yes / no
- Supervisor version suggestions, non-authoritative:

## Final objective
<What must be true when the entire loop is complete.>

## Owner intent and assumptions
- Owner intent:
- Operational requirements:
- Assumptions:
- Unresolved questions:

## Module boundary
- Owns:
- Does not own:

## Architecture contracts
- Public surface:
- Internal surface:
- Upstream inputs:
- Downstream consumers:
- Compatibility requirements:

## Pairing
- Small-loop composite checker:
- Large-loop planner:
- Checker:
- Router:
- Worker:

## Loop scale mode
- Mode: small-loop / large-loop
- Current role compression:
- Target role separation:
- Model allocation:
- Memory isolation:

## Coordination files
- Plan:
- Checker messages: `coordination/checker-messages/LE_YYYYMMDD-HHMMSS_<module>_<plan-version>_<result>.md`
- Worker method log:

## Resource inventory
- Skills checked:
- MCP/tools checked:
- Local CLIs/scripts checked:
- External resources researched:
- Model/capability profiles:
- Missing resources:
- Blocked resources:

## Risk and confirmation gates
- Security/privacy:
- Identity/credential:
- Payment/tax/legal:
- Production/destructive operations:
- Owner confirmation required:

## Global rules
- Supervisor stays outside the working loop.
- No LE-created plan, task, method-log segment, final queue markdown, or coordination markdown may exceed 999 lines.
- Preserve detail by splitting into index files and numbered shards, not by shortening the plan.
- Index files must list shard paths, line counts, and shard scopes.
- All go/cell IDs use the global format: `GO-01`, `CELL-01.01`, full reference `GO-01/CELL-01.01`, and round suffix `R01`.
- Do not use `GO-1`, `CELL-1.1`, bare `CELL-03`, or natural-language numbering as authoritative IDs.
- Do not renumber go/cell IDs after launch.
- In small-loop mode, composite checker owns go/cell progression with worker.
- In small-loop mode, composite checker internally performs planner, checker, and router functions.
- In large-loop mode, the working loop is planner -> worker -> checker -> router -> planner.
- This is a small-loop compression unless the plan explicitly separates checker, router, and planner.
- The worker executes only formal tasks or formal rework.
- Planner or composite checker sends worker tasks only after finishing resource matching for the fixed go/cell.
- Planner must not change go, cell, task objective, scope, tests, acceptance criteria, or sequence.
- The worker appends to the method log every round.
- The checker reads and judges the method log every round.
- Router or composite checker writes final markdown only after the whole plan passes or is blocked.
- The same issue must not appear in two consecutive worker deliveries unless the plan explicitly allows it.

## Go map

### GO-01: <name>
Goal:
Exit criteria:

#### CELL-01.01: <name>
Objective:
Inputs:
Allowed scope:
Forbidden scope:
Worker output:
Required tests:
Required scans:
Data checks:
Method log requirements:
Checker/router/planner requirements:
Checker acceptance:

#### CELL-01.02: <name>
...

### GO-02: <name>
...

## Final acceptance
- Tests:
- Scans:
- Data checks:
- Method log review:
- Remaining risk policy:
```

## Module Solution File

```md
# <Module> solution

## Final objective

## Product purpose

## Owner intent and operational requirements

## Assumptions and unresolved questions

## Users and downstream consumers

## Owned scope

## Non-goals

## Current system context

## Target capability

## Conceptual data/artifact model

## Architecture decisions and integration contracts

## Public API/MCP/CLI/UI surface

## Upstream inputs

## Downstream dependencies

## Security/privacy/identity/payment/legal boundaries

## Risk gates and owner-confirmation gates

## Risks and assumptions

## Resource inventory summary
- Skills:
- MCP/tools:
- Local CLIs/scripts:
- Browser/computer capabilities:
- Model/capability profiles:
- Missing or blocked resources:

## Resource research evidence
- Local skill discovery:
- Local tool discovery:
- External research:
- Accepted resources:
- Rejected resources:
- Blocked resources:

## Whole-module acceptance
```

## Goal Map File

```md
# <Module> goals

## GO-01: <name>
- Purpose:
- Entry conditions:
- Exit conditions:
- Stage acceptance:
- Evidence required:
- Dependencies:
- Outputs:
- Tests/scans/audits:
- Required resource classes:
- Blocked criteria:

## GO-02: <name>
...
```

## Cell Plan File

```md
# <Module> cells

## GO-01 / CELL-01.01: <name>
- Objective:
- Why this cell exists:
- Inputs:
- Allowed scope:
- Forbidden scope:
- Required work:
- Suggested method:
- Architecture contract affected:
- Worker evidence:
- Method log requirements:
- Focused tests:
- Full/regression tests:
- Scans:
- Data checks:
- Acceptance criteria:
- Rework criteria:
- Blocked criteria:
- Owner-confirmation gate:
- Downstream compatibility check:
- Resource needs:
  - Candidate skill:
  - Candidate MCP/tool/CLI:
  - Candidate model/reasoning level:
  - Planner may do additional tool discovery for this fixed cell: yes / no

## GO-01 / CELL-01.02: <name>
...
```

## Planner Or Composite Checker To Worker Formal Task

```md
Formal task: GO-01/CELL-01.01/R01

## Objective
<One concrete outcome.>

## Context
<Only the context needed for this cell.>

## Why this task is next
<Resource rationale based on the fixed go/cell and router path.>

## Resource match
- Skill:
- MCP/tools:
- Reasoning level:
- Model or capability profile:
- Memory/artifact inputs allowed:

## Allowed scope
- <file or directory>

## Forbidden scope
- <file or directory>
- <module boundary>

## Required work
1. ...
2. ...

## Required tests and scans
1. ...
2. ...

## Worker method log
Append this round to:
`coordination/worker-method-logs/<module>-worker-method-log.md`

Include objective, assumptions, method, why this method, changed files,
commands, results, failed attempts, risks, evidence, and next adjustment.

## Delivery to checker
Return summary, changed files, commands/results, risks, and method log path.
```

## Planner Or Composite Checker To Worker Formal Rework

```md
Formal rework: GO-01/CELL-01.01/R02

## Rejection reason
- ...

## Router decision
- Path: rework_allowed
- Retry count:
- Consequence if repeated:

## Required fixes
1. ...
2. ...

## Keep unchanged
- ...

## Additional tests or scans
1. ...

## Method log update
Append the rework round and explain the failed attempt and adjustment.
```

## Checker/Router/Planner Decision Record

```md
## GO-01/CELL-01.01/R01 decision

- Review finding:
- Router path: stop_critical / rework_allowed / continue_next_cell / complete_all / plan_defect / owner_decision
- Retry count:
- Planner resource assignment:
- Skills selected:
- Tools selected:
- Reasoning level:
- Model or capability profile:
- Memory inputs allowed:
- Next instruction type: Formal task / Formal rework / Final markdown / Blocked markdown
```

## Worker Method Log Entry

```md
## YYYY-MM-DD HH:mm:ss / GO-01 / CELL-01.01 / R01

- Objective:
- Understanding and assumptions:
- Method used:
- Why this method:
- Files changed:
- Commands run:
- Results:
- Failed attempts and reason:
- Risks and boundaries:
- Evidence handed to checker:
- Next adjustment:
```

## Router Or Composite Checker Final Message

```md
# LE final checker message: <module>

## Queue file
- Required filename format: `LE_YYYYMMDD-HHMMSS_<module>_<plan-version>_<result>.md`
- Actual filename:
- Main final queue file line count:
- Appendix files if needed:
  - `<path>`: `<line-count>` lines, scope `<scope>`
- Result value: passed / blocked / plan-defect / owner-decision / stopped

## LE metadata
- LE artifact: final-queue-md
- Loop mode: small-loop / large-loop
- Plan ID:
- Authoritative plan version:
- Owner-defined version policy confirmed: yes / no
- Module:
- Conclusion: passed / blocked / plan-defect / owner-decision / stopped
- Worker:
- Checker:
- Planner:
- Router:
- Source planning files:
  - Module solution:
  - Goal map:
  - Cell plan:

## Completion evidence
- Completed go/cell range:
- Allowed scope:
- Actual changed files:
- Key implementation summary:
- Test commands and results:
- Scan commands and results:
- Data consistency check:
- Sensitive data check:
- Module boundary check:
- Worker method log path:
- Worker method log read: yes / no
- Method issues:
- Method verdict: pass / fail
- Router path: complete_all / stop_critical / plan_defect / owner_decision
- Planner resource assignments:
- Planner changed go/cell: no
- Retry history:
- Model/capability profile used:
- Memory isolation check:
- Remaining risks:
- Objective acceptance evidence:

## Complete error or mistake process
- Error process status: recorded / none_observed
- Full timeline:
  - `<GO/CELL/Round>`:
    - What went wrong:
    - Actor or source: supervisor / planner / worker / checker / router / tool / external
    - Detection signal:
    - Impact:
    - Evidence:
- Repeated issues:
- Bad assumptions:
- Missed tests or weak evidence:
- Boundary drift:
- Plan defects:

## Complete solution process
- Resolution timeline:
  - `<GO/CELL/Round>`:
    - Fix or routing decision:
    - Method change:
    - Verification:
    - Residual risk:
- Failed repair attempts and why they failed:
- Final working method:
- Evidence proving the fix:

## Complete method record
- Methods used:
- Method changes:
- Failed methods:
- Working methods:
- Objective evidence for each method:
```

## Supervisor Board

```md
# Loop supervisor board

| Loop | Checker | Worker | State | Current go/cell | Last artifact | Supervisor decision |
|---|---|---|---|---|---|---|
| <module> | <checker> | <worker> | planned/running/final-review/accepted/blocked | <go/cell> | <path> | <decision> |
```

## Supervisor Final Audit Note

```md
# Supervisor final audit: <module>

- Checker final message:
- Plan covered: yes / no
- Scope respected: yes / no
- Tests reviewed:
- Scans reviewed:
- Method log reviewed by checker: yes / no
- Remaining risks accepted: yes / no
- Decision: accept / revise plan / blocked
- Next supervisor action:
```
