# Play: Automation that mutates state — shadow-first

> Carried from the original observation; **not yet re-tested by a falsifiable run here.** Ground it in your own work before trusting it.

- **Shadow-first behind a flag.** Ship the mutation disabled; produce the dry-run output it *would* make and inspect that before any real write.
- **Make destructive outcomes reversible** (write to a new location, soft-delete, keep an undo path) and prefer additive operations.
- **Exempt human-authored content** from automated mutation or cleanup by default.
- **POLICY values throw, never default.** A threshold/limit/rule never gets `?? default` — validate and `throw` a multi-line WHAT / WHY / HOW.
- **Emit a named telemetry event when a limit is hit; never silent-truncate** — a runaway must not be able to hide.
