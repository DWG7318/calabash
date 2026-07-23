---
name: calabash
description: Use when creating, reconstructing, auditing, versioning, reviewing, or evolving a product-definition baseline; when historical material must be organized before Owner questioning; when dynamic themes, choice-based Owner decisions, Minimum or Full Calabash, Git lineage, UI/workflow feedback, Calabash BI, GO traces, or SLK/CLK/GLK grounding are required.
---

# Calabash

## Canonical Identity

- Product name: `Calabash`.
- Canonical repository: `https://github.com/DWG7318/calabash`.
- Default branch: `main`.
- Current specification version: `2.2.0`.
- Version source: repository `VERSION` file.

Calabash is a product-definition and governance method. It defines what a product
is, records why that definition is authoritative, and keeps the definition
traceable while the product evolves.

Calabash is not a feature module, runtime, Worker topology, GO scheduler, fixed
questionnaire, PRD template, or substitute for SLK, CLK, or GLK.

## Core Principle

```text
A Calabash version is closed.
The Calabash lineage is open.
```

A frozen version is immutable and reproducible. New evidence, Owner decisions, UI
behavior, workflow reality, device/tool maturity, or product learning create a new
append-only version; they never silently rewrite history.

## Two Forms

### Minimum Calabash

Minimum Calabash is exactly:

```text
Grandpa
→ Product Architecture
→ Ontology
```

It is the smallest product-definition baseline accepted by product-facing Loop
Engineering.

### Full Calabash

Full Calabash is:

```text
Grandpa
→ Product Architecture
→ Ontology
→ Contract
→ Policy
→ Workflow
→ Action Catalog
→ Adapter
→ Eval & Audit
```

Minimum omission means “not yet frozen in Calabash,” not “unnecessary.” When an
omitted governance area becomes material, derive, review, and version it before the
affected work is accepted.

Read `references/minimum-calabash.md` and `references/architecture.md`.

## Product-First Order

```text
Owner intent and verified project reality
        ↓
Full or Minimum Calabash
        ↓
PROJECT_CALABASH_BASELINE
        ↓
SLK / CLK / GLK
```

Do not begin from Agent, model, MCP, repository folders, Worker count, Chain, Level,
or Graph.

## Creating Calabash

Calabash creation is evidence-first, question-last, and observable from the start.

```text
1. Project identity and BI bootstrap
2. Historical source discovery and preparation
3. Source self-verification
4. Dynamic theme synthesis
5. Filtered Owner decision interview
6. Immediate write-through and BI refresh after every material change
7. Consistency, completeness, and BI freshness audit
8. Baseline freeze, Git tag, and BI snapshot
9. Continuous desktop visibility, observation, review, and amendment
```

### Mandatory BI Bootstrap And Desktop Presence

Before material source preparation or Owner questioning, create the project-local BI,
select its desktop startup policy, build the first `DRAFT` view, and record:

```text
CALABASH_BI_BOOTSTRAP_PASS
```

No Owner question may be asked before `SOURCE_PREPARATION_PASS` unless the missing
source itself is Owner-exclusive and blocks preparation.

Read `references/creation-protocol.md`, `references/source-preparation.md`, and
`references/calabash-bi.md`.

## Historical Material First

Before questioning the Owner, collect and normalize relevant material, including:

- prior Owner statements and decisions;
- approved product and business documents;
- current UI, user journeys, and production behavior;
- domain models, data, contracts, workflows, and audit records;
- user research, feedback, support cases, and analytics;
- implementation evidence, while distinguishing current behavior from intended
  product meaning;
- earlier Calabash versions and Loop evidence.

Each source receives provenance, authority, freshness, scope, confidence, and
contradiction status. Facts, normative decisions, and AI inference must remain
separate.

“Self-verified” means source identity, consistency, freshness, and evidentiary
support were checked. It never means AI memory or confidence proved truth.

## Dynamic Theme Map

Questions are organized under project-specific themes recorded in:

```text
CALABASH_THEME_MAP
```

A theme is a coherent product decision area, such as “doctor approval authority,”
“first-use onboarding,” or “offline device fallback.” A theme may span several
Calabash parts.

Themes are derived from prepared evidence, contradictions, missing claims, and
product risk. There is no fixed theme count, question count, universal interview,
or mandatory question bank.

Reference layer names may be used as discovery lenses, but a blank template field
is not sufficient reason to ask the Owner a question.

