"""Reusable honest-zero scaffold for extraction / parse tasks.

Every outcome gets a typed status with a named honest-zero AND a named invalid
state, so "no result" can never be silently rendered as a fabricated value.
Adapt has_anchor() and the validators to your domain.
"""

from enum import Enum


class Status(str, Enum):
    PRODUCED = "produced"          # a valid result was extracted
    PARTIAL = "partial"           # required field genuinely absent (honest zero)
    ABSTAIN = "abstain_no_match"  # input is NOT an instance of the target — do not guess
    INVALID = "invalid_output"    # field present but fails the strict validator


def has_anchor(text: str) -> bool:
    """The input must actually BE the target thing before we extract from it.
    e.g. for invoices: require both an 'invoice' marker AND an 'amount due' label."""
    raise NotImplementedError


def validate_amount(raw: str):
    """Strict: return a number, or None if it does not parse. Never trust the prose."""
    import re
    m = re.match(r'([\d,]+(?:\.\d{2})?)\s*$', raw.strip())
    return float(m.group(1).replace(",", "")) if m else None


def extract(text: str) -> dict:
    if not has_anchor(text):
        return {"status": Status.ABSTAIN}
    # ... pull the raw field, then:
    #   amount = validate_amount(raw)
    #   if amount is None: return {"status": Status.INVALID, "raw": raw}
    raise NotImplementedError


def acceptance_harness(extract_fn, cases) -> tuple:
    """cases: list of (text, predicate). MUST include a negative case the extractor
    has to abstain on, and a present-but-unparseable case. Returns (passed, total)."""
    passed = sum(1 for text, ok in cases if ok(extract_fn(text)))
    return passed, len(cases)
