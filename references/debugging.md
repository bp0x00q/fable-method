# Play: Debugging — prove the mechanism

The trap is blaming the newest plausible change or patching around the symptom.

1. Capture the exact failing command, input, environment/config pointer, and observed output.
2. Classify the failure before theorizing: crash, empty result, wrong value, timeout, or skip.
3. Instrument the path with counts or markers until the failing stage is localized.
4. Trace focused history for the value or file that controls that stage.
5. Falsify the obvious cause by reverting or disabling it and rerunning the same reproduction.
6. Ship only when the fix changes the original failing observation and the proof table records the result.

See `receipts.md#debugging` for a reproduced red-herring example.
