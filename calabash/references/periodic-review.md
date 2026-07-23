# Periodic And Event-Triggered Review

## Review Is A Stage, Not Housekeeping

A Calabash review is a formal phase that tests whether the current baseline still
represents product intent and reality and whether the desktop definition window is
faithfully exposing that state.

Every baseline defines:

- time cadence;
- event triggers;
- review scope;
- required evidence;
- responsible Loop/Supervisor authority;
- Owner-exclusive escalation conditions;
- BI availability and freshness expectations.

No universal cadence is imposed. The project chooses cadence based on risk and
change velocity.

## Review Types

### Health Review

Short review of source freshness, open questions, contradictions, living-track
signals, trace validity, BI warnings, latest-change visibility, and launcher health.

### Theme Review

Deep review of one high-impact theme or one UI/Workflow drift cluster.

### Full Baseline Review

Re-read every active baseline part, major theme, unresolved risk, trace contract,
product outcome, BI dimension, and semantic change since the previous full review.

## Time Triggers

Examples:

- every defined number of days/weeks;
- before release;
- after a high-risk period;
- after the baseline maximum-staleness limit;
- when the desktop BI has not been opened or rebuilt within project policy.

## Event Triggers

Examples:

- user study or material UI behavior change;
- repeated workflow workaround;
- device/tool/vendor capability change;
- incident, security, legal, policy, or external contract change;
- SLK GO checkpoint, CLK Level barrier, GLK graph convergence, or project final
  audit when configured;
- `GO_DEFINITION_DEFECT`, repeated Verification gap, or product-effect gap;
- significant source contradiction or stale authority;
- `CALABASH_BI_STALE`, `CALABASH_BI_ERROR`, source-fingerprint mismatch, or missing latest change.

## BI Review Checklist

Every Health Review confirms:

- desktop service remains local-only and read-only;
- summary state hash matches governed source state;
- latest change event is visible in the window;
- current Grandpa, Product Architecture, and Ontology are not stale;
- blocking items are not hidden by overall status;
- UI and Workflow signal age is visible;
- review dates and trace health are accurate;
- launchers and optional desktop shortcut still work;
- generated dashboard contains no secret or credential.

## Review Record

```text
REVIEW_ID
BASELINE_ID / VERSION / HASH
TYPE
TRIGGER
SCOPE
SOURCES_RECHECKED
THEMES_REVIEWED
UI_SIGNALS
WORKFLOW_SIGNALS
CONTRADICTIONS
TRACE_IMPACT
BI_STATE_HASH
BI_FINDINGS
VERDICT
ACTIONS
NEXT_REVIEW_DUE
GIT_COMMIT
```

## Verdicts

```text
UNCHANGED
CLARIFICATION_REQUIRED
AMENDMENT_REQUIRED
MINIMUM_TO_FULL_UPGRADE_REQUIRED
CALABASH_DEFINITION_BLOCKED
BI_REPAIR_REQUIRED
```

A review never edits a frozen baseline in place.
