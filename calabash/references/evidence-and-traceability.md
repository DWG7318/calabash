# Calabash Evidence And Traceability

## Authority Chain

```text
source evidence
→ theme
→ Owner decision / supported claim
→ baseline clause
→ GO_CALABASH_TRACE
→ GO_VERIFICATION_CONTRACT
→ evidence and verdict
```

GLK additionally uses `EDGE_AUTHORITY_TRACE`.

## Baseline Identity

Every baseline records ID, mode, version, content hash, Git commit/tag, source
snapshot, decision-ledger head, known gaps, review policy, living tracks, and
superseded baseline.

## GO Trace

Every product-facing GO records:

```text
GO_ID / GO_VERSION
BASELINE_ID / VERSION / HASH / COMMIT
GRANDPA_REFERENCES
PRODUCT_ARCHITECTURE_REFERENCES
ONTOLOGY_REFERENCES
FULL_LAYER_REFERENCES
DERIVED_OUTCOME_CLAIM
VERIFICATION_IMPLICATIONS
INVALIDATION_RULE
```

## GLK Edge Trace

Every GLK edge records source/target GO, edge type, Calabash references, verified
runtime-fact references, required verdict/output, predicate, evidence source, and
invalidation rule.

## Verification Derivation

A criterion is valid only when it cites:

1. a baseline clause;
2. a GO claim derived from the clause;
3. an observable fact;
4. required evidence;
5. pass/fail or counter-evidence.

Verification applies the contract; it does not define product success.

## Decision Trace

Every baseline clause affected by Owner questioning should link to its current
`OWNER_DECISION_EVENT`. Superseded events remain visible.

## Invalidation

Material changes to Grandpa, Product Architecture, Ontology, Full layers, UI/workflow
reality, GO outcome, graph predicates, artifact, or environment may stale traces and
verdicts.

Record impact; do not rewrite history.

## Failure Classification

```text
IMPLEMENTATION_DEFECT
GO_CONTRACT_DEFECT
CALABASH_TRACE_INVALID
CALABASH_DEFINITION_BLOCKED
CALABASH_UPGRADE_REQUIRED
VERIFICATION_EVIDENCE_GAP
PRODUCT_EFFECT_GAP
UI_REALITY_DRIFT
WORKFLOW_REALITY_DRIFT
```

Engineering success with wrong product effect returns to Calabash rather than
unbounded code modification.
