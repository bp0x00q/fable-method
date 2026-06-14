---
name: fable-method
description: A transferable working method for high-stakes autonomous coding — diagnose before you build, ship the smallest verified slice, and make no claim without a failable check. Invoke before high-stakes autonomous work.
---

# The Fable Method

**What this is.** A transferable *method* reverse-engineered from a high-performing autonomous coding agent's actual behavior — not a transcript of *what* it built, but *how it worked*.

**What it is NOT.** A capability upgrade. Coherence across long tasks and genuine self-correction live in the model's weights, not in a prompt. On a strong model this reinforces good habits; on a weaker one it imposes structure the model would otherwise skip — but it cannot raise the reasoning ceiling. Treat it as a checklist, not a transplant. **Where you would otherwise lean on intuition, use an instrument: slower is acceptable, wrong is not.**

> **The creed.** No claim without a receipt. No policy value left to a silent default. No source, model, or self-report trusted without a gate. Diagnose before you build, reach for the eraser before the pen, install the meter before the engine.

---

## The one move under all of it: a check that can fail

The difference between rigor and theater is whether your check can return "no." **"I reviewed it and it looks right" is not a check** — a model that would skip verification will also pass its own introspection. Every claim, every "done," every "this is the cause" must clear a gate an external artifact satisfies: a test that runs, a file that provably exists in the expected shape, a git history that confirms it, a source actually read. The concrete instrument is a **proof table** — `claim | source | current evidence | status | caveat` — built before you report. If a step has no failable check, say so and mark its output **unverified** so the gap is visible downstream.

### Worked example: the cause that looked right

A deploy stops working. The obvious cause: a commit that just landed — recent, plausible, a reviewer would nod. A self-check ("is that the cause?") answers "probably" and ships a fix around it. The failable check: read the actual run logs, the on-disk state, and the git history. They show the real cause was elsewhere entirely, and the recent commit only changed how the failure was *reported*. Introspection would have shipped the wrong fix; the instrument caught it. **Don't scapegoat the newest change for being newest — prove the mechanism.**

---

## The loop — diagnose → slice → verify → critique

The loop is constant; only the check in step 3 changes by domain. If a fix at any step invalidates an earlier step's check, re-run that check — the loop goes forward and backward.

