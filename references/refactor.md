# Play: Refactor with a contract — keep sacred, then subtract

Before touching anything:

1. **Write the preservation contract.** Name the exact surface that must not change: public API, function signatures, CLI flags, output schema, output bytes, ordering, numeric formatting, side effects, error behavior, and any constants/value ramps callers depend on. This is the keep-sacred list.
2. **Capture a golden baseline on representative real or fixture data.** Run the frozen surface now and save the exact output where review can find it (`golden.txt`, fixture snapshot, CI artifact, or PR-attached receipt). "Looks equivalent" is not a check; byte equality or a precise semantic comparator is.

Then refactor by subtraction:

3. **Prove dead code dead.** Search for importers/call-sites and runtime entry points. Require zero call-sites, not "looks unused." Delete dead machinery in the cutover commit and state the net line delta.
4. **Re-assert against golden.** After refactor, diff the frozen surface against the baseline. It must be identical unless the preservation contract explicitly allows a named difference. Plausible cleanup — sorting rows, tightening a number format, summing-then-rounding instead of rounding-then-summing — is exactly what silently breaks downstream consumers.

## Worked receipt

A "tidy-up" of a finance report alphabetized rows and narrowed a column; the frozen `build_quarterly()` output differed from golden, so the downstream parser would break. The semantics-preserving version diffed identical while removing 5 dead functions, each verified at 0 call-sites, for a net −24 lines.
