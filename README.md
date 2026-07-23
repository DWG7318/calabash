# Calabash

Calabash is a product-definition and governance method for AI-assisted and
agent-native software.

Version **2.2.0** makes Calabash BI a mandatory project operating surface rather
than a report generated near the end of definition work.

```text
project initiation
        ↓
Calabash BI bootstrap
(compact desktop window + full dashboard)
        ↓
verified historical material
        ↓
dynamic theme map
        ↓
Owner decision interview
(single-choice / multi-choice + AI recommendation)
        ↓
immediate write-through to Calabash, Git, and BI change feed
        ↓
frozen versioned baseline
        ↓
SLK / CLK / GLK execution
        ↓
UI and core-workflow observations
        ↓
continuous desktop visibility, periodic review, and amendment
```

Minimum Calabash remains:

```text
Grandpa → Product Architecture → Ontology
```

Full Calabash remains:

```text
Grandpa → Product Architecture → Ontology → Contract → Policy
→ Workflow → Action Catalog → Adapter → Eval & Audit
```

A Calabash version is immutable after freeze. Calabash as a lineage remains open
and evolves through append-only, Git-governed amendments.

Calabash BI has two required presentation surfaces:

- a lightweight, continuously refreshable desktop window that shows current
  product definition and the latest changes;
- a full dashboard for evidence, history, questions, drift, traces, reviews, and
  version comparison.

Primary skill entry point:

```text
calabash/SKILL.md
```

## BI quick start

Create the BI in the same transaction that establishes the project's `.calabash/`
tree:

```bash
python calabash/scripts/bootstrap_calabash_bi.py \
  --project /path/to/project \
  --project-name "Project Name"
```

Open the lightweight persistent definition window:

```bash
python calabash/scripts/run_calabash_bi_desktop.py \
  --project /path/to/project
```

Validate a desktop-restricted or CI environment without opening a window:

```bash
python calabash/scripts/run_calabash_bi_desktop.py \
  --project /path/to/project \
  --headless-once
```

The compact window is intentionally read-only. It displays the current accepted
product definition, latest semantic changes, non-authoritative working state,
attention items, and freshness. The full dashboard remains one click away.
