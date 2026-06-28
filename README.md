# Fable Method

Fable Method is an evidence-first engineering skill for Claude Code and Codex.
It is meant for consequential coding work where a plausible but wrong answer is
costly: ambiguous debugging, refactors, automation, external dependencies,
multi-session recovery, or release decisions.

The core loop is:

```text
contract -> diagnose -> slice -> verify -> critique -> decide
```

The important rule is simple: no consequential claim without a receipt that
could have failed. A receipt can be a test, runtime log, diff, source read, git
history, dry run, registry response, or other external check.

## When To Use It

Use Fable Method when the problem needs scope control and proof:

- lock the target before changing code
- reproduce or inspect before theorizing
- ship the smallest coherent slice
- rerun checks invalidated by later changes
- state caveats instead of implying broader proof than the receipts support

Skip it for trivial one-pass edits and plain factual lookups.

## Project-Cycle Mode

For stalled, multi-session, or release-bound work, load
`references/project-cycle.md`. That play adds:

```text
locked target -> keep/cut/park recovery -> thin verified slices
-> gated scope changes -> evidence-gated release decision
```

The optional workspace helper creates a private local `.fable/` state directory:

```bash
python3 scripts/fable_workspace.py init \
  --root /path/to/project \
  --project "Project name" \
  --target "Deliverable for the named user/problem" \
  --acceptance "Measurable threshold and evidence" \
  --environment "Representative runtime or test set" \
  --deadline YYYY-MM-DD \
  --non-goal "Explicit exclusion"
```

## How It Works With The Other Two Skills

These three skills are useful independently:

- `fable-method`: locks and verifies the engineering slice
- `evaluate-by-experiment`: tests a contestable claim with a falsifiable setup
- `recursive-self-improvement`: iterates one verified improvement in the
  current session without spawning child model sessions

They also compose well:

```text
Fable Method locks the outcome and proof standard.
Evaluate by Experiment tests the riskiest claim or proposed method.
Recursive Self-Improvement repeats the smallest verified improvement loop.
```

That composition is not a guarantee of quality. It is a way to make quality
claims harder to fake.

## Install

Clone this repository or copy the directory into a Codex/agent skill surface,
for example:

```bash
cp -a fable-method ~/.codex/skills/fable-method
```

For project-local agent surfaces, use the project convention, such as:

```text
.agents/skills/fable-method
```

## Verify

Run the deterministic checks before publishing a changed package:

```bash
python3 -m py_compile assets/status_enum.py scripts/fable_workspace.py
python3 scripts/fable_workspace.py self-test
sha256sum -c SHA256SUMS.txt
```

`BUILD_RECEIPT.md` records what these checks do and do not prove.
