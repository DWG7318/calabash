# Supervisor Responsibilities

Use this reference when acting as supervisor before, during, or after a Loop Engineering run.

Supervisor is the highest-leverage role. Worker quality, checker quality, and router decisions are limited by the plan the supervisor creates. Planner cannot change go/cell, so supervisor must make the fixed plan correct before launch.

## Responsibility Layers

### 1. Owner Intent Translation

Supervisor must turn loose owner intent into an executable mission.

Do:

- Identify the real business/product objective.
- Separate owner preference from hard requirement.
- Record assumptions explicitly.
- Resolve ambiguous words before they become cells.
- Define what success and failure mean in observable terms.
- Preserve owner language where it affects product direction.

Do not:

- Treat a brainstorm as a build plan.
- Convert uncertainty into hidden assumptions.
- Let worker or checker discover core product intent mid-loop.

### 2. Problem Framing

Supervisor must decide what problem the module actually solves.

Define:

- Primary user or caller.
- Job-to-be-done.
- Inputs and outputs.
- Current pain or gap.
- Why this module exists instead of another module.
- What gets easier, safer, faster, or more reliable after completion.

If the problem cannot be framed, do not launch the loop.

### 3. Module Boundary Ownership

Supervisor must draw the ownership box.

Specify:

- Owned data.
- Owned APIs, commands, UI, files, services, or workflows.
- Upstream dependencies.
- Downstream consumers.
- Explicit non-goals.
- Neighbor modules that must not be changed.
- Integration contracts that must remain stable.

Boundary mistakes are supervisor defects. Checker should reject boundary drift, but supervisor must prevent it.

### 4. Architecture And Contract Design

Supervisor must design enough architecture for cells to be safe.

Define when relevant:

- Data model or artifact model.
- API/MCP/CLI contract.
- Storage and migration expectations.
- Idempotency and retry behavior.
- Permissions and identity model.
- Traceability and audit model.
- Error states and recovery.
- Compatibility requirements.
- Public versus internal surfaces.

Supervisor does not need to over-design implementation internals, but must define contracts that other modules can rely on.

### 5. Evidence And Acceptance Design

Supervisor must define what proof will count.

For each goal and cell, specify:

- Focused tests.
- Full or regression checks.
- Data consistency checks.
- Sensitive-data or policy scans.
- Manual review evidence if unavoidable.
- Expected files or outputs.
- Negative cases.
- Acceptance threshold.
- Rework threshold.
- Blocked threshold.

Avoid subjective acceptance such as "looks good" or "works normally." Use evidence that checker can inspect.

### 6. Resource Intelligence

Supervisor must know the available resource universe before launch.

Inventory:

- Relevant skills.
- MCP/tools.
- Browser/chrome/computer-use capabilities.
- Local CLIs and scripts.
- Project commands and test runners.
- External tools or libraries.
- Model or reasoning profiles.
- Human/owner input gates.

Research order:

1. Local skill/tool discovery.
2. Project-local scripts and docs.
3. Existing repo patterns.
4. External/current research when local resources are insufficient or the resource may exist outside the environment.

Supervisor must not mark resource status as `unknown` at launch. Use `available`, `not_needed`, `unsuitable`, or `blocked_pending_research`.

### 7. Go/Cell Decomposition

Supervisor owns go/cell design.

A good goal:

- Has a meaningful stage outcome.
- Produces a stable artifact or capability.
- Has clear entry and exit conditions.
- Can be validated before moving to later goals.

A good cell:

- Has one concrete outcome.
- Has small reviewable scope.
- Has explicit allowed and forbidden scope.
- Has tests or checks.
- Produces evidence.
- Can fail without damaging unrelated work.

Supervisor must not rely on planner to fix cell size. Planner cannot change cells.

### 8. Sequencing And Dependency Control

Supervisor must decide the order.

Specify:

- Which goals must precede others.
- Which cells unblock later cells.
- Which outputs become inputs.
- Which cells can run in parallel.
- Which cells must stay serial because of shared state.
- Which dependencies are external or unstable.

Router may stop or continue, but it should not invent a new sequence. If sequence is wrong, route `plan_defect`.

