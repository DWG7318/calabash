# Calabashi

This repository contains reusable Codex skills for designing, governing, and constructing agent-native product systems.

Included skills:

- `calabashi`: product-first architecture governance for agent-native systems.
- `loop-engineering-for-codex`: supervisor-outside loop engineering for large Codex work.
- `le`: short alias for `loop-engineering-for-codex`.

## Calabashi

Calabashi keeps the product architecture primary:

It keeps the product architecture primary:

```text
roles -> entry points -> business journey -> back-office modules
      -> agent/runtime support -> data/evidence -> deployment
```

Then it applies the Calabash seven-layer governance method:

```text
Ontology / Contract / Policy / Workflow / Action Catalog / Adapter / Eval & Audit
```

Small amount of Chinese terminology is kept for continuity:

- Calabash / 葫芦娃七层架构
- Grandpa / 产品宪法
- Snake / 语义混乱、幻觉、越界
- Scorpion / 遗留债、断链、脏工程

## Loop Engineering For Codex

Loop Engineering For Codex, short name **LE**, is a reusable Codex skill for running large projects through stable supervisor-outside execution loops.

It is designed for multi-module, multi-thread, or long-running Codex work where ordinary chat-style coordination becomes fragile.

Core idea:

```text
supervisor outside the loop
        ↓
planner / composite checker assigns fixed go-cell work
        ↓
worker executes one bounded cell
        ↓
checker verifies evidence
        ↓
router decides continue, rework, complete, block, or plan defect
```

LE provides:

- Supervisor-outside loop architecture.
- Small-loop and large-loop role models.
- Planner, worker, checker, and router boundaries.
- Go/cell planning format.
- Worker method logs.
- Final checker markdown queue.
- Direct thread receipt protocol using `完成，请检验`.
- No active waiting, no supervisor relay, and no hidden middle-loop chatter.
- Line-limit and artifact-sharding rules for long planning files.

## Install

Copy the desired skill folder into your Codex skills directory, or install from this repository with your preferred skill installer.

Canonical entry points:

```text
calabashi/SKILL.md
loop-engineering-for-codex/SKILL.md
le/SKILL.md
```

## Use

Example prompts:

```text
Use $calabashi to turn this agent product idea into a product-first architecture,
Calabash governance matrix, and micro-loop construction plan.

Use $le to plan this project as supervisor-outside loop engineering.
Create the solution file, goal map, cell plan, checker/worker responsibilities,
final queue rules, and validation gates before launching work.
```

## License

MIT.
