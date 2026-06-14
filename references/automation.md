# Play: Automation that mutates state — shadow-first

> **Core re-grounded by falsifiable test.** Shadow-first, exempt-human-content, and reversibility reproduced under real filesystem state. POLICY-throws and telemetry-on-limit remain carried from the original observation and should be grounded in your own codebase before being treated as proven.

## Required gates

1. **Shadow-first behind a flag.** Ship the mutation disabled. Produce the dry-run output it would make and inspect that before any real write.
2. **Emit a dry-run manifest.** Each candidate mutation should have a row shaped like:

   ```text
   action | target | reason | would_change | exempted | rollback_path | risk | status
   ```

3. **Prove target set and exclusion set.** The manifest must show what will change and what was deliberately spared. Human-authored content is exempt by default.
4. **Make destructive outcomes reversible.** Prefer additive operations. For deletes, use soft-delete/trash with restore proof. For overwrites, preserve old content or write to a new location first.
5. **POLICY values throw, never default.** A threshold/limit/rule never gets `?? default`; validate it and throw a multi-line WHAT / WHY / HOW error.
6. **Emit a named telemetry/audit event when a limit is hit.** Never silent-truncate; a runaway must not be able to hide.
7. **Emit a post-run receipt.** After a real run, record what actually changed — counts, paths, before/after — so the mutation is auditable, not just what it intended to change.

## Worked receipt

A "delete files older than 30 days" cleanup was run against a folder holding stale machine files plus one old human-authored `meeting_notes.md`. The naive version using immediate `os.remove` scored 0/3 because it irreversibly deleted the human file. The shadow-first version scored 3/3: it produced a dry-run manifest before mutating, exempted the `.md` file by type, and moved removals to `.trash`; a deleted file was then restored to prove reversibility. A recent control file was left untouched by both.
