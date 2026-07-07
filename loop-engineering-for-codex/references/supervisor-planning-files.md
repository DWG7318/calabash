# Supervisor Planning Files

Use this reference when preparing a module before any worker/checker loop starts.

The supervisor must create exactly three core planning files for each module stream. These files are the supervisor's main work product. Planner, checker, router, and worker must treat them as fixed inputs unless router reports `plan_defect`.

Each core planning file may be an index file if the detailed plan needs shards. No single planning file or shard may exceed 999 lines. Split detail into numbered files instead of reducing detail.

## Required Files

Use project-local paths unless the owner specifies another location:

```text
coordination/plans/<module>-solution.md
coordination/plans/<module>-goals.md
coordination/plans/<module>-cells.md
```

Optional shards:

```text
coordination/plans/<module>-solution-01.md
coordination/plans/<module>-goals-01.md
coordination/plans/<module>-cells-GO-01.md
coordination/plans/<module>-cells-GO-02.md
```

Do not start the loop until all three files exist, cross-reference the same module boundary, and define the same final objective.

Do not start the loop until every planning file and shard has 999 lines or fewer, and each index file lists shard paths, line counts, and shard scope.

## File 1: Module Solution

Purpose: give the complete module-level direction.

It must include:

- Module name and final objective.
- Owner intent translated into operational requirements.
- Explicit assumptions and unresolved questions.
- Product/business purpose.
- Users and downstream consumers.
- Scope owned by this module.
- Explicit non-goals.
- Current system context and known constraints.
- Target capability when the module is complete.
- Data model or artifact model at a conceptual level.
- Architecture decisions and integration contracts.
- Public API/MCP/CLI/UI surface expected from the module.
- Upstream inputs and downstream dependencies.
- Security, privacy, identity, payment, legal, and operational boundaries.
- Risk gates and owner-confirmation gates.
- Risks, assumptions, and unresolved questions.
- Resource inventory summary:
  - Skills available.
  - MCP/tools available.
  - Browser/computer/CLI capabilities available.
  - Model or reasoning profiles available.
  - Missing or uncertain resources.
- Resource research evidence:
  - Local skills checked.
  - Local tools/MCP checked.
  - External resources searched or reviewed when needed.
  - Why each resource was accepted, rejected, or left blocked.
- Final acceptance standard for the whole module.

Resource rule: the supervisor must not write "unknown" as a final resource state. Use `available`, `not_needed`, `unsuitable`, or `blocked_pending_research`.

## File 2: Goal Map

Purpose: define the fixed go structure from start to final outcome.

Each goal must include:

- Goal ID in `GO-01` format.
- Goal name.
- Why this goal exists.
- Entry conditions.
- Exit conditions.
- Stage acceptance standard.
- Evidence required to pass the stage.
- Dependencies on previous goals.
- Outputs produced.
- Required tests, scans, or audits.
- Required resource classes.
- Risks that would make this goal blocked.

Rules:

- Goals are fixed by supervisor.
- Planner must not add, remove, reorder, merge, or split goals.
- If a goal is wrong, router must report `plan_defect`.

## File 3: Cell Plan

Purpose: define the executable steps under each goal.

Each cell must include:

- Cell ID in `CELL-01.01` format under its parent goal.
- One concrete outcome.
- Why this cell exists.
- Inputs.
- Allowed files, modules, APIs, or data scopes.
- Forbidden files, modules, APIs, or data scopes.
- Required work.
- Suggested method.
- Architecture contract affected, if any.
- Worker evidence required.
- Method log requirements.
- Required focused tests.
- Required full tests or regression checks when needed.
- Required scans or sensitive-data checks.
- Data consistency checks.
- Acceptance criteria.
- Rework criteria.
- Blocked criteria.
- Owner-confirmation gate, if any.
- Downstream compatibility check, if any.
- Resource needs:
  - Candidate skill.
  - Candidate MCP/tool/CLI.
  - Candidate model/reasoning level.
  - Whether planner may perform additional tool discovery for this fixed cell.

Rules:

- Cells are fixed by supervisor.
- Use `GO-01`, `CELL-01.01`, and full references such as `GO-01/CELL-01.01` everywhere.
- Cell IDs must include the parent goal number before the dot.
- Do not use `GO-1`, `CELL-1.1`, bare `CELL-03`, or natural-language numbering as authoritative IDs.
- Do not renumber goals or cells after launch; route `plan_defect` if the launched plan needs structural correction.
- Planner must not change cell objective, scope, tests, or acceptance.
- Worker must not start a cell unless the instruction begins with `Formal task:` or `Formal rework:`.
- Checker must judge the worker against the cell plan, not against worker intent.
- Router must use `plan_defect` if a cell cannot be executed as written.

## Resource Research Standard

Supervisor must know the resource universe well enough to avoid blind planning.

Before launch, check:

1. Local skills: inspect available skill names/descriptions and load relevant skill files.
2. Local MCP/tools: search tool metadata when available, including thread, browser, design, GitHub, mail, automation, and project-specific tools.
3. Local CLIs/scripts: inspect project scripts, package commands, and known local tool installs.
4. External tools: when the required resource may exist outside the current environment, use web or primary-source research before declaring it unavailable or unsuitable.
5. Model/capability profiles: record which role needs light, medium, high, or xhigh reasoning; record if independent checker model separation is available.

Planner receives this resource inventory but still performs cell-level resource matching. Planner may search for a tool only within the fixed cell's resource need. Planner must not use resource discovery as a reason to change the cell.

## Handoff To Planner Or Composite Checker

The supervisor handoff must include:

- Paths to the three planning files.
- Owner-defined plan version policy.
- Plan version project component.
- Plan version project-part/module component.
- Plan version time component.
- Plan version iteration component.
- Current authoritative plan version.
- Supervisor version suggestions, if any, marked as non-authoritative.
- Current module boundary.
- Fixed goal and cell list.
- Resource inventory summary.
- Whether the loop is small-loop or large-loop.
- The first fixed goal/cell to execute.
- The rule that planner cannot change go/cell.
- The rule that plan defects go to router and then supervisor.
- The rule that only owner-defined plan versions are authoritative.

## Supervisor Pre-Launch Checklist

Before handoff, confirm:

- The module solution file exists.
- The goal map file exists.
- The cell plan file exists.
- Every planning file and shard has 999 lines or fewer.
- Index files list all shards, line counts, and shard scopes.
- The three files agree on final objective and module boundary.
- Every goal has exit criteria.
- Every cell has concrete acceptance criteria.
- Every cell has allowed and forbidden scope.
- Architecture contracts and downstream compatibility checks are defined when relevant.
- Risk gates and owner-confirmation gates are defined when relevant.
- Tests and scans are executable or explicitly blocked.
- Resource inventory has no unresolved `unknown`.
- External resource claims were researched when needed.
- Planner is only allowed to assign skill, MCP/tool, and model resources.
- Router has clear `plan_defect` and blocked rules.
