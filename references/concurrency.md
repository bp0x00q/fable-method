# Play: Concurrency / shared-state bugs — reproduce under contention, assert an invariant

The trap: a data race passes every single-threaded run and survives every glance. The code "looks right" because corruption only appears when executions interleave. A unit test that calls the function once will pass.

1. **Name the invariant.** What must hold regardless of interleaving: final count equals increments performed, no two orders share an ID, a balance never goes negative, every enqueue has one dequeue. "It ran without error" is not an invariant; races often corrupt silently.
2. **Reproduce under contention, not in isolation.** Stress it with many workers × many iterations. Shrink the thread-switch interval, widen the critical section, add jitter, or run repeated trials so interleavings actually happen.
3. **Assert the invariant over the stressed run.** Compare observed end state to what the invariant demands on every run. Record the failing seed/config when available.
4. **Fix by making the critical section atomic.** Use a lock, atomic primitive, transactional operation, or queue that serializes access. Prefer eliminating shared mutable state over guarding it.
5. **Re-run the same stress harness.** The same harness that exposed the race must pass after the fix.

## Worked receipt

A non-atomic counter incremented by 8 threads × 5,000 times should end at 40,000. Single-threaded it returned exactly 5,000, so a glance and a naive unit test passed. Under contention it returned 5,013, silently losing 34,987 updates with no exception. Wrapping the read-modify-write in a lock returned exactly 40,000 on the identical harness.
