# Checker, Router, Planner Composite Role

Use this reference when a single checker thread must also perform routing and planning inside a worker/checker loop.

## Role Composition

In small-loop mode, the composite checker thread has three internal functions. The worker is still a separate role; it appears in the sequence below only to show the operating order:

```text
Planner -> Worker -> Checker -> Router -> Planner
```

Do not split these into extra threads unless the owner explicitly asks. One checker may play all three internal roles, but it must keep the functions separate in its reasoning and artifacts.

This composite role is a small-loop compression. In the large-loop target architecture, planner, checker, and router are separate roles with separate models and separate memory.

The supervisor is outside the loop in both modes. It opens small loops by handing the plan to the composite checker. It opens large loops by handing the plan to the planner.

## Checker Function

The checker answers: "What is the quality and truth of the worker delivery?"

Check:

- Did the worker complete the assigned formal task or rework?
- Did changes stay in allowed scope?
- Were forbidden scopes untouched?
- Did tests, scans, and data checks run?
- Is the method log complete and sane?
- Did the worker avoid secrets and private credentials?
- Did the result preserve module boundaries?
- Did the worker repeat a previously rejected error?
- Is the result good enough to route forward?

The checker must produce a clear finding before the router acts.

## Router Function

The router answers: "Given the review result, which path should the loop take?"

Allowed paths:

1. `stop_critical`: severe problem, unsafe work, boundary break, serious data corruption, or untrusted state. Stop and write blocked markdown.
2. `rework_allowed`: problem exists but is small enough and within retry policy. Send to planner for a formal rework instruction.
3. `continue_next_cell`: current cell passes and the whole plan is not finished. Send to planner for the next formal task.
4. `complete_all`: the final go/cell passes. Write final passed markdown.
5. `plan_defect`: the supervisor plan is wrong, missing, or contradictory. Write blocked/escalation markdown. Do not let planner correct the plan locally.
6. `owner_decision`: legal, identity, credential, payment, production, or business decision needed. Write blocked markdown for supervisor.

The router must not send messages to the worker directly. It chooses a path, then hands the chosen path to planner if more worker work is needed.

## Retry Policy

Define retry policy in the plan when possible.

Default policy:

- The same issue must not appear in two consecutive worker deliveries.
- If the same issue repeats consecutively, route to `plan_defect` or `stop_critical` depending on severity.
- A cell should not loop indefinitely. If three total rounds do not resolve it, route to blocked unless the checker can prove a new tactic is likely to work.
- Low-severity new issues may be reworked if they are inside scope and do not indicate poor method.

The checker should mention retry counts in method review and final messages.

## Planner Function

The planner answers: "Which resources should the fixed task use?"

In large-loop mode, planner is the first working role after supervisor. In small-loop mode, the composite checker performs planner internally.

Planner is a resource allocator, not a plan editor. It must not change go, cell, task objective, scope, tests, acceptance criteria, or sequence. If the fixed plan cannot be executed as written, planner must report the issue to router as `plan_defect` or `owner_decision`.

Planner duties:

- Select relevant skills for the worker to use.
- Select MCP/tools or CLIs the worker should use.
- Select reasoning effort or model class when available.
- Copy allowed and forbidden scope from the fixed plan without changing it.
- Copy required tests, scans, data checks, and method log expectations from the fixed plan without changing them.
- Write the final formal task or formal rework instruction.

Resource matching:

- Skill: identify the skill name and when to read it.
- MCP/tool: identify needed tools and whether to search for them first.
- Reasoning/model: choose light, medium, high, or xhigh effort where the environment allows it.
- Model independence: use a different model from worker for checker when possible; otherwise use a higher reasoning profile and separate thread/memory.
- Memory isolation: list which formal artifacts may be read and avoid private role memory sharing.
- No resource: state when no special skill/tool is required.
- Plan defect: state why the fixed task cannot be resource-matched and return to router.

Planner must not publish until it has finished planning. This reinforces the task publish lock.

## Internal Decision Record

For each review cycle, the checker should keep or append an internal decision note, either in the checker thread or a project file if the project uses one:

```md
## GO-01/CELL-01.01/R01 decision

- Review finding:
- Router path:
- Retry count:
- Planner resource assignment:
- Skills selected:
- Tools selected:
- Reasoning level:
- Model or capability profile:
- Memory inputs allowed:
- Next instruction type: Formal task / Formal rework / Final markdown / Blocked markdown
```

This does not replace the worker method log. It records checker-side judgment.

## Formal Rework Planning

A formal rework instruction should include:

- The exact rejected issues.
- Whether each issue is result-level or method-level.
- What must change.
- What must stay unchanged.
- Additional tests/scans.
- Method log update requirements.
- Retry count and consequence if repeated.

## Formal Next-Cell Planning

A formal next-cell instruction should include:

- Why the previous cell passed.
- Which go/cell comes next.
- The next go/cell must be cited in full global format, such as `GO-01/CELL-01.02`.
- Resource assignments for the fixed go/cell.
- Resource matches: skill, MCP/tool, reasoning level.
- Allowed and forbidden scope.
- Required deliverables and checks.
- Method log requirements.

## Final Markdown Planning

Before writing final passed markdown, router must confirm:

- Every go/cell in the assigned plan is complete, or the router has blocked on a plan defect.
- No go/cell was changed, replaced, skipped, or reordered by planner.
- Method logs were reviewed.
- Retry history does not hide unresolved repeated issues.
- Risks are documented.
- The final markdown filename starts with `LE_` and follows `LE_YYYYMMDD-HHMMSS_<module>_<plan-version>_<result>.md`.
- The main final markdown and every appendix file have 999 lines or fewer.
- If the final record needs more than 999 lines, the main file lists appendix files and line counts.
- Complete error/mistake process is objectively recorded, or marked `none_observed`.
- Complete solution process is objectively recorded.
- Complete method record is included without future method-upgrade advice or speculative recommendations.
- Objective acceptance evidence is stated.

Before writing blocked markdown, router must confirm:

- The blocker is real and not ordinary implementation friction.
- Retry policy has been applied.
- The owner/supervisor decision needed is clearly stated.
- No secrets are included.
