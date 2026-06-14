# Play: Debugging a failure — prove the mechanism

The trap: the newest, most plausible change gets blamed for being newest. A self-check ("is that the cause?") answers "probably" and ships a fix *around* it.

Instruments, in order:

1. **Read the on-disk state and the actual logs first.** What did the run truly produce or emit? Distinguish an empty result from a crash from a wrong value before theorizing.
2. **Localize before you theorize.** Instrument the suspect component (print counts at each stage) so the data tells you *where* the behavior dies, instead of guessing.
3. **Trace the history of the thing that controls the behavior, not the whole repo.** `git log -- <file_or_value_that_governs_the_output>` beats `git log` + blame-the-top. The cause is often an earlier change to a POLICY value, while the newest commit only changed how the failure is *reported*.
4. **Falsify the obvious fix before shipping it.** Revert or disable the suspected cause and re-run. If the symptom persists, it was not the cause — keep looking. No fix ships without clearing this gate.

**Worked receipt (reproduced under real git).** A job wrote empty output. The newest commit was "clean up logging" — reverting it changed nothing, the symptom persisted. Instrumenting the filter showed 8 rows read and 0 above threshold; `git log -- config.json` showed the threshold had been changed 10→1000 three commits earlier. The logging commit had only changed the success message from a record count to "Done.", which is exactly why it looked guilty.