## Owner Decision Interview

Only questions that remain material after source preparation enter the interview.

Every question is a versioned `OWNER_DECISION_QUESTION` with:

- theme and Calabash-part references;
- verified evidence summary;
- the unresolved product decision and why it matters;
- `SINGLE` or `MULTI` choice mode;
- decision-complete options and consequences;
- one AI-recommended answer, confidence, rationale, and trade-offs;
- an `OTHER_WITH_TEXT` path when listed options do not express Owner intent;
- affected baseline claims, GOs, traces, UI, workflow, and evidence.

Use `SINGLE` only when one option must be authoritative. Use `MULTI` only when the
choices are independently compatible.

AI recommendation is mandatory, but it is advice, not authority. When evidence is
insufficient, recommend `DEFER_AND_COLLECT_EVIDENCE` rather than inventing intent.

Owner answers may create, split, merge, retire, or extend themes and may generate
unlimited follow-up questions. Ask in dependency and impact order, not template
order.

An answer may be `FINAL`, `PROVISIONAL`, `EXPERIMENTAL`, or `DEFERRED`. UI and
Workflow answers are often prototypes and must carry evidence requirements and a
review trigger instead of being treated as permanently correct.

Read `references/owner-decision-interview.md`.

## Immediate Write-Through

Every Owner answer and every material source, signal, review, or amendment must be
processed in the same semantic cycle:

```text
material change
→ normalize the product-definition effect
→ update authoritative Calabash artifacts
→ update theme, decision, impact, and invalidation state
→ create one atomic Git commit
→ rebuild BI summary, change feed, compact view, and full dashboard
```

The persistent desktop window must show the accepted change on its next bounded
refresh. Do not wait until the end of an interview or work phase.

A changed answer creates a new superseding decision event and commit. It never
rewrites or deletes the earlier answer.

## Baseline Freeze

Creation stops because blocking definition claims are resolved, not because a
fixed question count was reached.

A baseline may freeze only after:

- source preparation passed;
- every blocking theme is decided, explicitly deferred, or Owner-blocked;
- contradictions are resolved or consciously accepted with consequences;
- required Calabash artifacts are internally consistent;
- known gaps and upgrade triggers are explicit;
- UI and workflow living-track status is initialized;
- `CALABASH_BI_BOOTSTRAP_PASS` exists;
- compact and full BI views rebuild from the exact repository state;
- the desktop runtime or declared degraded surface reports current freshness;
- BI reports no hidden blocking defect;
- the exact baseline content is versioned, hashed, committed, tagged, and paired
  with a reproducible BI snapshot.

Record `PROJECT_CALABASH_BASELINE` and `CALABASH_BASELINE_FREEZE`.

## Living Tracks

Two domains remain continuously influential even after baseline freeze.

### UI Reality Track

Final UI can change Product Architecture, Ontology, Policy visibility, Workflow,
Action semantics, and Eval criteria because actual users may understand and use the
product differently from the logical design.

Record UI observations, usability evidence, behavior patterns, accessibility,
journey drift, and information-architecture findings as `UI_CHANGE_SIGNAL` records.

### Core Workflow Reality Track

Core Workflow can change because device capability, tool maturity, latency,
reliability, human/manual boundaries, external constraints, and operational methods
change during real work.

Record actual state movement, exceptions, workarounds, tool/device constraints, and
automation-boundary findings as `WORKFLOW_CHANGE_SIGNAL` records.

Signals do not mutate Calabash directly. They trigger evidence review, a theme or
question update, impact analysis, and a versioned amendment when warranted.

UI and Workflow may be `CURRENTLY_SUPPORTED`, but remain `MONITORING`; they are never
permanently closed.

Read `references/continuous-evolution.md`.

## Git Governance

Every project-facing Calabash must use Git.

Recommended control tree:

```text
.calabash/
  baseline/
  sources/
  themes/
  questions/
  decisions/
  observations/ui/
  observations/workflow/
  reviews/
  traces/go/
  traces/edge/
  bi/
    config.json
    bootstrap.json
    summary.json
    change-feed.jsonl
    compact.html
    dashboard.html
    runtime/
      state.json
    snapshots/
```

Rules:

