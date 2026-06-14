"""Reusable honest-zero scaffold for extraction / parse tasks.

Every outcome gets a typed status with a named honest-zero and a named invalid
state, so "no result" can never be silently rendered as a fabricated value.
Adapt has_anchor() and the validators to your domain.
"""

from enum import Enum
from typing import Any, Callable, Iterable, Mapping


class Status(str, Enum):
    PRODUCED = "produced"  # a valid result was extracted
    MISSING_REQUIRED_FIELD = "missing_required_field"  # target exists; required field is genuinely absent
    ABSTAIN_NO_MATCH = "abstain_no_match"  # input is not an instance of the target; do not guess
    INVALID_OUTPUT = "invalid_output"  # field is present but fails strict validation


Result = dict[str, Any]
Case = tuple[str, Callable[[Mapping[str, Any]], bool]]


def has_anchor(text: str) -> bool:
    """Return True only when the input is actually the target object.

    Example for invoices: require both an "invoice" marker and an "amount due"
    label before attempting extraction.
    """
    raise NotImplementedError


def validate_amount(raw: str) -> float | None:
    """Strict currency-like amount parser. Return a number or None.

    Never trust model prose such as "looks like about 1200"; parse the field.
    """
    import re

    match = re.fullmatch(r"\s*\$?([0-9]{1,3}(?:,[0-9]{3})*|[0-9]+)(?:\.([0-9]{2}))?\s*", raw)
    if not match:
        return None
    dollars, cents = match.groups()
    return float(f"{dollars.replace(',', '')}.{cents or '00'}")


def extract(text: str) -> Result:
    """Example shape for an extractor.

    Replace the placeholder field pull with domain-specific logic. Keep the
    status contract stable.
    """
    if not has_anchor(text):
        return {"status": Status.ABSTAIN_NO_MATCH}

    # Example shape:
    # raw_amount = pull_amount_field(text)
    # if raw_amount is None:
    #     return {"status": Status.MISSING_REQUIRED_FIELD, "field": "amount"}
    # amount = validate_amount(raw_amount)
    # if amount is None:
    #     return {"status": Status.INVALID_OUTPUT, "field": "amount", "raw": raw_amount}
    # return {"status": Status.PRODUCED, "amount": amount}
    raise NotImplementedError


def acceptance_harness(extract_fn: Callable[[str], Mapping[str, Any]], cases: Iterable[Case]) -> tuple[int, int]:
    """Run an extraction acceptance harness.

    Cases are (text, predicate) pairs. The suite must include:
    - a negative case the extractor has to abstain on;
    - an instance whose required field is missing;
    - an instance whose required field is present but unparseable.

    Returns (passed, total).
    """
    passed = 0
    total = 0
    for text, predicate in cases:
        total += 1
        try:
            result = extract_fn(text)
        except Exception as exc:  # harness keeps scoring instead of hiding failures
            result = {"status": Status.INVALID_OUTPUT, "error": repr(exc)}
        if predicate(result):
            passed += 1
    return passed, total
