# Play: Refactor with a contract — keep sacred, then subtract

Before touching anything:

1. **Write the preservation contract.** Name the exact surface that must not change — signature plus the behavior the caller depends on. This is the keep-sacred list.
2. **Capture a golden baseline on REAL data.** Run the frozen surface now and save its exact output to `golden.txt`. This is the receipt the whole refactor is checked against. "Looks equivalent" is not a check; byte-equality is.

Then refactor by subtraction:

3. **Prove dead code dead.** `grep` for importers/call-sites — zero call-sites, not "looks unused." Delete it in the cutover commit and state the net line delta; a big net-negative diff is the success signal.
4. **Re-assert against golden.** After the refactor, diff the frozen surface's output against `golden.txt`. It must be IDENTICAL. A plausible "cleanup" — sorting rows, tightening a number format, summing-then-rounding instead of rounding-then-summing — is exactly what silently breaks an exact-bytes contract.

**Worked receipt (reproduced).** A "tidy-up" of a finance report alphabetized the rows and narrowed a column; the frozen `build_quarterly()` output then DIFFERED from golden (the downstream parser would break). The semantics-preserving version diffed IDENTICAL, while still removing 5 dead functions — each verified at 0 call-sites — for a net −24 lines.
