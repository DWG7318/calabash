# Full Calabash Architecture

## Full Structure

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

The final seven items are the governance layers.

| Layer | Purpose | Typical artifacts | Key question |
|---|---|---|---|
| Ontology | canonical domain meaning | glossary, entity/state/relationship map | What exists and how does it relate? |
| Contract | exchange semantics and compatibility | schemas, APIs, events, versions | What must be sent, received, and preserved? |
| Policy | authority, permission, and safety | role/action matrix, access/safety rules | Who may do what, when, and why? |
| Workflow | product state movement | state machine, exceptions, recovery | What is the next valid business state? |
| Action Catalog | allowed product/system actions | action registry, preconditions, side effects | What can the system actually do? |
| Adapter | product/runtime translation | context/action/result mappings | How does meaning enter and return from AI/runtime safely? |
| Eval & Audit | product proof and traceability | evals, evidence packs, logs, audit | How do we know it worked and who did what? |

## Creation And Evolution

Full layers are not produced from a universal checklist. Each layer is populated by
prepared evidence, dynamic themes, Owner decisions, and implementation/operation
reality.

UI Reality can amend Product Architecture, Ontology, Policy, Workflow, Action, and
Eval. Core Workflow Reality can amend Contract, Policy, Workflow, Action, Adapter,
Eval, and possibly Grandpa when feasibility changes product promise.

## Dependencies

- Contract expresses Ontology but does not define it.
- Policy constrains Contracts, Workflows, and Actions.
- Workflow uses Ontology states and Policy-authorized transitions.
- Action Catalog makes Workflow transitions executable.
- Adapter exposes only valid product state and authorized actions to runtime.
- Eval & Audit proves the product and governance claims.

## Boundary

Product Workflow is not a GO sequence, CLK Level matrix, or GLK graph.
Action Catalog is not a Worker shell allowlist.
Adapter is not Planner, Router, Grapher, or runtime itself.
