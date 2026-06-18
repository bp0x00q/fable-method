# Fable Method — verified-learning edition

A working method for **consequential coding**, where a plausible-but-wrong result is costly: ambiguous debugging, behavior-preserving refactors, extraction pipelines, mutating automation, concurrency, external dependencies, or multi-step work that's hard to verify by inspection.

> **Core rule.** No consequential claim without a receipt — a test, diff, log, runtime result, filesystem fact, git history, or source actually read. Where intuition would carry the decision, install an instrument.

Fable is an **execution method first**:

```text
contract → diagnose → slice → verify → critique
```

A verified, non-obvious, reusable discovery may then enter an **optional, gated** retention path — never every-prompt extraction, never a direct write into a live skill library:

```text
proof-table receipt → search/dedupe → staged candidate
→ positive/negative/boundary evaluation → promotion → revalidation or retirement
```

This keeps the useful continuous-learning features — selective extraction, trigger-focused descriptions, update-vs-create decisions, project/user scope, versioning, cross-links, deprecation, and archival — while rejecting every-prompt extraction pressure and direct session-to-live-memory writes.

## Structure

- **[`SKILL.md`](./SKILL.md)** — the spine: the core rule, the loop, the play table, and the always-on invariants. Read it every run.
- **[`references/`](./references)** — load only what the task needs:
  - **execution plays** — [`debugging`](./references/debugging.md), [`refactor`](./references/refactor.md), [`extraction`](./references/extraction.md), [`automation`](./references/automation.md), [`research`](./references/research.md), [`concurrency`](./references/concurrency.md)
  - [`learning.md`](./references/learning.md) — the gated retention lifecycle
  - [`receipts.md`](./references/receipts.md) — the plays' reproduced worked examples
- **[`assets/`](./assets)** — runnable templates: [`proof_table.md`](./assets/proof_table.md), [`status_enum.py`](./assets/status_enum.py), [`skill_candidate_template.md`](./assets/skill_candidate_template.md).
- **[`BUILD_RECEIPT.md`](./BUILD_RECEIPT.md)** — this bundle's own proof table; **[`CHANGELOG.md`](./CHANGELOG.md)** — edition history.

## Proven vs. candidate

Obeying its own creed: the execution plays carry receipts reproduced under real git, logs, disk, and threads (see `BUILD_RECEIPT.md`). The **learning lifecycle is a candidate method** — its one empirical claim, that retained skills improve future-agent performance, is **unverified** until benchmarked in your target environment. Keep candidates staged until they pass a clean with/without-skill evaluation.

## Use it

`SKILL.md` uses the standard `name` + `description` frontmatter, so skills-based agents can register it. Copy the directory so the plays and assets resolve:

```bash
cp -r fable-method <your-agent-skills-dir>/
```

Or read `SKILL.md` and pull plays as needed. It's a checklist, not a transplant — on a strong model it reinforces good habits; it cannot raise the reasoning ceiling.

## License

MIT — see [`LICENSE`](./LICENSE).
