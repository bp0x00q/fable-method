# Proof table — build this before you report

One row per claim. If a row has no failable check, its status is `unverified`, and that must stay visible downstream.

| claim | source | current evidence | status | caveat |
|-------|--------|------------------|--------|--------|
| <what you assert is true / done> | <test / file / git / doc read> | <the actual output, count, or hash> | verified \| unverified \| refuted | <what this does NOT cover> |

Rules:
- "It looks right" is not evidence. The evidence column holds an artifact: a test result, a real count that matches the diff, a path proven to exist, a commit SHA, a source actually read.
- A refuted claim stays in the table with status `refuted` — don't delete the disproof.
