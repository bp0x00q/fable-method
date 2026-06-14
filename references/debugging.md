# Play: Debugging a failure — prove the mechanism

The trap: the newest, most plausible change gets blamed for being newest. A self-check ("is that the cause?") answers "probably" and ships a fix around it.

## Instruments, in order

0. **Capture the failing command first.** Record the exact command, input, environment/config pointer, and observed output. If you cannot reproduce or point to the failure, your diagnosis is floating.
1. **Read the on-disk state and actual logs.** What did the run truly produce or emit? Distinguish `empty result`, `crash`, `wrong value`, `timeout`, and `skipped` before theorizing.
2. **Localize before you theorize.** Instrument the suspect path with counts/markers at each stage so the data tells you where behavior dies.
3. **Trace the history of the thing that controls the behavior, not the whole repo.** `git log -- <file_or_value_that_governs_the_output>` beats `git log` plus blame-the-top. The cause is often an earlier POLICY change while the newest commit only changed how failure is reported.
4. **Falsify the obvious fix before shipping it.** Revert or disable the suspected cause and re-run. If the symptom persists, it was not the cause.
5. **Ship only after the mechanism clears a failable check.** The fix must change the failing command's observed behavior, not merely make the explanation sound coherent.

## Worked receipt

A job wrote empty output. The newest commit was "clean up logging." Reverting it changed nothing: the symptom persisted. Instrumenting the filter showed 8 rows read and 0 above threshold. `git log -- config.json` showed the threshold had changed from 10 to 1000 three commits earlier. The logging commit had only changed the success message from a record count to "Done," which is why it looked guilty.
