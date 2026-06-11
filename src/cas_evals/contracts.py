"""Offline validation for the vendored CAS shared evaluation contract."""

from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any

CONTRACT_VERSION = "0.1.0"
VENDOR_DIR = Path(__file__).parents[2] / "vendor" / "cas-contracts" / "v0.1.0"
PROVENANCE_PATH = VENDOR_DIR / "provenance.json"

_ACTOR_TYPES = {"human", "agent", "service", "workflow"}
_OUTCOMES = {"passed", "failed", "inconclusive"}
_RESULT_FIELDS = {
    "correlationId",
    "promptId",
    "runId",
    "repo",
    "actor",
    "timestamp",
    "schemaVersion",
    "traceContext",
    "kind",
    "evaluator",
    "outcome",
    "metrics",
}
_TRACEPARENT = re.compile(r"^[\da-f]{2}-[\da-f]{32}-[\da-f]{16}-[\da-f]{2}$")
_REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class ContractValidationError(ValueError):
    """Raised when shared-contract provenance or an emitted result is invalid."""


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _require_string(value: Any, field: str, minimum: int = 1, maximum: int = 128) -> str:
    if not isinstance(value, str) or not minimum <= len(value) <= maximum:
        raise ContractValidationError(f"{field} must be a string with length {minimum}..{maximum}")
    return value


def verify_vendored_contract() -> dict[str, Any]:
    """Verify immutable provenance and expected identities of vendored schemas."""
    provenance = _load_json(PROVENANCE_PATH)
    for filename, expected in provenance["schemas"].items():
        path = VENDOR_DIR / filename
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected["sha256"]:
            raise ContractValidationError(f"vendored schema digest mismatch: {filename}")

    common = _load_json(VENDOR_DIR / "common.schema.json")
    evaluation = _load_json(VENDOR_DIR / "evaluation-result.schema.json")
    if common.get("$id") != "https://schemas.coding-autopilot.dev/v0.1/common.schema.json":
        raise ContractValidationError("unexpected common schema identity")
    if evaluation.get("$id") != "https://schemas.coding-autopilot.dev/v0.1/evaluation-result.schema.json":
        raise ContractValidationError("unexpected evaluation schema identity")
    if evaluation["allOf"][0].get("$ref") != "common.schema.json#/$defs/lifecycleMetadata":
        raise ContractValidationError("evaluation schema does not reference the vendored common schema")
    return provenance


def validate_evaluation_result(result: dict[str, Any]) -> None:
    """Validate the complete constraint surface of shared EvaluationResult v0.1.0."""
    verify_vendored_contract()
    if not isinstance(result, dict):
        raise ContractValidationError("evaluation result must be an object")
    missing = sorted(_RESULT_FIELDS - result.keys())
    extra = sorted(result.keys() - _RESULT_FIELDS)
    if missing:
        raise ContractValidationError(f"evaluation result missing fields: {', '.join(missing)}")
    if extra:
        raise ContractValidationError(f"evaluation result has unevaluated fields: {', '.join(extra)}")

    for field in ("correlationId", "promptId", "runId"):
        _require_string(result[field], field)
    repo = _require_string(result["repo"], "repo", maximum=512)
    if not _REPO.fullmatch(repo):
        raise ContractValidationError("repo must use owner/name format")
    if result["schemaVersion"] != CONTRACT_VERSION:
        raise ContractValidationError(f"schemaVersion must be {CONTRACT_VERSION}")

    actor = result["actor"]
    if not isinstance(actor, dict) or set(actor) - {"id", "type", "displayName"}:
        raise ContractValidationError("actor contains invalid fields")
    if not {"id", "type"} <= actor.keys():
        raise ContractValidationError("actor requires id and type")
    _require_string(actor["id"], "actor.id", maximum=256)
    if actor["type"] not in _ACTOR_TYPES:
        raise ContractValidationError("actor.type is invalid")
    if "displayName" in actor:
        _require_string(actor["displayName"], "actor.displayName", maximum=256)

    timestamp = _require_string(result["timestamp"], "timestamp", maximum=64)
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as error:
        raise ContractValidationError("timestamp must be an ISO 8601 date-time") from error

    trace = result["traceContext"]
    if not isinstance(trace, dict) or not {"traceparent"} <= trace.keys() or set(trace) - {"traceparent", "tracestate"}:
        raise ContractValidationError("traceContext is invalid")
    if not isinstance(trace["traceparent"], str) or not _TRACEPARENT.fullmatch(trace["traceparent"]):
        raise ContractValidationError("traceContext.traceparent is invalid")
    if "tracestate" in trace:
        _require_string(trace["tracestate"], "traceContext.tracestate", maximum=512)

    if result["kind"] != "EvaluationResult":
        raise ContractValidationError("kind must be EvaluationResult")
    _require_string(result["evaluator"], "evaluator", maximum=256)
    if result["outcome"] not in _OUTCOMES:
        raise ContractValidationError("outcome is invalid")
    metrics = result["metrics"]
    if not isinstance(metrics, dict) or not metrics:
        raise ContractValidationError("metrics must be a non-empty object")
    for name, value in metrics.items():
        _require_string(name, "metric name", maximum=256)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ContractValidationError(f"metric {name} must be a finite number")
