#!/usr/bin/env python3
"""Create and maintain a local evidence-first Fable workspace.

Python 3.9+; standard library only. The fixed workspace path is ``.fable``.
``state.json`` is authoritative; Markdown files are rendered views.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterator, List, Mapping, Optional, Sequence, Tuple

SCHEMA_VERSION = 1
MANAGED_BY = "fable-workspace"
WORKSPACE_NAME = ".fable"
KNOWN_FILES = (
    ".gitignore",
    "contract.md",
    "proof-table.md",
    "evidence-log.md",
    "parking-lot.md",
    "release-gate.md",
    "state.json",
)

GATE_CRITERIA: Sequence[Tuple[str, str]] = (
    ("intended_environment", "Works in intended environment"),
    ("representative_evaluation", "Representative evaluation completed"),
    ("primary_threshold", "Primary acceptance threshold met"),
    ("failure_modes", "Failure modes documented"),
    ("rollback", "Fallback, escalation, or rollback defined"),
    ("reproducible", "Result reproducible or demonstrable"),
    ("claims_trace", "External claims trace to evidence"),
    ("target_solved", "Locked target actually solved"),
)
GATE_LABELS = dict(GATE_CRITERIA)
ALLOW_NA = {"rollback", "claims_trace"}
PROOF_STATUSES = {"verified", "unverified", "refuted"}
GATE_STATUSES = {"pending", "pass", "fail", "n/a"}
DECISIONS = {"ship", "final-slice", "pivot", "archive"}
PLACEHOLDERS = {"", "tbd", "todo", "none", "not yet", "n/a", "na", "unknown"}


class FableError(RuntimeError):
    """Raised for user-correctable workspace errors."""


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def today() -> str:
    return dt.date.today().isoformat()


def parse_date(value: str) -> str:
    try:
        return dt.date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc


def one_line_arg(value: str) -> str:
    try:
        return clean_text(value, "value")
    except FableError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def clean_text(value: Any, field: str, *, optional: bool = False) -> str:
    if value is None and optional:
        return ""
    if not isinstance(value, str):
        raise FableError(f"{field} must be text")
    text = value.strip()
    if not text and not optional:
        raise FableError(f"{field} must not be blank")
    if "\x00" in text or "\n" in text or "\r" in text:
        raise FableError(f"{field} must be one line")
    if len(text) > 4000:
        raise FableError(f"{field} is too long (maximum 4000 characters)")
    return text


def md_cell(value: Any) -> str:
    text = str(value) if value is not None else ""
    return text.replace("|", "\\|")


def root_path(value: str, *, create: bool = False) -> Path:
    root = Path(value).expanduser()
    if not root.exists():
        if not create:
            raise FableError(f"project root does not exist: {root}")
        root.mkdir(parents=True, exist_ok=False)
    root = root.resolve()
    if not root.is_dir():
        raise FableError(f"project root is not a directory: {root}")
    return root


def workspace_path(root: Path) -> Path:
    return root / WORKSPACE_NAME


def ensure_not_symlink(path: Path, label: str) -> None:
    if path.is_symlink():
        raise FableError(f"refusing symlinked {label}: {path}")


def chmod_private(path: Path, mode: int) -> None:
    if os.name != "nt":
        os.chmod(path, mode)


def fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    try:
        fd = os.open(str(path), flags)
    except OSError:
        return
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write(path: Path, content: str) -> None:
    parent = path.parent
    ensure_not_symlink(parent, "workspace directory")
    if not parent.is_dir():
        raise FableError(f"workspace directory is missing: {parent}")
    ensure_not_symlink(path, path.name)

    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=str(parent))
    temp = Path(temp_name)
    try:
        if os.name != "nt":
            os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(temp), str(path))
        chmod_private(path, 0o600)
        fsync_directory(parent)
    except Exception:
        with contextlib.suppress(OSError):
            temp.unlink()
        raise


def initial_gate() -> Dict[str, Dict[str, str]]:
    return {key: {"status": "pending", "evidence": ""} for key, _ in GATE_CRITERIA}


def validate_state(state: Any) -> Dict[str, Any]:
    if not isinstance(state, dict):
        raise FableError("workspace state must be a JSON object")
    if state.get("schema_version") != SCHEMA_VERSION:
        raise FableError("unsupported or missing workspace schema version")
    if state.get("managed_by") != MANAGED_BY:
        raise FableError("directory is not marked as a Fable workspace")

    required_strings = (
        "project",
        "mode",
        "target",
        "acceptance",
        "environment",
        "deadline",
        "created_at",
        "updated_at",
        "started_on",
    )
    for key in required_strings:
        clean_text(state.get(key), f"state.{key}")
    try:
        dt.date.fromisoformat(state["deadline"])
    except ValueError as exc:
        raise FableError("state.deadline is not YYYY-MM-DD") from exc
    if state["mode"] not in {"start", "recover"}:
        raise FableError("state.mode must be start or recover")

    for key in ("constraints", "non_goals", "proof_entries", "parking_lot", "decisions"):
        if not isinstance(state.get(key), list):
            raise FableError(f"state.{key} must be a list")
    for key in ("constraints", "non_goals"):
        for index, item in enumerate(state[key]):
            clean_text(item, f"state.{key}[{index}]")
    if not state["non_goals"]:
        raise FableError("state.non_goals must contain at least one exclusion")
    if not isinstance(state.get("stack", ""), str):
        raise FableError("state.stack must be text")

    gate = state.get("gate")
    if not isinstance(gate, dict) or set(gate) != set(GATE_LABELS):
        raise FableError("state.gate has missing or unknown criteria")
    for key, item in gate.items():
        if not isinstance(item, dict) or item.get("status") not in GATE_STATUSES:
            raise FableError(f"invalid gate status for {key}")
        if not isinstance(item.get("evidence", ""), str):
            raise FableError(f"invalid gate evidence for {key}")
        if item["status"] == "n/a" and key not in ALLOW_NA:
            raise FableError(f"criterion {key} cannot be n/a")

    proof_by_id: Dict[str, Mapping[str, Any]] = {}
    for index, entry in enumerate(state["proof_entries"]):
        if not isinstance(entry, dict) or entry.get("status") not in PROOF_STATUSES:
            raise FableError("invalid proof entry")
        for field in ("id", "timestamp", "claim", "source", "evidence"):
            clean_text(entry.get(field), f"state.proof_entries[{index}].{field}")
        proof_id = entry["id"]
        if not re.fullmatch(r"P-[0-9]+", proof_id) or proof_id in proof_by_id:
            raise FableError(f"invalid or duplicate proof id: {proof_id}")
        proof_by_id[proof_id] = entry

    for key, item in gate.items():
        if item["status"] != "pass":
            continue
        proof_ids = re.findall(r"\bP-[0-9]+\b", item["evidence"].upper())
        if not proof_ids:
            raise FableError(f"passed criterion {key} must cite a proof id")
        bad = [pid for pid in proof_ids if pid not in proof_by_id or proof_by_id[pid]["status"] != "verified"]
        if bad:
            raise FableError(f"passed criterion {key} cites missing or non-verified proof: {', '.join(bad)}")
    return state


def load_state(workspace: Path) -> Dict[str, Any]:
    ensure_not_symlink(workspace, "workspace")
    if not workspace.is_dir():
        raise FableError(f"workspace not found: {workspace}")
    state_path = workspace / "state.json"
    ensure_not_symlink(state_path, "state file")
    if not state_path.is_file():
        raise FableError(f"workspace state not found: {state_path}")
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise FableError(f"cannot read workspace state: {exc}") from exc
    return validate_state(state)


def save_state(workspace: Path, state: Dict[str, Any]) -> None:
    state["updated_at"] = now_utc()
    validate_state(state)
    atomic_write(
        workspace / "state.json",
        json.dumps(state, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
    )


@contextlib.contextmanager
def workspace_lock(workspace: Path) -> Iterator[None]:
    ensure_not_symlink(workspace, "workspace")
    lock_path = workspace / ".lock"
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(str(lock_path), flags, 0o600)
    except FileExistsError as exc:
        raise FableError(f"workspace is locked: {lock_path}") from exc
    try:
        payload = f"pid={os.getpid()} created={now_utc()}\n".encode("utf-8")
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
    try:
        yield
    finally:
        with contextlib.suppress(OSError):
            lock_path.unlink()


def bullet_lines(values: Sequence[str], empty: str = "- None recorded") -> str:
    return "\n".join(f"- {value}" for value in values) if values else empty


def render_contract(state: Mapping[str, Any]) -> str:
    recovery = ""
    if state["mode"] == "recover":
        recovery = """
