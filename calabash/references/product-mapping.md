# Product Mapping With Calabash

Start from product reality. Calabash is applied after the product map exists.

## Product-First Map

Use this sequence:

```text
1. Users and roles
2. Entry points
3. Core business journey
4. Back-office modules
5. Agent-native support layer
6. External tools and channels
7. Data, memory, evidence, deployment
8. Calabash governance matrix
```

## Questions

### Users and Roles

- Who uses the product?
- What does each role need to see?
- What is each role allowed to do?
- Which role owns each business decision?

### Entry Points

- Website, app, mini-program, admin console, chat lab, operations page?
- Which entry is for customers?
- Which entry is for staff?
- Which entry is for internal testing or operations?

### Business Journey

Write the real chain in verbs:

```text
acquire -> register -> profile -> collect data -> plan -> approve -> schedule -> execute -> follow up -> settle -> audit
```

Replace these verbs with the domain's actual words.

### Back Office

Every admin page should answer:

- Which workflow state does this page manage?
- Which role uses it?
- Which action can be taken here?
- What downstream state should change?
- What evidence is written?

### Agent Support

Add agent layers only after the above is clear:

- Adapter: product state to thread/turn.
- Runtime: reasoning, memory, tool choice.
- Action catalog: allowed operations.
- External tools: MCP, skills, channels.
- Eval/audit: prove the action and response were acceptable.

## Governance Matrix Template

| Calabash layer | Product artifact | Acceptance evidence |
|---|---|---|
| Ontology | domain glossary, entity map | no duplicate/conflicting terms |
| Contract | schemas, API/event specs | validators pass |
| Policy | role/action matrix | forbidden actions fail |
| Workflow | state machine | transition tests pass |
| Action Catalog | action registry | every action has precondition and audit event |
| Adapter | thread/turn interface | agent can run without bypassing product rules |
| Eval & Audit | tests, logs, screenshots | evidence pack is reproducible |

## Output Rule

When the user asks for a diagram, avoid pure category trees. Show at least one of:

- business state flow
- agent action loop
- data/evidence feedback
- governance constraints
- role-to-entry-to-task relation

If none of those relationships are visible, it is probably not an architecture diagram.
