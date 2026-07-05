# Calabashi

Calabashi is a reusable Codex skill for designing and governing agent-native product systems.

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

## Install

Copy the `calabashi/` folder into your Codex skills directory, or install from this repository with your preferred skill installer.

The skill entry point is:

```text
calabashi/SKILL.md
```

## Use

Example prompt:

```text
Use $calabashi to turn this agent product idea into a product-first architecture,
Calabash governance matrix, and micro-loop construction plan.
```

## License

MIT.
