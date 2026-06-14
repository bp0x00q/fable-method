# Play: Extraction / parsing — honest-zero kills fabrication

The trap: a best-guess extractor always emits a row, so it invents a value for inputs that have none — turning a cover letter into an invoice, or grabbing an ID as the amount.

1. **Model every outcome as a typed status**, with a named honest-zero AND a named invalid state — never a boolean, never a swallowed catch. e.g. `produced | partial | abstain_no_match | invalid_output`. A skip is not a success. See `assets/status_enum.py`.
2. **Define the abstain output explicitly, and require an anchor before extracting.** The input must actually *be* the target thing. No anchor → abstain, don't guess.
3. **Validate with a strict parser, never the prose.** The amount must parse as currency; the date must parse as a date. Unparseable → `invalid_output` (keep the raw for debugging), not a fabricated number.
4. **Gate adoption behind an acceptance harness that INCLUDES the negative case it must refuse**, scored n/m — a non-instance the extractor must abstain on, plus an instance whose required field is present-but-unparseable.

**Worked receipt (reproduced).** Against a 4-document harness with a cover-letter trap and a "TBD" amount, the best-guess extractor scored 1/4 (fabricated a $4,500 total from the letter; grabbed an invoice number as a total). The typed/abstain/validated extractor scored 4/4 — abstained on the letter, flagged the TBD amount as invalid, and marked a missing date MISSING rather than blanking it.
