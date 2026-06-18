# Play: Extraction — honest-zero kills fabrication

1. Use typed outcomes: `produced`, `missing_required_field`, `abstain_no_match`, and `invalid_output`.
2. Require anchors proving the input is the target object before extraction. No anchor means abstain.
3. Parse fields and validate the complete schema; never trust prose or best guesses.
4. Distinguish absent from malformed and retain malformed raw values for debugging.
5. Gate adoption with an n/m harness containing a positive case, a non-instance to refuse, a missing-field case, and a present-but-malformed case.

Use `assets/status_enum.py`. See `receipts.md#extraction` for a reproduced fabrication trap.
