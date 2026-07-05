---
name: calabashi
description: Use when designing, restructuring, or governing agent-native product systems; when a user mentions Calabash, ontology, contracts, policy, workflow, action catalogs, adapters, eval/audit, product architecture, or construction loops; or when Agent/LLM/MCP work is drifting away from real product roles, business flows, data, and acceptance evidence.
---

# Calabashi

## Overview

Calabashi is a product-first governance method for agent-native systems. It keeps the product architecture primary, then uses the Calabash seven layers to define concepts, contracts, permissions, workflows, actions, adapters, and evidence.

Core rule: **Calabash is not a feature module, not a runtime hub, and not the product story.** It is the design and construction discipline around the product.

## Quick Workflow

1. Start with the product, not the agent.
   - Who uses it?
   - Through which entry points?
   - What business journey must actually work?
   - Which admin/ops surfaces support it?
   - What data and evidence prove it worked?

2. State the product constitution.
   - Owner intent / Grandpa / 产品宪法
   - Business goals, boundaries, success criteria, release constraints, and value judgments.

3. Draw the real product architecture.
   - Users and roles
   - Product entry points
   - Core business journey
   - Back-office modules
   - Agent/runtime support
   - External tools and channels
   - Data, memory, logs, audit, tests, deployment

4. Apply the seven Calabash layers as governance checks.
   - Ontology: shared domain concepts and relationships
   - Contract: schemas, APIs, and event shapes
   - Policy: role permissions and safety boundaries
   - Workflow: state transitions and business process
   - Action Catalog: allowed actions and tool calls
   - Adapter: translation between product state and agent runtime
   - Eval & Audit: acceptance tests, evidence, logs, and review

5. Place agents in the correct layer.
   - LCagent/LLM runtime is support infrastructure.
   - MCP, tools, skills, and channels are external capabilities.
   - The user-facing product remains roles, entries, workflows, and outcomes.

6. Build through small construction loops.
   - Supervisor defines one micro-scope.
   - Worker implements it.
   - Checker verifies against explicit QC.
   - Router decides REDO, NEXT, COMPLETE, or STOP.
   - After repeated failure, stop and escalate scope/model/approach.

Read `references/product-mapping.md` when converting a product idea into architecture. Read `references/architecture.md` for the full Calabash layer definitions. Read `references/construction-loop.md` when planning or executing loops.

## Decision Rules

| Situation | Do this |
|---|---|
| User asks for "architecture" | Produce product architecture first; show Calabash only as governance. |
| User asks "what is Calabash?" | Explain it as reusable architecture method, not a product module. |
| Agent work feels clever but product feels unclear | Rebuild roles -> entries -> business journey -> data/evidence before touching runtime. |
| Backend/admin feels messy | Reorder by the main business chain, then map pages/actions to workflow states. |
| Mobile/app roles feel generic | Derive each role screen from actual permissions, tasks, data, and next actions. |
| Tool/MCP integration is tempting | Add it only after contract, policy, action catalog, and audit path are defined. |

## Required Outputs

For substantial work, produce these artifacts before implementation:

1. Product architecture map: roles, entries, business journey, modules, data, external capabilities.
2. Calabash governance matrix: seven layers mapped to concrete artifacts.
3. Main workflow state machine: state, trigger, allowed action, actor, result, evidence.
4. Action catalog: action name, actor, precondition, tool/API, side effect, audit event.
5. Acceptance plan: checks, pass/fail criteria, screenshots/logs/events required.
6. Construction loop plan: micro-loops with scope, worker output, checker criteria, router rule.

## Common Mistakes

- Do not draw Calabash as the center of the system.
- Do not let Agent, LLM, MCP, or tools become the product narrative.
- Do not call a list of modules an architecture; show causal flow and feedback loops.
- Do not add actions before contracts and policies exist.
- Do not claim completion without evidence: state changes, logs, screenshots, tests, or audit records.
- Do not build huge loops. Smaller loops fail cheaper and recover faster.

## Compact Diagram Pattern

Use this logic when sketching:

```text
Owner Intent / 产品宪法
        ↓
Product Architecture
roles → entry points → business journey → back-office modules
        ↓
Agent-Native Support
adapter → runtime → actions/tools/channels
        ↓
Data & Evidence
database → memory → events → audit → tests → deployment

Calabash governs every row:
Ontology / Contract / Policy / Workflow / Action Catalog / Adapter / Eval & Audit
```
