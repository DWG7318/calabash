# Calabash BI — Mandatory Bootstrap And Desktop Presence

## Purpose

Calabash BI is the continuously visible product-definition observability layer.
It must let an Owner or project operator answer, without opening the repository:

1. What is the current accepted Calabash?
2. What changed most recently?
3. Which changes are accepted, provisional, proposed, or blocked?
4. Where is UI reality drifting from the definition?
5. Where is core Workflow reality drifting from the definition?
6. What must be reviewed next?

Calabash BI is read-only. Git-backed Calabash records remain authoritative.
A dashboard must never become a second, mutable product-definition store.

## Mandatory Bootstrap Gate

Every project that creates or adopts Calabash must establish BI during project
initiation, before source preparation and Owner questioning are materially underway.

Required order:

```text
project initiation
→ create .calabash control tree
→ create BI configuration and desktop binding
→ issue CALABASH_BI_BOOTSTRAP_PASS
→ begin source preparation and Calabash creation
```

A project may not freeze a Calabash baseline or start product-affecting SLK, CLK,
or GLK work without:

- `.calabash/bi/config.json`;
- `.calabash/bi/bootstrap.json` with `CALABASH_BI_BOOTSTRAP_PASS`;
- a reproducible full dashboard build;
- a compact desktop view;
- a declared desktop startup policy;
- a working refresh path from authoritative records.

Bootstrap command:

```text
python calabash/scripts/bootstrap_calabash_bi.py \
  --project <project-root> \
  --project-name "<name>"
```

The BI starts in `DRAFT` even when no baseline exists. It evolves with source
preparation, Theme Map construction, Owner answers, amendments, UI/Workflow signals,
and reviews.

## Persistent Desktop Requirement

During an active project work session, Calabash must have one continuously visible
human-facing surface.

Preferred form:

```text
Compact Desktop Window
```

It is a small, auto-refreshing, optionally always-on-top window. It is not intended
to replace the full dashboard.

Run:

```text
python calabash/scripts/run_calabash_bi_desktop.py \
  --project <project-root>
```

For headless or restricted desktop environments, use the generated compact HTML as
the degraded equivalent and keep it pinned in a dedicated application/browser
window:

```text
.calabash/bi/compact.html
```

If no continuously visible surface can be maintained, record:

```text
BI_VISIBILITY_DEGRADED
```

with the reason and substitute display path. Silent omission is invalid.

Under the default `REQUIRED_WHILE_ACTIVE` gate, an already active safe CELL may
finish and reach its formal boundary, but no new Calabash decision, SLK CELL, GO,
CLK Level, GLK route, baseline freeze, or final closure may begin until the compact
surface is current again. `HEADLESS_PUBLISHED` is a declared alternate visibility
mode, not permission to omit BI.

## Lightweight Window Pattern

The default window is approximately `540 × 760` pixels and contains three tabs or
sections.

### Current

Show only the definition most needed for navigation:

- project name;
- overall definition status;
- baseline mode, version, hash, and Git commit;
- Grandpa purpose and non-negotiable boundaries;
- core roles;
- core entry points and business journey;
- core Ontology concepts;
- known gaps;
- next review date.

### Changes

Show the newest events in reverse chronological order:

- Owner decisions;
- accepted or proposed amendments;
- baseline freezes;
- UI change signals;
- Workflow change signals;
- review verdicts.

Every item should show:

```text
timestamp
change type and identifier
short summary
state
Git commit or evidence link
```

The compact window must label its definition block `Current accepted definition`.
It must never merge an uncommitted Git draft, provisional answer, experiment, or
observed UI/Workflow signal into that block. Those items appear only under `Latest
changes` or `Working state` until an accepted versioned amendment changes the
baseline.

The display must visually distinguish:

- current accepted definition;
- provisional/experimental decision;
- proposed amendment;
- observed drift not yet adopted;
- superseded history.

### Attention

Show only issues that can invalidate confidence or require action:

- blocking Owner decisions;
- blocked required claims;
- unresolved contradictions;
- high/critical UI drift;
- high/critical Workflow drift;
- overdue review;
- stale GO or GLK edge traces;
- invalidated Verification Contracts.

## Full Dashboard Pattern

The full dashboard provides detail behind the compact window.

Required views:

### Baseline identity

- mode, version, hash, commit, tag, and freeze date;
- current lineage and superseded versions;
- active SLK/CLK/GLK pins.

### Current definition

- Grandpa;
- Product Architecture roles, entries, journeys, and modules;
- Ontology concepts and relationships;
- Full Calabash layers when present;
- known gaps and upgrade triggers.

### Completeness

Completeness is based on the dynamic Theme Map, never a fixed question count.

For each required claim:

```text
SUPPORTED
DECIDED
OPEN
BLOCKED
MONITORING
```

Resolved completeness counts `SUPPORTED` and `DECIDED`. `MONITORING` is displayed
separately.