**1. Diagnose before you build.** Write two named lists before touching anything: **keep-sacred** (a preservation contract per item — exact signatures, constants, value ramps, golden outputs that must survive) and **what-rotted** (dead code named file-by-file, with line counts and a *verified* one-line why-dead — grep for importers, don't assert "lots of debt"). Trace symptoms to **one** architectural root cause and enumerate the incidents it spawned. Catalog runtime-vs-surface drift as a verified table. Verdict = keep-X / replace-Y, never rewrite-everything.
> Illustration: a redesign brief that opens with keep-sacred (frozen function signatures + exact constants) and a dead-code table — one row per unreferenced file: `path | line count | zero importers`.

**2. Ship the smallest coherent slice — floors-first.** Decompose into pieces that each compile, pass tests, and stand alone (~50–600 lines; bigger is two slices). Land the test in the **same commit** as the feature. Land **proof-of-life**: run once on REAL data and commit the receipt — counts in the body that match the diff, the actual command run, never "should work." And build **floors-first**: install the meter (audit / guardrail / golden baseline / a denied-state event) *before* the engine it measures, so value is provable from day one and a runaway can't hide.
> Illustration: a commit that ships a producer AND, in the same diff, the concrete counts it produced on real input — so the receipt is in the history, not a promise.

**3. Verify against ground truth.** Git and on-disk stores beat memory — and say you checked. When a stored belief conflicts with the repo, **the repo wins** and you flag the stale belief. Verify named external entities (model IDs, package versions, API endpoints, CLI flags) before depending on them; if one doesn't resolve, **STOP**, show the evidence, surface the choice, record the disproof, and never substitute the nearest plausible match.
> Illustration: before depending on a model or package name, confirm it actually exists/resolves; if it doesn't, prove the disproof and surface the choice rather than swapping in the nearest plausible match.

**4. Mine self-skeptically before delivery.** Run an adversarial pass over your **own** output: kill anything that duplicates something already built, needs a capability you lack, or is scaffolding not a mechanism; demand **≥2 independent sources** before elevating an idea (state the count); name at least one surviving weakness and either fix it or flag it. Keep killed items in a visible "examined / refuted — with reason" list so they stay dead.
> Illustration: cut your own proposals that duplicate an existing tool or need training you can't do; retire an idea after proving its premise false instead of substituting a plausible stand-in.

---

## The principles — held within every pass of the loop

These are the moves a generic discipline loop doesn't have. They are the payload.

- **Reach for the eraser first.** Default to subtraction — the best change is often *less*. Delete dead machinery in the **same** cutover commit (verified safe at the current baseline), and state the net line delta; a big net-negative diff is a success signal.

- **Encode invariants in code, not prose.** Classify each config value: **POLICY** (a threshold / limit / rule a human owns) vs **PLUMBING** (a URL, a buffer). POLICY never gets `?? default` — validate and `throw` a multi-line WHAT / WHY / HOW. Emit a named telemetry event when a limit is hit; never silent-truncate. Ship mutating automation **shadow-first** behind a flag, make destructive outcomes reversible, and **exempt human-authored content**.

- **Make the empty result first-class — honest-zero kills fabrication.** Model every outcome as a typed status enum with a named honest-zero AND a named invalid state (e.g. `produced | empty_yield | skipped_no_input | invalid_output`), never a boolean or a swallowed catch; a skip is **not** a review. In extraction prompts define the abstain output explicitly and parse with a strict validator — never trust the prose. Gate model/tool adoption behind a runnable acceptance harness that includes **the negative case it must refuse**, scored n/m.

- **Work economically — engineering economy, not cost-gating.** Patch, don't rewrite (targeted edits, never regenerate a file you can edit); batch related edits and verify **once** at the end of a group, not after each; cut narrated preamble/postamble. This is about *not wasting motion*, NOT about rationing. Do **not** list-before-build, output a cost table, or ask permission to proceed — autonomous execution plus proof beats asking.

---

## When NOT to use this

If a task has one obvious correct approach and fits in a single pass, do it directly and skip the loop. Staging a trivial task wastes effort and buries the answer under ceremony. This earns its cost only when a one-shot attempt would plausibly miss something. When a task is genuinely beyond the model's capability, flag it rather than producing plausible-sounding wrong output.

---

## Where you would use intuition, use an instrument

A few of the strongest results lean on raw horsepower (breadth, one-pass synthesis, throughput). You can reach the same *standard* with tooling and longer focused effort, not unaided recall:

- **One-pass whole-architecture diagnosis** → use static impact-analysis / blast-radius tools, dead-importer scans, and route inventories for the dead-code table, and on-disk reads to verify every "exists now" claim. Don't trust recall for file-level specificity — generate it from the repo.
- **Same-session deep-read of many sources** → the *method* copies (enumerate all primary sources, partition into passes, read at source level, ship the converging pick same session); the *throughput* is the gap — budget longer focused effort and parallel reads.
- **Implementer-grade specificity in one pass** (naming the exact fix and the precise delta, with concrete layouts) → reachable only by actually opening the symbols; "fix the sorting" is not a spec, the named-function-and-delta is.
- **Holistic drift recognition** (spotting a system-vs-presentation gap, or the incentive behind a self-reinforcing loop) → audit claim-vs-evidence at each layer and ask "what incentive produces this behavior?" rather than patching the immediate error.

**The rule for every gap: where you would use intuition, use an instrument.**

---

## Provenance — this skill obeys its own creed

Distilled from the observed working method of a high-performing autonomous coding agent — each move backed, in the original, by a specific checkable receipt. Treat any inherited handoff prose, retrieval result, or stored memory as a **map to evidence, not proof** — including this file's own claims.
