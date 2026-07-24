# Desktop Calabash BI Runtime

## Purpose

The desktop runtime keeps the project's current product definition and latest
changes continuously visible while work is active.

It is intentionally smaller than the full dashboard. The compact window should fit
beside Codex, an IDE, or the product UI without becoming another complex application.


## Project-Initialization Contract

The BI is created in the same project-initiation transaction that creates the
`.calabash/` control tree. It is not deferred until a baseline is frozen. Bootstrap
must produce the configuration, receipt, semantic change feed, compact view, full
dashboard, project-local launchers, and a successful one-shot refresh.

The project-open checklist then treats the launcher as a normal project surface:

```text
open repository
→ launch Calabash Definition Window
→ verify CALABASH_BI_LIVE and matching state hash
→ begin Calabash or Loop work
```

If the project has no graphical desktop, it records `HEADLESS_PUBLISHED`, the reason,
and the exact published compact-view location. Headless mode does not waive freshness
or visibility.


## Operator Quick Start

Initialize BI as part of project initiation:

```bash
python calabash/scripts/bootstrap_calabash_bi.py \
  --project /path/to/project \
  --project-name "Project Name"
```

Start the normal lightweight desktop surface:

```bash
/path/to/project/.calabash/bi/launch-calabash-bi.sh
```

Or invoke the runtime directly:

```bash
python calabash/scripts/run_calabash_bi_desktop.py \
  --project /path/to/project
```

Record one material semantic change and rebuild both views:

```bash
python calabash/scripts/record_calabash_bi_change.py \
  --project /path/to/project \
  --type OWNER_DECISION \
  --summary "Owner selected guided first use" \
  --reason "Historical evidence left two materially different outcomes" \
  --status PROVISIONAL \
  --part "Product Architecture" \
  --record-id DEC-014 \
  --actor Owner
```

Run project and BI health checks:

```bash
python calabash/scripts/validate_calabash_project.py \
  --project /path/to/project

python calabash/scripts/calabash_bi_desktop.py doctor \
  --project /path/to/project

python calabash/scripts/run_calabash_bi_desktop.py \
  --project /path/to/project \
  --headless-once
```

Expected gates are:

```text
CALABASH_BI_BOOTSTRAP_PASS
CALABASH_PROJECT_VALID
CALABASH_BI_CURRENT
CALABASH_BI_LIVE
```

## Semantic Change Write-Through

A file edit alone is not a complete Calabash change. For every material semantic
change, the responsible process must complete this transaction:

```text
authoritative Calabash record changes
→ append BI_CHANGE_EVENT
→ rebuild summary / compact / full BI
→ verify new source fingerprint is visible
→ commit the transaction to Git when accepted
```

The compact surface may also show uncommitted `.calabash/` changes as
`WORKING_DRAFT`, but a draft must never be rendered as accepted definition.

## Reference Layout

```text
┌──────────────────────────────────────────────────────┐
│ Calabash — Project Name             CURRENT / DRAFT │
│ Baseline MINIMUM v1.4.0 · branch calabash/amend/... │
├──────────────────────────────────────────────────────┤
│ GRANDPA                                              │
│ Help clinicians deliver only reviewed plans.        │
│                                                      │
│ PRODUCT                                              │
│ Roles: Patient · Doctor · Operator                   │
│ Journey: Collect → Plan → Approve → Deliver          │
│ Ontology: Patient · Plan · Approval · Review         │
├──────────────────────────────────────────────────────┤
│ LATEST CHANGES                                       │
│ 10:42 Owner decision: doctor-only final approval     │
│ 09:55 UI signal: patients misread draft as final     │
│ Yesterday Workflow: device fallback made manual     │
├──────────────────────────────────────────────────────┤
│ ATTENTION                                            │
│ 1 blocking question · 1 UI drift · review Aug 15    │
├──────────────────────────────────────────────────────┤
│ Updated 10:42:05 · CALABASH_BI_LIVE                 │
│ [Refresh] [Open Full BI]                             │
└──────────────────────────────────────────────────────┘
```

## Display Contract

The compact surface must show:

1. **Identity** — project, baseline, branch, status.
2. **Definition** — Grandpa, roles, journey, ontology.
3. **Latest changes** — bounded append-only change feed.
4. **Attention** — blocking questions, contradictions, UI/Workflow drift, review.
5. **Freshness** — last refresh, source fingerprint, runtime state.
6. **Drill-down** — one action to open the complete dashboard.

## Lifecycle

```text
project opens
→ runtime starts
→ build current BI
→ calculate source fingerprint
→ display compact window
→ poll for Calabash changes
→ rebuild only when fingerprint changes
→ refresh visible content
→ write runtime freshness state
→ stop cleanly at project-session end
```

The runtime excludes its own generated files from the source fingerprint to avoid
self-triggered rebuild loops.

## Modes

### COMPACT_WINDOW

Uses a small native Tk window when available. Recommended for desktop Codex work.

### BROWSER_COMPACT

Uses `compact.html` with automatic refresh. It is the fallback when the native UI
library is unavailable or a browser window is preferred.

### HEADLESS_PUBLISHED

Runs without a window, continually rebuilding compact/full pages and runtime state.
It requires an explicit environmental reason and a known place where the Owner can
open the published BI.

## Runtime Isolation

The BI runtime is read-only with respect to product definition. It may write only
its generated presentation and runtime-state files.

It must not:

- answer Owner questions;
- modify baseline clauses;
- accept amendments;
- change Loop or Verification state;
- convert draft Git changes into accepted product meaning.

## Freshness

The runtime records:

```text
runtime state
last refresh timestamp
source fingerprint
baseline identity
Git branch and HEAD
number of uncommitted .calabash paths
process ID and presentation mode
```

If the source fingerprint changes and rebuild fails, the window changes to
`CALABASH_BI_ERROR`. If displayed content no longer matches current source state, it
shows `CALABASH_BI_STALE`.

## Startup Guidance

Preferred order at project start:

```text
1. open project repository
2. start Calabash BI launcher
3. verify CALABASH_BI_LIVE
4. start Calabash/SLK/CLK/GLK work
```

`start_with_project: true` means project tooling should invoke the launcher as part
of its normal project-open routine. It does not grant the BI permission to modify
anything beyond generated BI files.

## Platform Guidance

Bootstrap creates project-local shell and Windows command launchers. Teams may attach
those launchers to:

- an IDE/Codex project-open task;
- a desktop shortcut;
- a macOS LaunchAgent;
- a Linux `.desktop` or user service;
- Windows Task Scheduler.

OS-login autostart is optional. Project-open startup is the default because the BI
is project-specific.

## Multiple Projects

Each project has its own BI runtime, window title, `.calabash/` tree, source
fingerprint, and process state. Never merge multiple projects into one compact window
unless a separate portfolio BI is explicitly designed; portfolio BI is outside the
Calabash project baseline specification.
