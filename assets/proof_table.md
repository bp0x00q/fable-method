# Proof table

Create one row per consequential claim before reporting.

| id | claim | source | current evidence | status | caveat |
|---|---|---|---|---|---|
| `P-01` | `<assertion>` | `<test / diff / file / git / log / registry / source>` | `<actual output, count, hash, path, status, or excerpt>` | `verified` \| `unverified` \| `refuted` | `<what this does not establish>` |

Rules:

- “Looks right” and self-review are not evidence.
- Keep refuted rows; do not erase disproof.
- Learning candidates may cite only `verified` rows.
- Low-stakes local reasoning may stay out. Diagnosis, shipped behavior, destructive actions, dependencies, and user-facing conclusions may not.
