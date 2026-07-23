# Calabash Git Governance

## Why Git Is Mandatory

Calabash decisions change product meaning. They require the same reproducibility,
authority, review, and rollback visibility as source code.

## Recommended Project Tree

```text
.calabash/
  baseline/
    manifest.json
    grandpa.md
    product-architecture.md
    ontology.json
    full/
  sources/
    register.json
    claims.jsonl
    contradictions.json
  themes/
    map.json
  questions/
    Q-*.json
  decisions/
    ledger.jsonl
  observations/
    ui/
    workflow/
  reviews/
  traces/
    go/
    edge/
  bi/
    config.json
    bootstrap.json
    change-feed.jsonl
    summary.json
    dashboard.html
    compact.html
    launch-calabash-bi.sh
    launch-calabash-bi.cmd
    runtime/
```

`bi/runtime/` is mutable local process state and should be ignored by Git.

## Branches

Recommended names:

```text
calabash/create/<baseline-id>
calabash/amend/<next-version>/<theme>
calabash/review/<yyyy-mm-dd>
```

`main` contains accepted lineage. Working branches contain durable drafts.

## Atomic Definition Commit

Every Owner answer or material Calabash change produces one atomic commit containing:

- authoritative artifact changes;
- question/decision/theme/signal/review/amendment state as applicable;
- impact and trace invalidation;
- one append-only `BI_CHANGE_EVENT`;
- refreshed `bi/summary.json` and `bi/dashboard.html` when generated assets are
  committed;
- successful BI doctor and project validation.

Suggested commits:

```text
calabash(decision): Q-014 approve doctor-only final review
calabash(ui): record onboarding-label drift
calabash(workflow): add manual fallback experiment
calabash(amend): adopt ontology split in v1.4.0
calabash(bi): bootstrap desktop definition window
```

When a remote is available, push the commit before the next session boundary. A
local unpushed answer is not durable cross-session history.

## Change Feed And Git

The change feed is semantic, while Git is structural.

Every change event records its Git commit when known. During the same atomic commit,
the event may temporarily use `null`; the next deterministic finalization step may
fill the commit without changing product meaning.

Do not replace the change feed with commit titles. Do not replace Git history with
the change feed.

## Commit Classes

```text
calabash(source): ...
calabash(theme): ...
calabash(question): ...
calabash(decision): ...
calabash(ui): ...
calabash(workflow): ...
calabash(review): ...
calabash(amend): ...
calabash(freeze): ...
calabash(bi): ...
```

## Tags

Tag every frozen project baseline independently from the Calabash method version:

```text
calabash/<baseline-id>/v1.0.0
```

The method may be Calabash 2.2.0 while a project baseline is v3.4.1.

## Baseline Semantic Versioning

Recommended:

- patch: clarification without material behavior/authority change;
- minor: compatible additive product definition or monitored UI/workflow amendment;
- major: Grandpa, core product outcome, incompatible Ontology, role authority, or
  major workflow change.

## Append-Only History

Never:

- force-push accepted decision history;
- rebase or squash away accepted Owner decision commits;
- delete superseded questions, decisions, or change events;
- edit old baseline tags;
- move evidence to a newer version without invalidation analysis;
- regenerate BI to hide a prior provisional or failed definition state.

Corrections create superseding records.

## Generated Assets

Default policy commits `summary.json` and `dashboard.html` because they make the
current projected state reviewable on GitHub and across sessions.

They remain generated, not authoritative. A project may set:

```text
commit_generated_assets: false
```

only when CI or an equivalent reproducible process always builds them and cross-
session visibility is otherwise preserved.

## Active Loop Pinning

Every SLK, CLK, or GLK run records:

```text
CALABASH_BASELINE_ID
CALABASH_BASELINE_VERSION
CALABASH_BASELINE_HASH
CALABASH_GIT_COMMIT
CALABASH_BI_STATE_HASH
```

A new Calabash version requires explicit impact analysis and adoption. It does not
silently alter active work.


## BI Derived-State Policy

`bi/config.json` and `bi/bootstrap.json` are durable governance records. The live summary, HTML views, and runtime heartbeat are reproducible derived
state. The append-only change feed is a durable semantic ledger, not disposable
presentation output. Continuous refresh must not create Git noise or alter authoritative product
definition.

At each baseline freeze, formal review, or release handoff, build and retain one BI
snapshot tied to the exact Calabash Git commit. Runtime heartbeat files remain
untracked.

A project opening checklist must launch the persistent BI according to the recorded
startup policy. A project-closing checklist must record the final refresh state and
stop the desktop process cleanly.
