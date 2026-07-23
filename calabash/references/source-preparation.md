# Historical Material Preparation And Self-Verification

## Why It Comes First

Owner time should be spent on unresolved product judgment, not reconstructing facts
that the project already contains.

Questioning before source preparation creates duplicate questions, false choices,
memory bias, and a Calabash that ignores its own history.

## Source Classes

Classify each source as one or more of:

- `OWNER_AUTHORITY`: explicit Owner intent or decision;
- `APPROVED_NORMATIVE`: approved product, legal, policy, or business document;
- `OBSERVED_REALITY`: current UI, logs, analytics, production behavior, operations;
- `USER_EVIDENCE`: research, feedback, support, usability, accessibility;
- `ENGINEERING_EVIDENCE`: code, schema, tests, architecture, runtime state;
- `HISTORICAL_DECISION`: prior decision event, ADR, issue, review;
- `EXTERNAL_CONSTRAINT`: regulation, device, tool, vendor, channel constraint;
- `AI_INFERENCE`: derived interpretation that has not become authority.

Engineering evidence describes implementation. It does not automatically define
product intent.

## Source Register

Each source records:

```text
SOURCE_ID
TITLE / LOCATION / HASH
SOURCE_CLASS
CREATED_AT / OBSERVED_AT
AUTHOR / OWNER
AUTHORITY_LEVEL
FRESHNESS_STATUS
SCOPE
CLAIMS_SUPPORTED
CLAIMS_CONTRADICTED
VERIFICATION_METHOD
CONFIDENCE
NOTES
```

## Claim Ledger

Normalize source content into atomic claims.

Each claim records:

- claim text;
- normative/descriptive/inferential type;
- Calabash-part references;
- supporting and contradicting source IDs;
- current status;
- confidence and authority;
- whether Owner decision is required.

## Self-Verification Checks

A source preparation pass checks:

1. **Provenance** — can the source be identified and reproduced?
2. **Authority** — does it describe intent, current reality, or only implementation?
3. **Freshness** — is it current for the claim being made?
4. **Consistency** — do other sources agree?
5. **Observability** — can current behavior be independently observed?
6. **Scope** — does the source actually cover the affected product area?
7. **Inference separation** — are AI conclusions labeled as inference?
8. **Contradiction visibility** — are conflicts preserved rather than silently
   resolved?

## Contradictions

Do not choose a winner silently.

Classify contradiction as:

- stale source;
- different scope;
- implementation drift;
- changed Owner intent;
- unresolved product choice;
- data-quality defect;
- ambiguous terminology.

Resolve from evidence when uniquely supported. Ask Owner only when the remaining
choice is materially product-defining and Owner-exclusive.

## SOURCE_PREPARATION_PASS

Required fields:

```text
scope_covered
source_count
verified_source_count
unverified_source_ids
contradiction_count
blocking_contradiction_ids
known_unknown_ids
claim_coverage_summary
prepared_by
prepared_at
receipt_hash
```

The pass does not claim perfect knowledge. It claims that questioning can now be
focused, sourced, and non-redundant.