## Recovery audit

| Existing item | Current receipt/state | Keep/Cut/Park | Required action |
|---|---|---|---|
| _Complete before substantial new work_ |  |  |  |
"""
    stack = state.get("stack") or "Not locked"
    return f"""# Fable Project Contract

## Mode

{state['mode']}

## Locked target

Deliver **{state['target']}** by **{state['deadline']}**, accepted when **{state['acceptance']}**, in **{state['environment']}**.

## Project

- Name: {state['project']}
- Started: {state['started_on']}
- Decision date: {state['deadline']}
- Stack: {stack}

## Constraints

{bullet_lines(state['constraints'])}

## Non-goals

{bullet_lines(state['non_goals'])}
{recovery}
## Evidence-producing slices

| Slice | Risk or unknown resolved | Decisive check | Evidence location |
|---|---|---|---|
| Thin end-to-end path |  |  |  |
| Representative behavior |  |  |  |
| Intended-environment run |  |  |  |

## Change gate

A scope or stack change requires a new user/safety requirement, failed acceptance criterion, or demonstrated infeasibility; the blocker must be recorded, and expected risk reduction must exceed migration cost.

## Immediate next check

Resolve the highest-risk unknown with the smallest check that can fail.
"""


def render_proof_table(state: Mapping[str, Any]) -> str:
    lines = [
        "# Proof Table",
        "",
        "| id | claim | source/check | current evidence | status | caveat |",
        "|---|---|---|---|---|---|",
    ]
    for entry in state["proof_entries"]:
        lines.append(
            "| {id} | {claim} | {source} | {evidence} | {status} | {caveat} |".format(
                id=md_cell(entry["id"]),
                claim=md_cell(entry["claim"]),
                source=md_cell(entry["source"]),
                evidence=md_cell(entry["evidence"]),
                status=md_cell(entry["status"]),
                caveat=md_cell(entry.get("caveat") or "None recorded"),
            )
        )
    if not state["proof_entries"]:
        lines.append("| _none yet_ |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "Unsupported claims remain `unverified`; disproof remains `refuted`.",
            "",
        ]
    )
    return "\n".join(lines)


def render_evidence_log(state: Mapping[str, Any]) -> str:
    lines = [
        "# Evidence Log",
        "",
        "Each entry records an observed result. Hours and announcements are not evidence.",
        "",
    ]
    if not state["proof_entries"]:
        lines.append("_No entries yet._\n")
    for entry in state["proof_entries"]:
        lines.extend(
            [
                f"## {entry['id']} — {entry['timestamp']}",
                "",
                f"- **Claim:** {entry['claim']}",
                f"- **Source/check:** {entry['source']}",
                f"- **Observed evidence:** {entry['evidence']}",
                f"- **Status:** {entry['status']}",
                f"- **Caveat:** {entry.get('caveat') or 'None recorded'}",
                f"- **Next proof-producing action:** {entry.get('next') or 'None recorded'}",
                "",
            ]
        )
    return "\n".join(lines)


def render_parking_lot(state: Mapping[str, Any]) -> str:
    lines = [
        "# Parking Lot",
        "",
        "Recording an idea does not change the active contract.",
        "",
        "| id | date | idea | why deferred | review trigger |",
        "|---|---|---|---|---|",
    ]
    for item in state["parking_lot"]:
        lines.append(
            "| {id} | {date} | {idea} | {reason} | {trigger} |".format(
                id=md_cell(item["id"]),
                date=md_cell(item["date"]),
                idea=md_cell(item["idea"]),
                reason=md_cell(item["reason"]),
                trigger=md_cell(item["review_trigger"]),
            )
        )
    if not state["parking_lot"]:
        lines.append("| _none_ |  |  |  |  |")
    lines.append("")
    return "\n".join(lines)


def current_decision(state: Mapping[str, Any]) -> Optional[Mapping[str, Any]]:
    decisions = state.get("decisions", [])
    return decisions[-1] if decisions else None


def gate_ready(state: Mapping[str, Any]) -> bool:
    gate = state["gate"]
    for key, _ in GATE_CRITERIA:
        status_value = gate[key]["status"]
        if status_value == "pass":
            continue
        if status_value == "n/a" and key in ALLOW_NA:
            continue
        return False
    return True


def gate_blockers(state: Mapping[str, Any]) -> List[str]:
    blockers: List[str] = []
    for key, label in GATE_CRITERIA:
        item = state["gate"][key]
        if item["status"] == "pass" or (item["status"] == "n/a" and key in ALLOW_NA):
            continue
        blockers.append(f"{key}: {item['status']} ({label})")
    return blockers


def render_release_gate(state: Mapping[str, Any]) -> str:
    decision = current_decision(state)
    decision_text = (
        f"{decision['decision']} — {decision['reason']} ({decision['timestamp']})"
        if decision
        else "not set"
    )
    lines = [
        "# Fable Release Gate",
        "",
        "A criterion passes only with non-placeholder evidence.",
        "",
        f"- Decision: {decision_text}",
        f"- Release ready: {'yes' if gate_ready(state) else 'no'}",
        "",
        "| key | criterion | status | evidence |",
        "|---|---|---|---|",
    ]
    for key, label in GATE_CRITERIA:
        item = state["gate"][key]
        lines.append(
            f"| `{key}` | {md_cell(label)} | {md_cell(item['status'])} | {md_cell(item['evidence'])} |"
        )
    lines.extend(["", "## Blocking gaps", ""])
    blockers = gate_blockers(state)
    lines.extend(f"- {item}" for item in blockers)
    if not blockers:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def render_views(workspace: Path, state: Mapping[str, Any]) -> None:
    atomic_write(workspace / "contract.md", render_contract(state))
    atomic_write(workspace / "proof-table.md", render_proof_table(state))
    atomic_write(workspace / "evidence-log.md", render_evidence_log(state))
    atomic_write(workspace / "parking-lot.md", render_parking_lot(state))
    atomic_write(workspace / "release-gate.md", render_release_gate(state))


def next_backup_path(workspace: Path) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    candidate = workspace.with_name(f"{workspace.name}.backup-{stamp}")
    counter = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = workspace.with_name(f"{workspace.name}.backup-{stamp}-{counter}")
        counter += 1
    return candidate


def initialize(args: argparse.Namespace) -> Dict[str, Any]:
    root = root_path(args.root, create=args.create_root)
    workspace = workspace_path(root)
    ensure_not_symlink(workspace, "workspace")

    deadline = dt.date.fromisoformat(args.deadline)
    if deadline < dt.date.today():
        raise FableError("--deadline cannot be in the past")

    non_goals = [clean_text(item, "non-goal") for item in args.non_goal]
    constraints = [clean_text(item, "constraint") for item in args.constraint]
    if not non_goals:
        raise FableError("at least one --non-goal is required")

    state: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "managed_by": MANAGED_BY,
        "project": clean_text(args.project, "project"),
        "mode": args.mode,
        "target": clean_text(args.target, "target"),
        "acceptance": clean_text(args.acceptance, "acceptance"),
        "environment": clean_text(args.environment, "environment"),
        "deadline": args.deadline,
        "constraints": constraints,
        "non_goals": non_goals,
        "stack": clean_text(args.stack, "stack", optional=True),
        "started_on": today(),
        "created_at": now_utc(),
        "updated_at": now_utc(),
        "proof_entries": [],
        "parking_lot": [],
        "gate": initial_gate(),
        "decisions": [],
    }

    backup: Optional[Path] = None
    if workspace.exists():
        if not args.reset:
            raise FableError(f"workspace already exists: {workspace}; use --reset for a managed workspace")
        load_state(workspace)  # Refuses unrelated directories and malformed markers.
        backup = next_backup_path(workspace)
        workspace.rename(backup)

    temp_dir: Optional[Path] = None
    try:
        temp_dir = Path(tempfile.mkdtemp(prefix=".fable.init-", dir=str(root)))
        chmod_private(temp_dir, 0o700)
        atomic_write(temp_dir / ".gitignore", "*\n!.gitignore\n")
        save_state(temp_dir, state)
        render_views(temp_dir, state)
        temp_dir.rename(workspace)
        temp_dir = None
        fsync_directory(root)
    except Exception:
        if temp_dir is not None:
            shutil.rmtree(temp_dir, ignore_errors=True)
        if backup is not None and backup.exists() and not workspace.exists():
            backup.rename(workspace)
        raise

    return {
        "action": "initialized",
        "workspace": str(workspace),
        "backup": str(backup) if backup else None,
        "files": [str(workspace / name) for name in KNOWN_FILES],
    }


def append_proof(args: argparse.Namespace) -> Dict[str, Any]:
    root = root_path(args.root)
    workspace = workspace_path(root)
    with workspace_lock(workspace):
        state = load_state(workspace)
        status_value = args.status
        if status_value not in PROOF_STATUSES:
            raise FableError(f"invalid proof status: {status_value}")
        number = len(state["proof_entries"]) + 1
        entry = {
            "id": f"P-{number:02d}",
            "timestamp": now_utc(),
            "claim": clean_text(args.claim, "claim"),
            "source": clean_text(args.source, "source"),
            "evidence": clean_text(args.evidence, "evidence"),
            "status": status_value,
            "caveat": clean_text(args.caveat, "caveat", optional=True),
            "next": clean_text(args.next_action, "next", optional=True),
        }
        state["proof_entries"].append(entry)
        save_state(workspace, state)
        render_views(workspace, state)
    return {"action": "logged", "workspace": str(workspace), "proof_id": entry["id"]}


def park_idea(args: argparse.Namespace) -> Dict[str, Any]:
    root = root_path(args.root)
    workspace = workspace_path(root)
    with workspace_lock(workspace):
        state = load_state(workspace)
        number = len(state["parking_lot"]) + 1
        item = {
            "id": f"I-{number:02d}",
            "date": today(),
            "idea": clean_text(args.idea, "idea"),
            "reason": clean_text(args.reason, "reason"),
            "review_trigger": clean_text(args.review_trigger, "review-trigger"),
        }
        state["parking_lot"].append(item)
        save_state(workspace, state)
        render_views(workspace, state)
    return {"action": "parked", "workspace": str(workspace), "idea_id": item["id"]}


def meaningful_evidence(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in PLACEHOLDERS:
        return False
    if normalized.startswith("[") and normalized.endswith("]"):
        return False
    return True


def update_gate(args: argparse.Namespace) -> Dict[str, Any]:
    root = root_path(args.root)
    workspace = workspace_path(root)
    criterion = args.criterion
    status_value = args.status
    if criterion not in GATE_LABELS:
        raise FableError(f"unknown criterion: {criterion}")
    if status_value not in GATE_STATUSES:
        raise FableError(f"invalid gate status: {status_value}")
    if status_value == "n/a" and criterion not in ALLOW_NA:
        raise FableError(f"criterion {criterion} cannot be n/a")

    evidence = clean_text(args.evidence, "evidence", optional=status_value == "pending")
    if status_value != "pending" and not meaningful_evidence(evidence):
        raise FableError("pass, fail, and n/a gate updates require non-placeholder evidence")
    if status_value == "pending":
        evidence = ""

    with workspace_lock(workspace):
        state = load_state(workspace)
        if status_value == "pass":
            proof_ids = re.findall(r"\bP-[0-9]+\b", evidence.upper())
            if not proof_ids:
                raise FableError("a passed criterion must cite at least one proof id")
            proof_by_id = {entry["id"]: entry for entry in state["proof_entries"]}
            bad = [pid for pid in proof_ids if pid not in proof_by_id or proof_by_id[pid]["status"] != "verified"]
            if bad:
                raise FableError("gate pass cites missing or non-verified proof: " + ", ".join(bad))
        state["gate"][criterion] = {"status": status_value, "evidence": evidence}
        save_state(workspace, state)
        render_views(workspace, state)
        ready = gate_ready(state)
    return {
        "action": "gate-updated",
        "workspace": str(workspace),
        "criterion": criterion,
        "status": status_value,
        "release_ready": ready,
    }


def decide(args: argparse.Namespace) -> Dict[str, Any]:
    root = root_path(args.root)
    workspace = workspace_path(root)
    decision_value = args.decision
    if decision_value not in DECISIONS:
        raise FableError(f"invalid decision: {decision_value}")
    reason = clean_text(args.reason, "reason")

    with workspace_lock(workspace):
        state = load_state(workspace)
        if decision_value == "ship" and not gate_ready(state):
            raise FableError("cannot ship; release gate blockers: " + "; ".join(gate_blockers(state)))
        record = {"decision": decision_value, "reason": reason, "timestamp": now_utc()}
        state["decisions"].append(record)
        save_state(workspace, state)
        render_views(workspace, state)
    return {"action": "decided", "workspace": str(workspace), **record}


def sync_views(args: argparse.Namespace) -> Dict[str, Any]:
    root = root_path(args.root)
    workspace = workspace_path(root)
    with workspace_lock(workspace):
        state = load_state(workspace)
        render_views(workspace, state)
    return {"action": "synced", "workspace": str(workspace)}


def status(args: argparse.Namespace) -> Dict[str, Any]:
    root = root_path(args.root)
    workspace = workspace_path(root)
    state = load_state(workspace)
    deadline = dt.date.fromisoformat(state["deadline"])
    proof_counts = {key: 0 for key in sorted(PROOF_STATUSES)}
    for entry in state["proof_entries"]:
        proof_counts[entry["status"]] += 1
    gate_counts = {key: 0 for key in sorted(GATE_STATUSES)}
    for item in state["gate"].values():
        gate_counts[item["status"]] += 1
    return {
        "workspace": str(workspace),
        "project": state["project"],
        "mode": state["mode"],
        "target": state["target"],
        "acceptance": state["acceptance"],
        "environment": state["environment"],
        "deadline": state["deadline"],
        "days_remaining": (deadline - dt.date.today()).days,
        "proof_entries": len(state["proof_entries"]),
        "proof_statuses": proof_counts,
        "parked_ideas": len(state["parking_lot"]),
        "gate_statuses": gate_counts,
        "release_ready": gate_ready(state),
        "gate_blockers": gate_blockers(state),
        "decision": current_decision(state),
        "updated_at": state["updated_at"],
    }


def self_test() -> Dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="fable-workspace-test-") as temp:
        root = Path(temp) / "project"
        root.mkdir()
        init_args = argparse.Namespace(
            root=str(root),
            create_root=False,
            reset=False,
            project="Self Test",
            mode="start",
            target="a verified vertical slice for a test operator",
            acceptance="one representative check passes",
            environment="temporary fixture",
            deadline=(dt.date.today() + dt.timedelta(days=7)).isoformat(),
            constraint=["standard library only"],
            non_goal=["no unrelated features"],
            stack="Python",
        )
        initialize(init_args)
        append_proof(
            argparse.Namespace(
                root=str(root),
                claim="The vertical slice handles the representative case",
                source="self-test fixture",
                evidence="1/1 passed",
                status="verified",
                caveat="Only the fixture was tested",
                next_action="Run boundary cases",
            )
        )
        append_proof(
            argparse.Namespace(
                root=str(root),
                claim="Load behavior is acceptable",
                source="load test not run",
                evidence="No measurement",
                status="unverified",
                caveat="Requires a load fixture",
                next_action="Run the load fixture",
            )
        )
        try:
            update_gate(
                argparse.Namespace(
                    root=str(root),
                    criterion="primary_threshold",
                    status="pass",
                    evidence="P-02",
                )
            )
        except FableError:
            pass
        else:
            raise FableError("self-test accepted a non-verified proof for a gate pass")
        park_idea(
            argparse.Namespace(
                root=str(root),
                idea="Add an unrelated dashboard",
                reason="Outside the locked target",
                review_trigger="After the release decision",
            )
        )
        for key, _ in GATE_CRITERIA:
            gate_status = "n/a" if key in ALLOW_NA else "pass"
            update_gate(
                argparse.Namespace(
                    root=str(root),
                    criterion=key,
                    status=gate_status,
                    evidence="P-01" if gate_status == "pass" else "Not applicable to fixture; no mutation or external claim",
                )
            )
        decide(
            argparse.Namespace(
                root=str(root),
                decision="ship",
                reason="All required gate criteria pass",
            )
        )
        result = status(argparse.Namespace(root=str(root)))
        workspace = root / WORKSPACE_NAME
        missing = [name for name in KNOWN_FILES if not (workspace / name).is_file()]
        if missing:
            raise FableError(f"self-test missing files: {missing}")
        if result["proof_entries"] != 2 or result["parked_ideas"] != 1:
            raise FableError(f"self-test count mismatch: {result}")
        if not result["release_ready"] or result["decision"]["decision"] != "ship":
            raise FableError(f"self-test release decision failed: {result}")
        try:
            update_gate(
                argparse.Namespace(
                    root=str(root),
                    criterion="primary_threshold",
                    status="pass",
                    evidence="TBD",
                )
            )
        except FableError:
            pass
        else:
            raise FableError("self-test accepted placeholder gate evidence")

        if os.name != "nt":
            if stat.S_IMODE(workspace.stat().st_mode) != 0o700:
                raise FableError("workspace directory is not mode 0700")
            for name in KNOWN_FILES:
                mode = stat.S_IMODE((workspace / name).stat().st_mode)
                if mode != 0o600:
                    raise FableError(f"{name} is not mode 0600: {oct(mode)}")

        unrelated_root = Path(temp) / "unrelated"
        unrelated_workspace = unrelated_root / WORKSPACE_NAME
        unrelated_workspace.mkdir(parents=True)
        (unrelated_workspace / "notes.txt").write_text("not managed\n", encoding="utf-8")
        bad_args = argparse.Namespace(**vars(init_args))
        bad_args.root = str(unrelated_root)
        bad_args.reset = True
        try:
            initialize(bad_args)
        except FableError:
            pass
        else:
            raise FableError("self-test reset an unrelated directory")

        return {
            "self_test": "passed",
            "files_checked": len(KNOWN_FILES),
            "release_ready": result["release_ready"],
            "placeholder_evidence_rejected": True,
            "unverified_gate_receipt_rejected": True,
            "unrelated_reset_rejected": True,
            "private_permissions_checked": os.name != "nt",
        }


def add_root_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", default=".", help="Project root. Default: current directory.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create and maintain a Fable project workspace.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize the fixed .fable workspace.")
    add_root_argument(init_parser)
    init_parser.add_argument("--project", required=True, type=one_line_arg)
    init_parser.add_argument("--mode", choices=("start", "recover"), default="start")
    init_parser.add_argument("--target", required=True, type=one_line_arg)
    init_parser.add_argument("--acceptance", required=True, type=one_line_arg)
    init_parser.add_argument("--environment", required=True, type=one_line_arg)
    init_parser.add_argument("--deadline", required=True, type=parse_date)
    init_parser.add_argument("--constraint", action="append", default=[], type=one_line_arg)
    init_parser.add_argument(
        "--non-goal",
        action="append",
        required=True,
        type=one_line_arg,
        help="Explicit exclusion. Repeat for multiple non-goals.",
    )
    init_parser.add_argument("--stack", default=None, type=one_line_arg)
    init_parser.add_argument("--create-root", action="store_true")
    init_parser.add_argument(
        "--reset",
        action="store_true",
        help="Back up and replace only an existing workspace with a valid Fable marker.",
    )

    log_parser = subparsers.add_parser("log", help="Append a proof-table entry.")
    add_root_argument(log_parser)
    log_parser.add_argument("--claim", required=True, type=one_line_arg)
    log_parser.add_argument("--source", required=True, type=one_line_arg)
    log_parser.add_argument("--evidence", required=True, type=one_line_arg)
    log_parser.add_argument("--status", required=True, choices=sorted(PROOF_STATUSES))
    log_parser.add_argument("--caveat", default=None, type=one_line_arg)
    log_parser.add_argument("--next", dest="next_action", default=None, type=one_line_arg)

    park_parser = subparsers.add_parser("park", help="Add an idea without changing the contract.")
    add_root_argument(park_parser)
    park_parser.add_argument("--idea", required=True, type=one_line_arg)
    park_parser.add_argument("--reason", required=True, type=one_line_arg)
    park_parser.add_argument("--review-trigger", required=True, type=one_line_arg)

    gate_parser = subparsers.add_parser("gate", help="Set one release-gate criterion.")
    add_root_argument(gate_parser)
    gate_parser.add_argument("--criterion", required=True, choices=tuple(GATE_LABELS))
    gate_parser.add_argument("--status", required=True, choices=("pending", "pass", "fail", "n/a"))
    gate_parser.add_argument("--evidence", default=None, type=one_line_arg)

    decide_parser = subparsers.add_parser("decide", help="Record ship/final-slice/pivot/archive.")
    add_root_argument(decide_parser)
    decide_parser.add_argument("--decision", required=True, choices=sorted(DECISIONS))
    decide_parser.add_argument("--reason", required=True, type=one_line_arg)

    status_parser = subparsers.add_parser("status", help="Print machine-readable status.")
    add_root_argument(status_parser)

    sync_parser = subparsers.add_parser("sync", help="Regenerate Markdown views from state.json.")
    add_root_argument(sync_parser)

    subparsers.add_parser("self-test", help="Run an isolated end-to-end test.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "init":
            result = initialize(args)
        elif args.command == "log":
            result = append_proof(args)
        elif args.command == "park":
            result = park_idea(args)
        elif args.command == "gate":
            result = update_gate(args)
        elif args.command == "decide":
            result = decide(args)
        elif args.command == "status":
            result = status(args)
        elif args.command == "sync":
            result = sync_views(args)
        elif args.command == "self-test":
            result = self_test()
        else:
            parser.error(f"unknown command: {args.command}")
            return 2
    except (FableError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