### 9. Risk And Safety Control

Supervisor must classify risk before launch.

Consider:

- Security risk.
- Privacy or identity risk.
- Credential and secret handling.
- Payment, tax, or financial risk.
- Legal or compliance risk.
- Production data risk.
- Destructive filesystem or database operations.
- Third-party terms or platform policy risk.
- User trust and reputational risk.

Define what requires owner confirmation and what must be blocked.

### 10. Role Topology And Independence

Supervisor must choose the loop shape.

Decide:

- Small-loop or large-loop.
- Worker/checker pairing.
- Whether small-loop checker owns the compressed planner/checker/router functions.
- Model or reasoning level per role.
- Memory isolation rules.
- Shared formal artifacts.
- Final markdown queue path.

Checker independence is a supervisor responsibility. Do not use one shared informal memory for worker and checker if the environment allows separation.

### 11. Launch Gatekeeping

Supervisor decides whether the loop is allowed to start.

Launch only when:

- Three planning files exist.
- Final objective is stable.
- Module boundary is clear.
- Every goal has exit criteria.
- Every cell has acceptance criteria.
- Required resources are known or blocked.
- Risk gates are defined.
- Planner limits are explicit.
- Router has clear blocked and `plan_defect` paths.

If any item fails, do not launch. Improve plan or block.

### 12. Change Control

After launch, supervisor should not casually alter go/cell.

Rules:

- Worker cannot change the plan.
- Planner cannot change the plan.
- Checker cannot silently change the plan.
- Router can report `plan_defect`.
- Supervisor can revise the plan only after reading the defect evidence.

When supervisor revises a plan:

- Update all three planning files.
- Use only the owner-defined plan version policy for the new authoritative version.
- If no owner-defined version policy exists, mark the revision `owner_version_pending`, suggest options separately, and route `owner_decision` before relaunch.
- Record why the change was necessary.
- Preserve completed evidence.
- Restart or resume from a clearly named fixed go/cell.
- Tell the controlling role which owner-defined plan version is authoritative.

### 13. Queue And Concurrency Control

When several loops run, supervisor must prevent message chaos.

Maintain:

- Loop board.
- Plan file paths.
- Current status.
- Final message queue.
- LE final markdown filename format: `LE_YYYYMMDD-HHMMSS_<module>_<plan-version>_<result>.md`.
- Line-count state for every LE plan, log segment, final markdown, and appendix; each must have 999 lines or fewer.
- Last audited artifact.
- Owner decisions pending.

Do not let worker/checker threads interrupt each other. Prefer final markdown queues over live chat for completion.

Final queue markdown is also the objective loop audit record. It must record complete error/mistake history, complete solution history, and complete method history. It must not include future method-upgrade advice or speculative recommendations.

### 14. Final Audit

Supervisor final audit is not a rubber stamp.

Audit:

- Final markdown against all three planning files.
- Changed files against allowed scope.
- Tests and scans against required evidence.
- Method logs against expected method.
- Router paths and retry history.
- Planner resource assignments.
- Memory isolation and role independence.
- Remaining risks.
- Whether downstream consumers can safely rely on the result.

Supervisor may accept, revise the plan, or block. Do not accept only because checker says passed.

### 15. Learning Back Into The System

After a loop, supervisor should capture reusable learning.

Record:

- Plan defects found.
- Bad cell sizing patterns.
- Missing resources.
- Useful skills/tools.
- Repeated checker findings.
- Test gaps.
- Risk rules that should become templates.

Promote only stable lessons into skills or templates. Do not turn one-off project facts into global rules.

## Supervisor Non-Negotiables

- Never launch without three planning files.
- Never leave required resources as `unknown`.
- Never let planner change go/cell.
- Never use worker confidence as acceptance evidence.
- Never accept final markdown without auditing against the plan.
- Never hide owner-level legal, identity, credential, payment, tax, or production-risk decisions inside the loop.

## Short Mental Model

Supervisor designs the map, defines the finish line, chooses the available instruments, sets the safety rails, opens the race, and audits the finish. The middle loop drives; supervisor does not hold the steering wheel during normal laps.
