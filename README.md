# The Fable Method

A working method for **consequential coding tasks** — where a plausible-but-wrong result is costly: large refactors, debugging a failure whose obvious cause is a red herring, building extraction/parsing logic, shipping automation that mutates real state. Reverse-engineered from how a capable coding agent actually worked — *how* it worked, not a transcript of *what* it built.

> **The creed.** No claim without a receipt. No policy value left to a silent default. No source, model, or self-report trusted without a gate. Reach for the eraser before the pen; install the meter before the engine.

## Structure

- **[`SKILL.md`](./SKILL.md)** — the spine: the creed, the one move (a check that can fail), the loop (diagnose → slice → verify → critique), the always-on principles, and when *not* to use it. Read this every run.
- **[`references/`](./references)** — six task-specific plays, each with a worked receipt. Load only the one matching your task:
  - [`debugging.md`](./references/debugging.md) — prove the mechanism; don't scapegoat the newest change
  - [`refactor.md`](./references/refactor.md) — golden baseline first, then subtract
  - [`extraction.md`](./references/extraction.md) — typed honest-zero + abstain + strict validator
  - [`automation.md`](./references/automation.md) — shadow-first, reversible, exempt human content
  - [`research.md`](./references/research.md) — verify entities; independent sources where appropriate; kill weak ideas
  - [`concurrency.md`](./references/concurrency.md) — reproduce under contention; assert an invariant
- **[`assets/`](./assets)** — runnable templates: [`proof_table.md`](./assets/proof_table.md) (the claim/evidence/status table to build before reporting) and [`status_enum.py`](./assets/status_enum.py) (an honest-zero extraction scaffold).

Progressive disclosure by design: read the spine, then pull only the one play your task needs into context.

## Honesty about its own receipts

Obeying its own creed: the **debugging, refactor, and extraction** plays each carry a worked example **reproduced under real git/logs/disk**; **automation** (shadow-first / exempt-human / reversible) was reproduced under real filesystem state, **research** entity-resolution under real package-registry queries, and **concurrency** under real threads with an invariant stress harness. What remains untested is lower-stakes residue — the automation play's POLICY-throw and telemetry-on-limit claims, plus the research play's independent-source and adversarial-self-pass claims — **treat those as map, not proof** until you ground them in your own work.

## Use it

`SKILL.md` follows the common skill convention (`name` + `description` frontmatter), so skills-based agents can register it as-is. Copy the whole directory so the plays and assets resolve:

```bash
cp -r fable-method <your-agent-skills-dir>/
```

Or just read `SKILL.md` and pull plays as needed. It's a checklist, not a transplant — on a strong model it reinforces good habits; it cannot raise the reasoning ceiling.

## License

MIT — see [`LICENSE`](./LICENSE).
