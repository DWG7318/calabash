# Continuous Calabash Evolution

## Open Lineage, Frozen Versions

Calabash must remain adaptable without becoming ambiguous.

- frozen baseline versions are immutable;
- observations and new decisions accumulate append-only;
- amendments create a new baseline version;
- active Loop work stays pinned until explicit adoption;
- old evidence remains attributable to the version it proved.


## Prototype-To-Reality Cycle

Question-and-answer decisions may begin as prototypes. UI and Workflow prototypes
must declare the evidence that will confirm, revise, or retire them. BI keeps them
visible until the review trigger is satisfied. A frozen baseline may contain an
explicitly provisional non-blocking claim, but never an invisible or unbounded one.

## UI Reality Track

UI is not merely a visual implementation of prior logic. Real users can reveal that
roles, concepts, journeys, action meaning, or success criteria were wrong or
incomplete.

Monitor:

- navigation and completion behavior;
- misunderstood labels and concepts;
- role-specific information needs;
- abandonment, repetition, workaround, and support patterns;
- accessibility and device constraints;
- mismatch between displayed state and actual product state;
- differences between intended and observed user journeys.

Record each material finding as `UI_CHANGE_SIGNAL` with evidence, severity, affected
themes and Calabash parts, and suggested next action. Append a `BI_CHANGE_EVENT` and
show the signal immediately in compact BI as observation, not accepted definition.

Possible impacts include:

- Product Architecture surface or journey amendment;
- Ontology rename, split, or state distinction;
- Policy visibility or confirmation change;
- Workflow change;
- Action Catalog or Eval amendment.

## Core Workflow Reality Track

Core Workflow is affected by operational reality, not only product logic.

Monitor:

- actual state transitions and exception paths;
- manual steps and human handoffs;
- device capability and availability;
- tool/vendor maturity, latency, accuracy, and failure modes;
- automation boundaries and fallback methods;
- repeated repair or workaround behavior;
- differences between designed and executable workflow.

Record each material finding as `WORKFLOW_CHANGE_SIGNAL`. Append a `BI_CHANGE_EVENT`
and show it immediately in compact BI as observation, not accepted definition.

Possible impacts include Contract, Policy, Workflow, Action Catalog, Adapter, Eval,
Product Architecture, and even Grandpa when the product promise becomes infeasible.

## Signal Lifecycle

```text
OBSERVED
→ TRIAGED
→ EVIDENCE_REQUIRED | DISMISSED | AMENDMENT_CANDIDATE
→ OWNER_DECISION_REQUIRED (when product-authority change)
→ AMENDED | ACCEPTED_AS_RISK
```

A signal is evidence, not authority. It cannot modify a frozen baseline directly.

## Impact Analysis

Before amendment, identify:

- affected themes and baseline clauses;
- affected GO and Verification traces;
- affected CLK Level barriers or GLK graph edges;
- accepted evidence that remains valid;
- UI/workflow artifacts requiring re-observation;
- active Loop runs requiring replan or re-verification;
- release and handoff impact.

## Permanent Monitoring

UI and Workflow can be current and supported, but never permanently complete.
The BI dashboard shows them as living tracks with current signal load, freshness,
and next review, not as ordinary unfinished sections.
