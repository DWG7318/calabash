# Calabash Construction Loop

Use construction loops to prevent large agent projects from drifting. Each loop should be small enough to verify in one pass.

## Roles

| Role | Responsibility | Recommended model strength |
|---|---|---|
| Supervisor | Defines the next micro-scope and owns final judgment | high / extra-high |
| Worker | Implements the scoped work | medium, escalate if repeated failure |
| Checker | Verifies output against QC and acceptance criteria | high / extra-high |
| Router | Chooses REDO, NEXT, COMPLETE, or STOP | medium |

The model strengths are guidance, not a hard dependency.

## Loop Protocol

```text
Supervisor defines micro-scope
        ↓
Worker produces artifact/change
        ↓
Checker compares against QC
        ↓
Router decides:
  REDO     -> return same micro-scope to Worker
  NEXT     -> return to Supervisor for next micro-scope
  COMPLETE -> close the goal
  STOP     -> escalate to Supervisor due to repeated failure, ambiguity, or risk
```

## Micro-Scope Rule

One loop should touch only one dominant concern:

- one contract
- one workflow segment
- one role page
- one adapter path
- one action family
- one test/evidence pack
- one deployment or release check

If a loop title contains "and" more than once, split it.

## QC Template

Each loop should include:

```text
Goal:
Scope:
Inputs:
Worker output:
Checker criteria:
Acceptance evidence:
Router stop rule:
Known risks:
```

## Stop And Escalate

Stop after two or three repeated failures on the same micro-scope. The Supervisor should then change one of:

- model strength
- scope size
- source of truth
- test method
- architecture assumption
- product requirement

Do not keep retrying the same vague instruction.

## Acceptance Standards

Prefer evidence that survives conversation memory loss:

- files committed to the repo
- tests and smoke commands
- screenshots
- event logs
- schema validation output
- audit records
- release notes or decision logs

Verbal claims are not acceptance evidence.
