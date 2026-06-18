# Play: Concurrency — contention plus invariant

1. Name the invariant that must survive every interleaving.
2. Reproduce under contention with many workers, repeated trials, jitter, widened critical sections, or smaller switch intervals.
3. Assert the invariant on every stressed run; “no exception” is not a pass.
4. Record the failing seed or stress configuration when available.
5. Prefer removing shared mutable state; otherwise use an atomic primitive, transaction, lock, or serialized queue.
6. Rerun the identical stress harness after the fix.

See `receipts.md#concurrency` for a reproduced lost-update example.
