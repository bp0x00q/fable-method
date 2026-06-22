# Fable Method

"Fable-Method" is an evidence-first engineering skill for Claude Code and Codex. There are many fable skills, but this one is mine. The behavioral change from Opus 4.8 to Mythos/Fable was subtle but *dramatic*. It is ridiculous to suggest this skill will achieve the same level of excellence, but it does produce a measurable improvement and you are encouraged to tell the LLM to actually prove that by evaluating through experiment. This skill was produced by a swarm of Opus 4.8 subagents on max effort mining my git history for the entire duration that Fable was first avaiable:

```text
contract → diagnose → slice → verify → critique → decide
```

For stalled or multi-session work, the optional project-cycle play adds only the useful focus controls:

```text
locked target → keep/cut/park recovery → thin verified slices
→ gated scope/stack changes → evidence-gated release decision
```

A verified, non-obvious, reusable discovery may then enter a guarded retention path:

```text
proof-table receipt → dedupe/search → staged candidate
→ positive/negative/boundary evaluation → promotion → revalidation or retirement
```

Focus means one bounded outcome, controlled change, and honest release evidence—not secrecy, lifestyle rules, or performative intensity.

## Optional workspace

`scripts/fable_workspace.py` (Python 3.9+, standard library only) creates a local `.fable/` contract, proof table, evidence log, parking lot, release gate, and machine-readable state. It uses a fixed directory, refuses to replace unrelated content, requires evidence for passed gate items, and applies restrictive filesystem permissions where supported.
