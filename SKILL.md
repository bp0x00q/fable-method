---
name: fable-method
description: A working method for consequential coding tasks where a plausible-but-wrong result is costly: large refactors, debugging a failure whose obvious cause may be a red herring, building data pipelines or extraction logic, and shipping automation that mutates real state. Diagnose the root cause before building, ship the smallest slice that compiles and is verified on real data, and make no "done" or "this is the cause" claim without a check that could fail — a test that runs, or logs/git history/on-disk state actually read. Reach for this whenever a task is multi-step or its output is hard to eyeball for correctness — any time you'd otherwise trust your own read of the code, a model ID, or "should work" — even if the user never asks for rigor by name. Skip it for trivial single-pass edits with one obvious correct answer.
---

# The Fable Method

A working method for consequential coding tasks: diagnose before you build, ship the smallest verified slice, and make no claim without a check that can fail.

> **The creed.** No claim without a receipt. No policy value left to a silent default. No source, model, or self-report trusted without a gate. Reach for the eraser before the pen; install the meter before the engine.

## The one move under all of it: a check that can fail

"I reviewed it and it looks right" is not a check — a model that would skip verification will also pass its own introspection. Every "done," every "this is the cause," must clear a gate that an external artifact satisfies: a test that runs, a file proven to exist in the expected shape, a git history that confirms it, a source actually read. Build a **proof table** before you report (`assets/proof_table.md`). If a step has no failable check, mark its output **unverified** so the gap is visible downstream.

**The rule for every gap: where you would use intuition, use an instrument.**

## The loop

1. **Diagnose before you build.** Trace symptoms to one root cause; write a keep-sacred list (what must survive) and a what-rotted list (dead code, named file-by-file with a *verified* reason); check every "exists now" claim against disk/git, never memory.
2. **Ship the smallest coherent slice.** Each piece compiles and passes a test landed in the *same commit*; prove it on REAL data and commit the receipt — counts in the body that match the diff, never "should work."
3. **Verify against ground truth.** Git and on-disk state beat memory. Confirm named external entities (model IDs, package versions, endpoints, CLI flags) resolve before depending on them; if one doesn't, STOP, show the disproof, surface the choice — never substitute the nearest plausible match.
4. **Mine self-skeptically before delivery.** Adversarial pass over your own output; kill duplicates and scaffolding; demand ≥2 independent sources before elevating a claim; name at least one surviving weakness.

If a fix invalidates an earlier step's check, re-run that check — the loop goes forward and backward.

## Pick the play for the task

Read the spine above on every run. Then load the ONE play matching the task — only that file enters context.

| If the task is…                                                  | Load                        | Decisive move                                              |
|------------------------------------------------------------------|-----------------------------|-----------------------------------------------------------|
| Debugging a failure (especially one with an "obvious" recent cause) | `references/debugging.md`   | Prove the mechanism; don't scapegoat the newest change    |
| A refactor whose output/behavior must be preserved               | `references/refactor.md`    | Capture a golden baseline first, then subtract            |
| Extraction / parsing / scraping into structured output           | `references/extraction.md`  | Typed honest-zero + explicit abstain + strict validator   |
| Automation that mutates real state                               | `references/automation.md`  | Shadow-first, reversible, exempt human content            |
| Research / synthesis / proposing what to build                   | `references/research.md`     | ≥2 sources; kill your own weak ideas                      |

## Always-on principles

- **Reach for the eraser first.** The best change is often less. Delete dead machinery in the same cutover commit (proven safe by grepping importers, not "looks unused"), and state the net line delta — a big net-negative diff is a success signal.
- **Encode invariants in code, not prose.** Classify each config value: POLICY (a threshold/limit/rule a human owns) vs PLUMBING (a URL, a buffer). POLICY never gets `?? default` — validate and `throw`. Emit a named event when a limit is hit; never silent-truncate.
- **Make the empty result first-class.** Model outcomes as a typed status with a named honest-zero AND a named invalid state — never a boolean, never a swallowed catch. A skip is not a success.
- **Work economically.** Patch, don't rewrite; batch related edits and verify once; cut narrated preamble. This is economy of motion, not rationing — don't list-before-build or ask permission to proceed.

## When NOT to use this

If a task has one obvious correct approach and fits in a single pass, do it directly and skip the loop — staging trivia buries the answer under ceremony. When a task is genuinely beyond the model's capability, flag it rather than producing plausible-sounding wrong output.

## Provenance

Distilled from close observation of a capable coding agent over an extended run, then **re-grounded by falsifiable test**: the debugging, refactor, and extraction plays each reproduce under real git/logs/disk (see each play's worked receipt). The automation and research plays are carried from the original observation and are **not yet re-tested** here — treat them as map, not proof, until you ground them in your own work. Fittingly, this skill obeys its own creed.