### Evidence health

- verified/unverified source counts;
- stale sources;
- claim evidence coverage;
- source-authority distribution;
- unresolved contradictions.

### Decision state

- open/blocking questions;
- answered and superseded questions;
- recommendation acceptance pattern;
- provisional/experimental decisions;
- required evidence and review triggers.

### Living tracks

- open UI signals by severity and age;
- open Workflow signals by severity and age;
- latest observations;
- drift themes;
- next required review.

### Trace health

- current/stale GO traces;
- current/stale GLK edge traces;
- invalidated Verification Contracts;
- accepted work affected by amendments.

### Evolution timeline

- baseline history;
- amendments;
- Owner decision commits;
- review results;
- UI/Workflow signals;
- adoption and supersession state.


Every material semantic change appends one `BI_CHANGE_EVENT` to the change feed.
The event summarizes what changed, why, affected Calabash parts, downstream impact,
status, record identifiers, and Git identity.

Git working-tree changes that have not passed the normal Calabash process are shown
as `WORKING_DRAFT`. They must never be displayed as accepted product definition.

## Auto-Refresh Contract

The desktop surface must refresh from `.calabash/` authoritative records at a
bounded interval. Default:

```text
5 seconds
```

Refresh must reread the append-only change feed and rebuild only the derived views:

```text
.calabash/bi/summary.json
.calabash/bi/dashboard.html
.calabash/bi/compact.html
```

`.calabash/bi/change-feed.jsonl` is an authoritative semantic input. Refresh must
never rewrite, reorder, or synthesize away its existing events.

The runtime writes heartbeat/state only to:

```text
.calabash/bi/runtime/state.json
```

Runtime state is ephemeral and should be ignored by Git. Refresh must not create
source-definition commits or mutate Calabash clauses.

## Presentation Mode And Project Startup

Each project selects one presentation mode:

```text
COMPACT_WINDOW
BROWSER_COMPACT
HEADLESS_PUBLISHED
```

`COMPACT_WINDOW` is the default for Codex desktop work. It uses the lightweight
native window. `BROWSER_COMPACT` keeps `compact.html` open in a dedicated browser or
application window. `HEADLESS_PUBLISHED` is allowed only when the environment cannot
present a local desktop and an explicit reason plus known published view are recorded.

The normal project setting is:

```json
{ "start_with_project": true }
```

This means the BI launcher is part of the project-open routine. OS-login startup may
be added for a small number of long-lived projects, but project-open startup remains
the project-level contract. A manual-only launch is invalid unless the project-open
checklist makes it mandatory and verifies `CALABASH_BI_LIVE`.

## Read-Only Boundary

The desktop window may:

- refresh;
- open the full dashboard;
- open evidence or repository paths;
- pin/unpin itself;
- display status and history.

It must not:

- edit a Calabash clause;
- answer an Owner question;
- accept an amendment;
- change a baseline version;
- mark a signal resolved;
- mutate a Loop trace.

All changes return through source preparation, Theme Map analysis, Owner decision
when required, Git amendment, impact analysis, and baseline adoption.

## Git and Snapshot Rules

Authoritative and durable:

```text
bi/config.json
bi/bootstrap.json
bi/change-feed.jsonl
Calabash source records that BI reads
```

Derived live outputs:

```text
bi/summary.json
bi/dashboard.html
bi/compact.html
bi/runtime/*
```

`bi/change-feed.jsonl` is append-only durable semantic history. It is read by the
projection but is never regenerated from the HTML output.

Live refresh does not require a Git commit. At baseline freeze, formal review, or
release handoff, create a reproducible BI snapshot tied to the exact Git commit.

Suggested path:

```text
.calabash/bi/snapshots/<baseline-version-or-review-id>/
```

## Privacy and Redaction

A desktop window may remain visible for long periods. Project configuration must
identify sensitive fields and use one of:

```text
NONE
PROJECT_DEFAULT
STRICT
```

The compact window should display short product-definition summaries, not credentials,
private user data, hidden reasoning, or unrestricted evidence bodies.

## No Opaque Single Score

One overall status may summarize blocking state, but it must not hide dimensions.
A green status must never conceal contradictions, stale sources, provisional product
choices, or UI/Workflow drift.

Suggested top-level states:

```text
DRAFT
BLOCKED
AT_RISK
REVIEW_DUE
CURRENT
BI_ERROR
```

## Validation

A valid BI deployment proves:

1. bootstrap record exists;
2. config validates;
3. summary and both HTML views build from a clean checkout;
4. compact payload contains current definition and latest changes;
5. desktop runtime can refresh once in headless mode;
6. runtime state is written outside authoritative records;
7. a material Owner decision appears in the next refresh;
8. the dashboard points to the same baseline version and Git identity as the repository.

Headless validation command:

```text
python calabash/scripts/run_calabash_bi_desktop.py \
  --project <project-root> \
  --headless-once
```
