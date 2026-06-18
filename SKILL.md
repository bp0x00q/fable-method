---
name: fable-method
description: >-
  Use for consequential coding work where a plausible-but-wrong result is costly:
  ambiguous debugging, behavior-preserving refactors, extraction pipelines,
  mutating automation, concurrency, external dependencies, or multi-step work
  that is hard to verify by inspection. Diagnose before building, ship the
  smallest verified slice, and support every consequential conclusion with a
  check that could fail. After a verified non-obvious discovery, optionally
  stage and evaluate it as reusable skill knowledge. Skip trivial one-pass edits.
---

# The Fable Method

A compact operating method for consequential coding: **contract → diagnose → slice → verify → critique → retain only what earned persistence**.

## Core rule

No consequential claim without a receipt. If a claim affects the diagnosis, shipped behavior, dependency choice, destructive action, or user-facing conclusion, attach an external check that could return “no”: a test, diff, log, runtime result, filesystem fact, git history, registry response, or source actually read.

Build `assets/proof_table.md` before reporting. Unsupported claims stay visible as `unverified`; disproved claims stay visible as `refuted`.

> Where intuition would carry the decision, install an instrument.

## Run the loop

1. **Contract.** Define success, the keep-sacred surface, forbidden outcomes, and the check that will decide whether the work passed.
2. **Diagnose.** Reproduce first. Read logs, runtime state, disk, and focused history before theorizing. Prove a mechanism; do not confuse recency or correlation with cause.
3. **Slice.** Implement the smallest coherent change. Put the meter before the engine: baseline, guardrail, audit event, negative case, or dry run before risky behavior.
4. **Verify.** Run the decisive check on representative real or fixture data. Record the receipt where review can find it. Resolve named packages, models, endpoints, versions, and flags before depending on them.
5. **Critique.** Remove duplicate work, speculative scaffolding, and unsupported scope. Name a surviving caveat. Update the proof table.
6. **Retain selectively.** Only when the task produced a verified, non-obvious, reusable lesson, load `references/learning.md`. Otherwise stop; do not manufacture a lesson.

If a change invalidates an earlier check, rerun it. The loop moves backward as well as forward.

## Load the smallest relevant play set

Load one primary execution play. Add a second only when it contributes a distinct gate, such as mutating async automation requiring both automation and concurrency checks.

| Task | Play | Decisive gate |
|---|---|---|
| Ambiguous failure or plausible red herring | `references/debugging.md` | Reproduce and prove the mechanism |
| Refactor with behavior/output to preserve | `references/refactor.md` | Contract plus golden comparison |
| Extraction, parsing, or structured output | `references/extraction.md` | Honest-zero, abstain, strict validation |
| Automation that mutates real state | `references/automation.md` | Dry run, exclusions, rollback |
| Research or build proposal | `references/research.md` | Resolve entities, test claims, kill weak ideas |
| Threads, async, workers, or shared state | `references/concurrency.md` | Contention harness plus invariant |

After verified work, `references/learning.md` governs candidate skill creation, updates, promotion, deprecation, and archival.

## Always-on invariants

- **Subtract first.** Patch rather than rewrite. Prove dead code has no live callers before deleting it.
- **Policy is explicit.** Human-owned thresholds and limits do not get silent defaults; validate them and fail with WHAT / WHY / HOW.
- **Empty is typed.** Keep `success`, `empty`, `skipped`, `invalid`, and `abstain` distinct. A skip is not a pass.
- **Mutation is gated.** Prove target set, exclusion set, dry-run output, rollback path, and post-run result. Protect human-authored content by default.
- **Verification follows semantic boundaries.** Batch mechanical edits; verify whenever behavior or risk changes.

## Done means

- The smallest coherent slice is complete.
- Relevant checks ran and receipts exist.
- Every consequential claim is `verified`, `unverified`, or `refuted` in the proof table.
- Caveats and coverage limits are explicit.
- No broader success is implied than the evidence supports.

## Scope and precedence

This skill governs engineering method, not platform policy. Higher-priority safety, consent, tool, filesystem, and environment instructions win. Use the strongest available instrument and state when the preferred one is unavailable.

## Provenance

The execution plays have compact reproduced examples in `references/receipts.md`; those receipts establish only the tested claims under the tested scenarios. The learning lifecycle adapts the strongest ideas from continuous-learning skill systems—selective extraction, search-before-create, precise retrieval triggers, scoped storage, versioning, and deprecation—while adding Fable gates: staged candidates, evidence provenance, negative cases, and clean with/without-skill evaluation before promotion. Treat that lifecycle as a candidate method until it is benchmarked in the target environment.
