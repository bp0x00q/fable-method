---
name: fable-method
description: >-
  A working method for consequential coding tasks where a plausible-but-wrong
  result is costly: large refactors, debugging failures whose obvious cause may
  be a red herring, data pipelines or extraction logic, automation that mutates
  real state, concurrency/shared-state bugs, and multi-step work whose output is
  hard to eyeball for correctness. Diagnose before building, ship the smallest
  verified slice, and make no consequential "done" or "this is the cause" claim
  without a check that could fail: a test that runs, logs/git history/on-disk
  state actually read, or an external entity actually resolved. Skip it for
  trivial single-pass edits with one obvious correct answer.
---

# The Fable Method

A working method for consequential coding tasks: diagnose before you build, ship the smallest verified slice, and make no consequential claim without a check that can fail.

> **The creed.** No consequential claim without a receipt. No policy value left to a silent default. No source, model, package, or self-report trusted without a gate. Reach for the eraser before the pen; install the meter before the engine.

## The one move under all of it: a check that can fail

"I reviewed it and it looks right" is not a check — a model that would skip verification will also pass its own introspection. If a claim affects a diagnosis, shipped behavior, dependency choice, destructive action, or user-facing conclusion, it must clear a gate that an external artifact satisfies: a test that runs, a file proven to exist in the expected shape, git history that confirms it, logs actually read, or a source/entity actually resolved.

Build a **proof table** before reporting (`assets/proof_table.md`). If a consequential step has no failable check, mark it **unverified** so the gap stays visible downstream.

**The rule for every gap: where you would use intuition, use an instrument.**

## The loop

1. **Diagnose before you build.** Trace symptoms to one root cause where possible. Write a keep-sacred list (what must survive) and a what-rotted list (dead code, named file-by-file with a verified reason). Check every "exists now" claim against disk/git/runtime output, never memory.
2. **Ship the smallest coherent slice.** Each slice should compile, pass its relevant checks, and stand alone. Land tests/checks with the feature. Prove it on representative real or fixture data and record the receipt where review can find it: test output, CI artifact, PR body, commit message, checked-in fixture, golden file, or another durable artifact.
3. **Verify against ground truth.** Repo, tests, logs, runtime output, package registries, and docs beat memory. Confirm named external entities — model IDs, package versions, endpoints, CLI flags — before depending on them. If one does not resolve, stop unless an explicit fallback policy already exists; show the disproof and never silently substitute the nearest plausible match.
4. **Mine self-skeptically before delivery.** Run an adversarial pass over your own output. Kill duplicates, speculative scaffolding, and proposals that require capabilities you do not have. For external factual claims, research findings, or non-obvious recommendations, require at least two independent sources and state the count. For repo-local claims, prefer the authoritative artifact: code, tests, logs, git, filesystem, registry, or runtime output. Name at least one surviving weakness or caveat.

If a fix invalidates an earlier check, re-run that check. The loop goes forward and backward.

## Pick the play for the task

Read the spine above on every run. Then load the **one** play matching the task — only that file enters context.

| If the task is… | Load | Decisive move |
|---|---|---|
| Debugging a failure, especially with an "obvious" recent cause | `references/debugging.md` | Prove the mechanism; do not scapegoat the newest change |
| A refactor whose output/behavior must be preserved | `references/refactor.md` | Capture a golden baseline first, then subtract |
| Extraction / parsing / scraping into structured output | `references/extraction.md` | Typed honest-zero + explicit abstain + strict validator |
| Automation that mutates real state | `references/automation.md` | Shadow-first, reversible, exempt human content |
| Research / synthesis / proposing what to build | `references/research.md` | Verify entities; use independent sources where appropriate; kill weak ideas |
| Concurrency / shared-state bug, or code that will run under threads/async | `references/concurrency.md` | Reproduce under contention; assert an invariant |

## Always-on principles

- **Reach for the eraser first.** The best change is often less. Delete dead machinery in the same cutover commit when it is proven safe by importer/call-site checks, not by "looks unused." State the net line delta; a net-negative diff is often a success signal.
- **Encode invariants in code, not prose.** Classify each config value: POLICY (a threshold, limit, or rule a human owns) vs PLUMBING (a URL, buffer, path, or adapter detail). POLICY never gets `?? default`; validate it and throw a multi-line WHAT / WHY / HOW error. Emit a named event when a limit is hit; never silent-truncate.
- **Make the empty result first-class.** Model outcomes as typed statuses with a named honest-zero and a named invalid state. Never collapse `empty`, `skipped`, `invalid`, and `success` into one boolean. A skip is not a pass.
- **Gate destructive actions.** Any deletion, overwrite, migration, or external mutation goes shadow-first and reversible, and exempts human-authored content by default. When the task is mutating automation, load `references/automation.md` for the full gate checklist.
- **Work economically.** Patch rather than rewrite. Batch mechanically related low-risk edits, but verify at each semantic boundary. Cut narrated preamble/postamble. Economy means avoiding wasted motion, not rationing rigor.

## Done means

- The smallest coherent slice is implemented.
- Relevant checks ran and their receipts exist.
- The proof table supports every consequential claim or marks it unverified/refuted.
- Known caveats are named.
- No broader completion is implied than the evidence supports.

## When NOT to use this

If a task has one obvious correct approach and fits in a single pass, do it directly and skip the loop — staging trivia buries the answer under ceremony. When a task is genuinely beyond the available instruments, say which claim cannot be verified rather than producing plausible-sounding certainty.

## Provenance

Distilled from close observation of a capable coding agent over an extended run, then re-grounded by falsifiable tests: debugging, refactor, and extraction under real git/logs/disk; automation core behavior (shadow-first / exempt-human / reversible) under real filesystem state; research entity-resolution under real package-registry queries; and concurrency under real threads with an invariant stress harness. See each play's worked receipt.

What remains untested here is lower-stakes residue: the automation play's POLICY-throw and telemetry-on-limit claims, plus the research play's independent-source and adversarial-self-pass claims. Treat those as map, not proof, until you ground them in your own work.
