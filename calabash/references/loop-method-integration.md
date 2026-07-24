# Calabash Integration With SLK, CLK, And GLK

## Shared Order

```text
prepared sources
→ dynamic themes and Owner decisions
→ frozen Full or Minimum Calabash
→ selected Loop method
→ GO traces and Verification Contracts
→ execution and evidence
→ UI/Workflow observations
→ Calabash review/amendment
```

## Summary

| Method | Shape | Calabash use |
|---|---|---|
| SLK | one persistent Worker, coherent serial domain | mandatory for product-affecting work; narrow technical exemption allowed |
| CLK | fixed Chains, ordered concurrent Levels, full barriers | Full or Minimum mandatory |
| GLK | free GO graph, branches, joins, fallback, partial unlock, bounded cycles | Full or Minimum mandatory; node and edge traces required |

`MSLK` is the legacy name for pre-2.0 CLK history.

## SLK

The SLK Supervisor responsibility establishes or adopts the baseline before product
GO planning. The shared Supervisor/Checker conversation does not authorize Checker
to redefine product meaning. Checker validates against frozen traces.

A narrow `CALABASH_EXEMPTION` must prove no user behavior, journey, ontology, policy,
workflow, or product acceptance can change.

SLK may feed UI and Workflow observations back to a Calabash amendment branch. An
active run remains pinned until explicit adoption.

## CLK

Calabash precedes Chain/Level planning.

Every real GO records `GO_CALABASH_TRACE`; every Verification Contract derives from
that trace. Calabash grounds Chain ownership, Level outcomes, cross-Chain contracts,
and final composition.

CLK has no Grapher. It may not use Calabash to justify conditional routing or partial
Level unlock.

A Level barrier is a useful periodic-review trigger.

## GLK

Calabash precedes graph construction.

Every GO node records a GO trace. Every graph edge records `EDGE_AUTHORITY_TRACE`.
Grapher owns graph state and legal routing but cannot amend Calabash, invent product
intent, or turn implementation convenience into edge authority.

Graph checkpoints, convergence, repeated loop-back, and terminal review are useful
Calabash review triggers.

## Change Propagation

An amendment identifies affected GO traces, edge traces, Verification Contracts,
accepted evidence, active Loops, releases, Level barriers, and graph terminal
conditions.

No Loop method may disguise a product-definition change as ordinary rework.
