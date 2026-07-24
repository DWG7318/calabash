# Owner Decision Interview

## Purpose

The interview supplies authoritative product judgments that verified historical
material cannot settle.

It is adaptive, theme-based, and unlimited in length. It is not a standard
questionnaire.

## Question Eligibility

Ask Owner only when the decision:

- materially affects Grandpa, Product Architecture, Ontology, or required Full
  governance;
- cannot be uniquely resolved from authoritative sources;
- is not a routine engineering choice;
- has enough prepared evidence to present meaningful options;
- is ready in dependency order.

## Question Card

Each `OWNER_DECISION_QUESTION` contains:

```text
QUESTION_ID
QUESTION_VERSION
THEME_ID
RELATED_CALABASH_PARTS
DECISION_CLAIM
WHY_NOW
EVIDENCE_SUMMARY
SOURCE_REFERENCES
CONTRADICTIONS
CHOICE_MODE: SINGLE | MULTI
OPTIONS
RECOMMENDED_OPTION_IDS
RECOMMENDATION_RATIONALE
RECOMMENDATION_CONFIDENCE
TRADE_OFFS
AFFECTED_ARTIFACTS
AFFECTED_UI / WORKFLOW / GO / EDGE
FOLLOW_UP_RULES
```

### Single choice

Use only when one mutually exclusive answer must become authoritative.

### Multiple choice

Use only when several independently compatible answers may all be selected.

### Other answer

Include `OTHER_WITH_TEXT` when Owner may need to express intent not covered by the
prepared options.

## AI Recommendation

AI must recommend an answer using the prepared evidence.

The recommendation must show:

- selected option(s);
- evidence and reasoning;
- confidence;
- benefits and costs;
- what would make the recommendation change.

When evidence is too weak, recommend:

```text
DEFER_AND_COLLECT_EVIDENCE
```

Do not hide uncertainty behind a confident recommendation.

## Avoid Leading Questions

Options should represent materially plausible choices, not one desirable answer and
several caricatures.

For single-choice questions, options should be mutually exclusive enough to produce
one authoritative claim. For multi-choice questions, each option should be independently
interpretable.

## Adaptive Follow-Up

Every answer may:

- resolve the theme;
- expose a contradiction;
- create a subtheme;
- require an Ontology distinction;
- trigger Full-layer upgrade;
- change UI/Workflow monitoring;
- invalidate a later question;
- generate one or more new questions.

Recompute the question queue after each answer.


## Provisional And Prototype Answers

An Owner answer may define a prototype rather than a permanent product truth,
especially for UI and core Workflow decisions whose real effect must be observed.

Record:

```text
DECISION_STATUS: FINAL | PROVISIONAL | EXPERIMENTAL | DEFERRED
EVIDENCE_REQUIRED
REVIEW_TRIGGER
VALID_UNTIL
```

A provisional answer is still written and committed immediately. It does not become
permanent merely because implementation begins. Critical safety, authority, or
non-negotiable Grandpa claims may not be hidden behind an unbounded provisional
status.

## Write-Through Decision

After Owner answers, create `OWNER_DECISION_EVENT`:

```text
DECISION_ID
QUESTION_ID / VERSION
OWNER_ANSWER
NORMALIZED_CLAIM
SELECTED_OPTION_IDS
OWNER_TEXT
AI_RECOMMENDATION
RECOMMENDATION_ACCEPTED: true | false | partial
AFFECTED_CALABASH_PATHS
SUPERSEDES
TIMESTAMP
GIT_COMMIT
DECISION_STATUS
EVIDENCE_REQUIRED
REVIEW_TRIGGER
VALID_UNTIL
```

Update the working Calabash, append one `BI_CHANGE_EVENT`, rebuild the compact/full BI, verify freshness, and commit in the same decision cycle.

## Correction

If Owner corrects or revises an answer, create a new event with `SUPERSEDES`.
Never edit the earlier event or pretend the later answer was always the original.