- `main` contains the latest accepted baseline lineage.
- Creation and amendment occur on dedicated branches.
- Every Owner answer is an atomic commit.
- Frozen baselines receive immutable tags.
- No force-push, history rewrite, or deletion of accepted decision records.
- Active Loop runs pin exact baseline ID, version, hash, and commit.
- A newer Calabash version does not silently change an active Loop.
- Every amendment includes impact analysis and explicit adoption/re-verification.

Read `references/git-governance.md`.

## Periodic Review

Every baseline declares time-based and event-based review triggers.

Typical event triggers include:

- meaningful UI study or user-behavior change;
- repeated workflow workaround or failure;
- device/tool maturity change;
- release, incident, policy change, or new external integration;
- SLK GO acceptance, CLK Level barrier, or GLK graph checkpoint when configured;
- stale source, unresolved contradiction, or BI drift warning.

Review outputs are:

```text
UNCHANGED
CLARIFICATION_REQUIRED
AMENDMENT_REQUIRED
MINIMUM_TO_FULL_UPGRADE_REQUIRED
CALABASH_DEFINITION_BLOCKED
```

Read `references/periodic-review.md`.

## Calabash BI Operating Surface

Calabash BI is a mandatory project operating surface, not a report generated after
completion. It is established at project initiation and remains current during
creation, Loop execution, observation, review, and amendment.

It has two complementary views:

```text
Compact Desktop Window
current definition + latest changes + immediate attention

Full Calabash BI
complete content + evidence + history + questions + drift + traces + reviews
```

During active project work, one compact surface must remain continuously visible.
The preferred implementation is a small auto-refreshing desktop window. A pinned
compact HTML window is the declared alternative for headless environments.

If visibility or freshness is lost, record `BI_VISIBILITY_DEGRADED`. Current safe
work may reach its next formal boundary, but no new Calabash decision, SLK CELL, GO,
CLK Level, GLK route, baseline freeze, or final closure may begin until BI is current.

The compact surface is organized around two explicitly named sections: `Current definition` and `Latest changes`, followed by `Immediate attention`.

The compact surface is organized around `Current definition`, `Latest changes`,
`Working state`, and `Attention`. The accepted-definition block is labeled
`Current accepted definition`; draft and observed changes never appear there.

The compact view must show:

- project, baseline mode/version/hash, branch/commit identity, and refresh time;
- Grandpa purpose and non-negotiable boundaries;
- key roles, entry points, business journey, and Ontology concepts;
- known gaps and next review;
- latest Owner decisions, amendments, baseline freezes, reviews, UI signals, and
  Workflow signals;
- blocking decisions, contradictions, drift, stale traces, and invalidated evidence.

Accepted definition, provisional decisions, proposed amendments, observed drift, and
superseded history must remain visually distinct.

Every material semantic change appends one `BI_CHANGE_EVENT` before the compact and
full BI are rebuilt.

BI is read-only. Git-backed Calabash records remain authoritative, and the window
must never edit a clause, answer a question, accept an amendment, or resolve a signal.

Completeness is calculated from the project-specific Theme Map, never from a fixed
question count. BI must expose actual definition content and visible dimensions; it
must not hide unknowns inside one opaque score.

Tooling:

```text
scripts/calabash_bi_desktop.py
scripts/bootstrap_calabash_bi.py
scripts/build_calabash_bi.py
scripts/run_calabash_bi_desktop.py
scripts/record_calabash_bi_change.py
```

Read `references/calabash-bi.md`.

## Relationship To Loop Methods

Calabash owns product meaning. Loop methods own execution.

### SLK — Small Loop Skill

For product-affecting work, SLK requires Full or Minimum Calabash before GO/CELL
planning. The combined Supervisor/Checker conversation may maintain the Calabash
lineage, but Checker acceptance must use frozen traces and may not redefine product
meaning.

A strictly non-product task may use a versioned `CALABASH_EXEMPTION` only when it
proves no user behavior, role, journey, ontology, workflow, policy, or product
acceptance can change.

### CLK — Chain Loop Skill

CLK always requires Full or Minimum Calabash before fixed Chain/Level planning.
Calabash grounds Chain ownership, Level outcomes, GO traces, Verification Contracts,
and final composition. CLK has no Grapher and cannot use Calabash to introduce
conditional graph routing.

`MSLK` is a legacy name for pre-2.0 Chain Loop Skill history.

### GLK — Graph Loop Skill

