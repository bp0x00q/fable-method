"""Honest-zero scaffold for extraction and parsing tasks."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any, Callable, Iterable, Mapping


class Status(str, Enum):
    PRODUCED = "produced"
    MISSING_REQUIRED_FIELD = "missing_required_field"
    ABSTAIN_NO_MATCH = "abstain_no_match"
    INVALID_OUTPUT = "invalid_output"


Result = dict[str, Any]
Case = tuple[str, Callable[[Mapping[str, Any]], bool]]
_AMOUNT = re.compile(
    r"\s*\$?([0-9]{1,3}(?:,[0-9]{3})*|[0-9]+)(?:\.([0-9]{2}))?\s*"
)


def has_anchor(text: str) -> bool:
    """Return True only when the input is an instance of the target object."""
    raise NotImplementedError


def validate_amount(raw: str) -> Decimal | None:
    """Parse a strict currency-like amount exactly; return None if malformed."""
    match = _AMOUNT.fullmatch(raw)
    if not match:
        return None

    whole, cents = match.groups()
    try:
        return Decimal(f"{whole.replace(',', '')}.{cents or '00'}")
    except InvalidOperation:
        return None


def extract(text: str) -> Result:
    """Replace the field pull while keeping this status contract stable."""
    if not has_anchor(text):
        return {"status": Status.ABSTAIN_NO_MATCH}

    # raw = pull_required_field(text)
    # if raw is None:
    #     return {"status": Status.MISSING_REQUIRED_FIELD, "field": "amount"}
    # amount = validate_amount(raw)
    # if amount is None:
    #     return {"status": Status.INVALID_OUTPUT, "field": "amount", "raw": raw}
    # return {"status": Status.PRODUCED, "amount": amount}
    raise NotImplementedError


def acceptance_harness(
    extract_fn: Callable[[str], Mapping[str, Any]],
    cases: Iterable[Case],
) -> tuple[int, int]:
    """Score positive, abstain, missing-field, and malformed-field cases."""
    passed = total = 0
    for text, predicate in cases:
        total += 1
        try:
            result = extract_fn(text)
        except Exception as exc:
            result = {"status": Status.INVALID_OUTPUT, "error": repr(exc)}
        passed += int(predicate(result))
    return passed, total
