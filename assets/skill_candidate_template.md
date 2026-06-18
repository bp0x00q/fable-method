---
name: descriptive-kebab-case
description: >-
  State the exact problem, observable triggers or error text, relevant technology
  and context markers, what the skill helps accomplish, and one important
  non-trigger. Avoid vague phrases such as “helps with database issues.”
---

# Human-readable title

| lifecycle field | value |
|---|---|
| status | `candidate` |
| scope | `project` \| `user` |
| version | `0.1.0` |
| created | `YYYY-MM-DD` |
| last validated | `YYYY-MM-DD` or `not yet` |

## Trigger

Use when all required conditions hold:

- `<exact error, symptom, file, command, framework, or environment marker>`
- `<second discriminator that prevents false activation>`

Do not use when:

- `<near-miss or counterexample>`

## Problem and mechanism

Describe the recurring problem and the verified mechanism. Separate mechanism from symptom and avoid claiming broader causality than the receipt supports.

## Procedure

Give the smallest actionable sequence. Prefer commands, symbols, paths, checks, and decision points over narrative.

## Verification

State the check that can fail, expected result, and negative case the procedure must reject.

## Observed receipt

- Source task/environment: `<repo, fixture, session, or issue>`
- Proof-table rows: `<P-01, P-02>`
- Evidence: `<test output, diff, log, hash, registry result, or artifact>`
- Result: `<what passed or failed>`

## Boundaries

- What this receipt does not establish
- Versions or environments not tested
- Known variants and failure modes

## Evaluation

| case | without candidate | with candidate | pass criterion | result |
|---|---|---|---|---|
| positive trigger | `<outcome>` | `<outcome>` | `<criterion>` | `<pass/fail>` |
| near-miss negative | `<outcome>` | `<outcome>` | candidate must not misfire | `<pass/fail>` |
| boundary / variant | `<outcome>` | `<outcome>` | `<criterion>` | `<pass/fail>` |

## Lifecycle

- Revalidate when: `<dependency major version, API change, architecture change, date, or failed application>`
- Replaces: `<skill or none>`
- See also: `<related skills or none>`
- Promotion decision: `candidate | active | deprecated | archived`