GLK always requires Full or Minimum Calabash before GO Graph construction. Each GO
records `GO_CALABASH_TRACE`; every graph edge records `EDGE_AUTHORITY_TRACE`.
Grapher routes only within the authority of the frozen Calabash and verified runtime
facts. Grapher cannot amend Calabash.

Read `references/loop-method-integration.md`.

## Traceability Chain

```text
source evidence
→ theme and decision
→ Calabash baseline clause
→ GO_CALABASH_TRACE
→ GO_VERIFICATION_CONTRACT
→ evidence and verdict
```

GLK adds:

```text
EDGE_AUTHORITY_TRACE
```

A missing, stale, or contradictory trace is `CALABASH_TRACE_INVALID`.

## Thirty-Six Hard Rules

1. Start from product reality and Owner authority, not agent/runtime design.
2. Declare `MINIMUM` or `FULL` baseline mode.
3. Minimum Calabash is exactly Grandpa, Product Architecture, and Ontology.
4. Full Calabash preserves all seven governance layers.
5. A frozen version is immutable; lineage evolves only by superseding versions.
6. Prepare and self-verify historical material before Owner questioning.
7. Separate normative decisions, descriptive facts, and AI inference.
8. No fixed questionnaire, question count, or universal theme count is permitted.
9. Themes must derive from project evidence, gaps, contradictions, and risk.
10. Do not ask questions already resolved by authoritative evidence.
11. Do not send routine engineering decisions to Owner.
12. Every Owner question must be single-choice or multi-choice and include an AI
    recommendation, rationale, confidence, and consequences.
13. Owner may provide an alternative answer not represented by the options.
14. Questions may branch and extend without a numerical limit.
15. Every answer is written through immediately and committed atomically.
16. Corrections supersede; they never erase.
17. Baseline freeze depends on resolved blocking claims, not interview length.
18. Every product-facing GO has a current `GO_CALABASH_TRACE`.
19. Every GO Verification Contract derives from its trace.
20. Every GLK edge has an `EDGE_AUTHORITY_TRACE`.
21. UI Reality and Core Workflow Reality remain permanent monitoring tracks.
22. Observations do not silently mutate a frozen baseline.
23. Product-definition changes require impact analysis and versioned amendment.
24. Active Loops remain pinned until they explicitly adopt a new baseline.
25. Git history, decision ledger, and frozen tags are mandatory.
26. Periodic and event-triggered reviews are mandatory.
27. Calabash BI must expose completeness, drift, contradictions, questions, review,
    evolution, and trace health.
28. Completeness may not be inferred from a standard question total.
29. Engineering success with wrong product effect returns to Calabash analysis.
30. Urgency, model confidence, or schedule cannot waive these rules.
31. Every project bootstraps BI while Calabash is still `DRAFT`.
32. Active work keeps a compact Calabash surface continuously visible.
33. Compact BI shows current product definition and latest semantic changes, not
    metrics alone.
34. Accepted definition and pending or observed changes must never be conflated.
35. BI is read-only and cannot become a second source of product truth.
36. A stale, failed, or unavailable BI surface must be reported explicitly; it may
    not silently claim the project definition is current.

## Required Outputs

A substantial Calabash engagement produces:

1. source register and preparation receipt;
2. dynamic Theme Map;
3. question and decision ledger;
4. Minimum or Full baseline artifacts;
5. baseline manifest, version, hash, and Git tag;
6. known gaps and upgrade triggers;
7. UI and Workflow living-track configuration;
8. periodic review policy;
9. Calabash BI bootstrap record, config, compact desktop view, full dashboard,
   change feed, runtime freshness, and versioned snapshots;
10. Loop-method handoff, traces, and invalidation rules.

## Common Mistakes

- Asking the Owner a template questionnaire before reading existing material.
- Treating code as authoritative product intent.
- Giving choices without an AI recommendation.
- Asking “please confirm” for decisions already supported by evidence.
- Waiting until the interview ends before writing answers.
- Calling a mutable document a frozen baseline.
- Letting UI or actual workflow drift without feeding Calabash.
- Editing old decisions instead of superseding them.
- Treating “100% questions answered” as completeness.
- Creating BI only after the baseline is complete.
- Showing only scores while hiding current definition and latest changes.
- Letting a stale desktop window imply that the Calabash is current.
- Using the BI window to edit or approve authoritative product definition.
- Letting SLK, CLK, Verification, Router, Planner, or Grapher redefine Calabash.
