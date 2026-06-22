---
name: fable-method
metadata:
  self_test: "python3 scripts/fable_workspace.py self-test"
description: >-
  Use for consequential coding or focused multi-step builds where a
  plausible-but-wrong result is costly: ambiguous debugging, preserving
  behavior through refactors, extraction, mutating automation, concurrency,
  external dependencies, stalled projects, scope drift, or release decisions.
  Lock the outcome, diagnose before changing code, ship the smallest verified
  slice, and support consequential conclusions with checks that could fail.
  Optionally retain verified reusable discoveries. Skip trivial one-pass edits.
---

# The Fable Method

**contract → diagnose → slice → verify → critique → decide**

## Receipt rule

No consequential claim without an external check that could return “no”: a test, diff, log, runtime result, filesystem fact, git history, registry response, or source actually read. This applies to diagnosis, shipped behavior, dependencies, destructive actions, scope changes, and user-facing conclusions.

Create `assets/proof_table.md` before reporting. Leave unsupported claims `unverified` and disproved claims `refuted`.

> Where intuition would carry the decision, install an instrument.

## Select the operating depth

- **Task:** Run the core loop.
- **Project cycle:** Also load `references/project-cycle.md` for multi-session, stalled, drifting, or release-bound work.
- **Retention:** Load `references/learning.md` only after a verified, non-obvious, reusable discovery. Otherwise stop.

## Core loop

1. **Contract.** Define one outcome, its user/context, intended environment, keep-sacred surface, forbidden outcomes, and decisive pass check. For a project cycle, add a decision date, constraints, and non-goals.
2. **Diagnose.** Reproduce first. Read logs, runtime state, disk, and focused history before theorizing. Prove mechanism, not correlation.
3. **Slice.** Resolve the highest-risk unknown with the smallest coherent change or thin end-to-end path. Put the meter before the engine: baseline, guardrail, audit event, negative case, or dry run before risky behavior.
4. **Verify.** Run the decisive check on representative real or fixture data and record the receipt. Resolve named packages, models, endpoints, versions, and flags before relying on them.
5. **Critique.** Remove duplicate work, speculative scaffolding, and unsupported scope. Record a surviving caveat and update the proof table.
6. **Decide.** Continue, narrow, ship, pivot, or archive. For project cycles, ship only when the release gate passes; otherwise name the smallest blocking evidence gap.

Rerun any check invalidated by later changes.

## Load the smallest relevant play set

Use one primary technical play; add another only for a distinct gate.

| Task | Play | Gate |
|---|---|---|
| Stalled, drifting, multi-session, or release-bound work | `references/project-cycle.md` | Locked target and evidence-gated decision |
| Ambiguous failure | `references/debugging.md` | Reproduce and prove mechanism |
| Behavior-preserving refactor | `references/refactor.md` | Contract and golden comparison |
| Extraction or structured output | `references/extraction.md` | Honest-zero, abstain, strict validation |
| Automation that mutates state | `references/automation.md` | Dry run, exclusions, rollback |
| Research or build proposal | `references/research.md` | Resolve entities and test claims |
| Threads, async, workers, shared state | `references/concurrency.md` | Contention harness and invariant |

## Invariants

- **One active outcome.** Park unrelated ideas; recording one does not change the contract.
- **Subtract first.** Patch rather than rewrite; prove code dead before deleting it.
- **Changes need cause.** Expand scope or switch stack only for new user evidence, safety/compliance needs, a failed criterion, or demonstrated infeasibility—and only when risk reduction exceeds migration cost.
- **Policy is explicit.** Validate human-owned thresholds and fail with WHAT / WHY / HOW.
- **Empty is typed.** Keep `success`, `empty`, `skipped`, `invalid`, and `abstain` distinct.
- **Mutation is gated.** Prove targets, exclusions, dry-run output, rollback, and post-run result. Protect human-authored content by default.
- **Verify at semantic boundaries.** Batch mechanical edits; rerun checks when behavior or risk changes.

## Done means

- The contracted slice works in its intended environment.
- Relevant checks ran and receipts exist.
- Consequential claims are `verified`, `unverified`, or `refuted`.
- Failure modes, caveats, and coverage limits are explicit.
- The decisive result is reproducible when practical.
- No broader success is implied than evidence supports.

## Scope and precedence

This skill governs engineering method, not platform policy. Higher-priority safety, consent, tool, filesystem, and environment instructions win. Use the strongest available instrument and state when the preferred one is unavailable.
