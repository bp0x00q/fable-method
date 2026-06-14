# Play: Extraction / parsing — honest-zero kills fabrication

The trap: a best-guess extractor always emits a row, so it invents values for inputs that have none — turning a cover letter into an invoice, or grabbing an ID as an amount.

1. **Model every outcome as a typed status.** Use a named honest-zero and a named invalid state — never a boolean, never a swallowed catch. Suggested statuses: `produced | missing_required_field | abstain_no_match | invalid_output`. A skip is not a success. See `assets/status_enum.py`.
2. **Define the abstain output explicitly, and require an anchor before extracting.** The input must actually be the target thing. No anchor → `abstain_no_match`, not a guess.
3. **Validate with strict parsers and schema checks, never prose.** Amounts must parse as currency; dates must parse as dates; output must match the declared schema. Unparseable field → `invalid_output` with the raw value kept for debugging, not a fabricated number.
4. **Distinguish missing from invalid.** A required field genuinely absent is `missing_required_field`; a present but malformed field is `invalid_output`.
5. **Gate adoption behind an acceptance harness.** Score n/m. The suite must include a negative case the extractor must refuse, a missing-required-field case, and a present-but-unparseable case.

## Worked receipt

Against a 4-document harness with a cover-letter trap and a "TBD" amount, the best-guess extractor scored 1/4: it fabricated a $4,500 total from the letter and grabbed an invoice number as a total. The typed/abstain/validated extractor scored 4/4: it abstained on the letter, flagged the TBD amount as invalid, and marked a missing date as `missing_required_field` rather than blanking it.
