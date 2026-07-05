# Calabash Architecture Reference

Calabash is a reusable governance architecture for agent-native products. It is not tied to one project, one runtime, or one business domain.

## Placement

Correct placement:

```text
Owner intent / product constitution
        ↓
Product architecture and business journey
        ↓
Calabash governance checks
        ↓
Domain application implementation
        ↓
Agent adapters, runtimes, tools, data, audit
```

Do not place Calabash as a runtime center or a user-facing module.

## The Seven Layers

| Layer | Purpose | Typical artifacts | Key question |
|---|---|---|---|
| Ontology | Define the domain language | entity map, glossary, relationship model | What things exist and how do they relate? |
| Contract | Define data and interface shapes | schemas, API specs, event envelopes | What must each layer send and receive? |
| Policy | Define permissions and boundaries | role matrix, safety rules, access checks | Who can do what, when, and why? |
| Workflow | Define business state movement | state machine, BPMN-like flow, transitions | What is the next valid state? |
| Action Catalog | Define allowed actions | action registry, tool list, preconditions | What can the system actually do? |
| Adapter | Translate between product and agent runtime | thread/turn APIs, orchestration layer | How does product state become agent work? |
| Eval & Audit | Prove quality and traceability | tests, logs, screenshots, audit events | How do we know it worked and stayed safe? |

## Metaphor Roles

These names are optional shorthand, not required implementation classes.

| Name | Meaning |
|---|---|
| Grandpa / 爷爷 | Owner intent, product constitution, value judgment |
| Snake / 蛇精 | Ambiguity, hallucination, overclaim, boundary drift |
| Scorpion / 蝎子精 | Legacy chaos, dirty integration, broken links, engineering debt |

## Mature Architecture Comparisons

Use these as reference frames when explaining Calabash:

- Domain-Driven Design: aligns with Ontology and bounded language.
- Clean Architecture / Hexagonal Architecture: aligns with Adapter and boundary separation.
- BPMN and finite state machines: align with Workflow.
- RBAC/ABAC: align with Policy.
- OpenAPI/JSON Schema/event contracts: align with Contract.
- Tool registries and command buses: align with Action Catalog.
- Observability, audit trails, and evaluation harnesses: align with Eval & Audit.

Calabash is not a replacement for these practices. It is a wrapper that makes them usable for agent-native business systems.

## Architecture Test

A Calabash architecture is healthy when:

1. Product users and business outcomes are clear before agent details.
2. Every major concept has one name and one owner.
3. Every important action has a precondition, permission check, side effect, and audit event.
4. Agents can only act through adapters and action catalogs.
5. Evidence exists for user-visible flows, backend state changes, and runtime decisions.
