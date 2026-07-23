# Calabash Creation Protocol

## Purpose

This protocol turns incomplete historical material and Owner knowledge into a
versioned Minimum or Full Calabash while keeping the evolving definition continuously
visible.

It is not a fixed interview template. It is an evidence-driven decision process.

## Lifecycle

```text
INIT
→ BI_BOOTSTRAP
→ CALABASH_BI_BOOTSTRAP_PASS
→ SCOPE_AND_MODE
→ SOURCE_DISCOVERY
→ SOURCE_PREPARATION
→ SOURCE_PREPARATION_PASS
→ THEME_SYNTHESIS
→ OWNER_DECISION_LOOP
→ BASELINE_CONSISTENCY_AUDIT
→ BI_FRESHNESS_AUDIT
→ BASELINE_READY
→ BASELINE_FROZEN
→ ACTIVE_MONITORING
→ REVIEW / AMENDMENT
```

## Phase 0 — Project And BI Bootstrap

Create the project-local `.calabash/` control tree and Calabash BI before substantial
source preparation or Owner questioning.

Required BI artifacts:

```text
.calabash/bi/config.json
.calabash/bi/bootstrap.json
.calabash/bi/change-feed.jsonl
.calabash/bi/summary.json
.calabash/bi/compact.html
.calabash/bi/dashboard.html
.calabash/bi/launch-calabash-bi.sh
.calabash/bi/launch-calabash-bi.cmd
```

Required actions:

1. choose `COMPACT_WINDOW`, `BROWSER_COMPACT`, or an explicitly justified
   `HEADLESS_PUBLISHED` mode;
2. set refresh, latest-change depth, and project-open startup policy;
3. generate the first `DRAFT` compact and full views;
4. make the desktop surface immediately launchable;
5. append the initial `BOOTSTRAP` BI change event;
6. record `CALABASH_BI_BOOTSTRAP_PASS`.

The initial view may contain mostly unknowns. It must expose them rather than wait
for a polished baseline.

Read `calabash-bi.md` and `desktop-bi-runtime.md`.

## Phase 1 — Scope And Mode

Record:

- project identity and product scope;
- candidate baseline mode (`MINIMUM` or `FULL`);
- affected product surfaces and users;
- current Loop method or method candidates;
- known source locations;
- current Calabash lineage, if any;
- initial UI/Workflow monitoring applicability;
- BI presentation and project-open policy.

The mode may change after source preparation. BI must show this as a draft change,
not silently overwrite an earlier accepted baseline.

## Phase 2 — Source Discovery

Collect all likely authoritative and descriptive material before questioning Owner.
Use breadth first, then narrow by relevance.

Do not assume the newest file is the most authoritative. A recently copied old PRD
may be less current than production behavior plus a later Owner decision.

Every material source registration appends a `BI_CHANGE_EVENT` and refreshes the
compact and full views.

## Phase 3 — Source Preparation

Build:

```text
SOURCE_REGISTER
CLAIM_LEDGER
CONTRADICTION_LEDGER
KNOWN_UNKNOWN_LEDGER
```

Normalize duplicate concepts and link every claim to sources. Separate:

- normative: what the product should be;
- descriptive: what the product currently does;
- inferential: what AI concludes from evidence.

Issue `SOURCE_PREPARATION_PASS` only when provenance, freshness, authority,
contradictions, and scope have been checked sufficiently to ask high-value questions.

BI must show source coverage, stale sources, contradictions, and known unknowns while
this phase proceeds.

Read `source-preparation.md`.

## Phase 4 — Dynamic Theme Synthesis

Create `CALABASH_THEME_MAP` from:

- unresolved normative claims;
- contradictions between sources or reality and intent;
- missing product decisions;
- risk and dependency concentration;
- Minimum-to-Full upgrade triggers;
- UI and Workflow change signals.

Themes may cut across Calabash parts. A theme is not required merely because a
reference template contains a heading.

For every theme record:

- current supported claims;
- unresolved decisions;
- related sources and contradictions;
- affected Calabash parts;
- blocking/criticality status;
- required decision dependencies;
- open/answered question IDs;
- living-track relationship.

Every new, merged, split, or retired theme appends a BI change event and refreshes
the compact view.

## Phase 5 — Candidate Question Filtering

Generate candidate questions, then remove or defer questions that are:

- already resolved by authoritative evidence;
- routine technical choices within Loop authority;
- speculative and unsupported;
- materially dependent on an earlier unanswered decision;
- low-impact and outside current baseline scope;
- better answered through observation or experiment.

Rank retained questions by:

1. product authority impact;
2. downstream dependency count;
3. irreversibility and safety risk;
4. contradiction resolution value;
5. ability to unlock other themes.

BI shows only filtered, material questions, not raw brainstorming.

## Phase 6 — Owner Decision Loop

Ask one high-dependency question or a small independent batch.

Each question supplies a recommended answer and choice structure. After every answer:

1. normalize what Owner decided;
2. show the normalized decision briefly;
3. write `OWNER_DECISION_EVENT`;
4. update baseline draft claims;
5. update affected themes and questions;
6. re-run contradiction and dependency analysis;
7. generate follow-up questions if needed;
8. append one `BI_CHANGE_EVENT`;
9. rebuild compact and full BI;
10. verify the new source fingerprint is visible;
11. commit the complete transaction atomically.

Question count is unlimited. The interview ends only when blocking definition claims
are resolved, deferred under explicit authority, or blocked by an Owner-exclusive
unknown.

The compact window must show the decision immediately, including whether it is
`FINAL`, `PROVISIONAL`, `EXPERIMENTAL`, or `DEFERRED` and which UI, Workflow, GO,
Verification, Chain, Level, or Graph artifacts may be affected.

## Phase 7 — Baseline Consistency Audit

Check:

- Grandpa, Product Architecture, and Ontology do not contradict;
- Full layers, when present, trace to Minimum layers;
- every decision has provenance and a current supersession state;
- unanswered blocking questions are visible;
- UI and Workflow living tracks are initialized;
- source and claim status are not overstated;
- Loop traces can be derived without inventing product meaning;
- BI reflects the same state as the repository;
- current definition and latest semantic changes are visible and linked.

## Phase 8 — BI Freshness Audit

Verify:

- `CALABASH_BI_BOOTSTRAP_PASS` is valid;
- visible BI source fingerprint matches current governed source state;
- compact and full views exist and include current baseline/working-draft identity;
- the change feed parses and its latest event is visible;
- project-local launchers exist;
- desktop mode or headless publication is explicit;
- the BI remains read-only;
- stale/error state is not hidden.

A stale, failed, or unavailable required BI surface blocks baseline freeze.

## Phase 9 — Freeze

Create:

```text
PROJECT_CALABASH_BASELINE
CALABASH_BASELINE_FREEZE
```

Record exact files, hashes, source snapshot, decision-ledger head, Git commit, tag,
review policy, BI source fingerprint, change-feed head, snapshot path, and
invalidation rules.

A freeze closes only that version.

## Phase 10 — Continuous Evolution

During implementation and use, collect UI and Workflow signals, new evidence,
incidents, user behavior, and tool/device changes.

Every material observation appears in compact BI immediately as a signal, even
before an amendment is approved. It must be labeled as observed/draft rather than
accepted definition.

Signals enter review and amendment; they never bypass versioning.
