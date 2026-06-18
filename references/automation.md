# Play: Mutating automation — shadow-first

Before a real write:

1. Ship mutation disabled or behind an explicit activation flag.
2. Produce a dry-run manifest:

   ```text
   action | target | reason | would_change | exempted | rollback_path | risk | status
   ```

3. Prove both target and exclusion sets. Protect human-authored content by default.
4. Prefer additive writes, soft deletion, versioned outputs, or another tested undo path.
5. Validate human-owned policy values; do not silently default thresholds or limits.
6. Emit named audit/telemetry events for limits and truncation.
7. After execution, reconcile actual changes against the manifest and prove rollback on a representative item.

See `receipts.md#automation` for a reproduced deletion-safety example.
