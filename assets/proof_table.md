# Proof table — build this before you report

One row per consequential claim. If a row has no failable check, its status is `unverified`, and that must stay visible downstream.

| claim | source | current evidence | status | caveat |
|---|---|---|---|---|
| `<what you assert is true / done>` | `<test / file / git / log / doc / registry read>` | `<actual output, count, hash, diff, status code, or path>` | `verified` \| `unverified` \| `refuted` | `<what this does not cover>` |

## Rules

- "It looks right" is not evidence. The evidence column holds an artifact: a test result, a real count that matches the diff, a path proven to exist, a commit SHA, a status code, a source actually read, or a runtime/log excerpt.
- A refuted claim stays in the table with status `refuted`. Do not delete the disproof.
- Low-stakes local reasoning can stay out of the table. Claims that affect a diagnosis, shipped behavior, destructive action, dependency choice, or user-facing conclusion cannot.
