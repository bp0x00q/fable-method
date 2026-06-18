# Play: Refactor — keep sacred, then subtract

1. Write the preservation contract: public API, signatures, flags, schema, bytes, ordering, formatting, side effects, errors, and load-bearing constants.
2. Capture a golden baseline on representative real or fixture data. Use byte equality unless the contract names a semantic comparator.
3. Search importers, call sites, runtime entry points, and generated references before declaring code dead.
4. Delete proven-dead machinery in the cutover and state the net line delta.
5. Rerun the frozen surface and compare against golden. Any allowed difference must already exist in the contract.

See `receipts.md#refactor` for a reproduced output-drift example.
