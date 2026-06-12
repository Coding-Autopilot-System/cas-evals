"""Deterministic evaluation primitives."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .contracts import CONTRACT_VERSION, validate_evaluation_result

EVALUATOR_VERSION = "0.2.0"
DEFAULT_RELEASED_AT = "2026-06-11T00:00:00Z"


def _metric(value: float, threshold: float, passed: bool, details: dict[str, Any]) -> dict[str, Any]:
    return {"value": round(value, 6), "threshold": threshold, "passed": passed, "details": details}


def _traceparent(case_id: str) -> str:
    trace_id = hashlib.sha256(f"trace:{case_id}".encode()).hexdigest()[:32]
    parent_id = hashlib.sha256(f"parent:{case_id}".encode()).hexdigest()[:16]
    return f"00-{trace_id}-{parent_id}-01"


def lifecycle_metadata(case_id: str, suite_id: str, released_at: str) -> dict[str, Any]:
    """Build deterministic lifecycle metadata shared by offline and live evaluations."""
    return {
        "correlationId": f"eval-{case_id}",
        "promptId": case_id,
        "runId": suite_id,
        "timestamp": released_at,
        "traceContext": {"traceparent": _traceparent(case_id)},
    }


def _evaluate_case_with_evidence(
    case: dict[str, Any],
    suite_id: str,
    released_at: str,
    *,
    source_case: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
    execution_evidence: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    required = {"id", "kind", "prompt", "response", "expected", "limits"}
    missing = sorted(required - case.keys())
    if missing:
        raise ValueError(f"case missing required fields: {', '.join(missing)}")

    response = case["response"].casefold()
    expected = case["expected"]
    keywords = [word.casefold() for word in expected.get("keywords", [])]
    matched = [word for word in keywords if word in response]
    quality = 1.0 if not keywords else len(matched) / len(keywords)

    prohibited = [word.casefold() for word in expected.get("prohibited", [])]
    violations = [word for word in prohibited if word in response]
    safety = 1.0 if not violations else 0.0

    cost = float(case.get("observed", {}).get("cost_usd", 0.0))
    latency = float(case.get("observed", {}).get("latency_ms", 0.0))
    limits = case["limits"]

    evidence = {
        "quality": _metric(quality, float(limits["min_quality"]), quality >= float(limits["min_quality"]), {"matched": matched, "expected": keywords}),
        "safety": _metric(safety, 1.0, safety == 1.0, {"violations": violations}),
        "cost_usd": _metric(cost, float(limits["max_cost_usd"]), cost <= float(limits["max_cost_usd"]), {"source": "fixture"}),
        "latency_ms": _metric(latency, float(limits["max_latency_ms"]), latency <= float(limits["max_latency_ms"]), {"source": "fixture"}),
    }
    passed = all(metric["passed"] for metric in evidence.values())
    canonical = json.dumps(source_case or case, sort_keys=True, separators=(",", ":")).encode("utf-8")
    lifecycle = metadata or lifecycle_metadata(case["id"], suite_id, released_at)
    result = {
        "kind": "EvaluationResult",
        "correlationId": lifecycle["correlationId"],
        "promptId": lifecycle["promptId"],
        "runId": lifecycle["runId"],
        "repo": "Coding-Autopilot-System/cas-evals",
        "actor": {"id": "cas-evals", "type": "service"},
        "timestamp": lifecycle["timestamp"],
        "schemaVersion": CONTRACT_VERSION,
        "traceContext": lifecycle["traceContext"],
        "evaluator": f"cas-evals/{EVALUATOR_VERSION}",
        "outcome": "passed" if passed else "failed",
        "metrics": {
            "quality": round(quality, 6),
            "safety": round(safety, 6),
            "costUsd": round(cost, 6),
            "latencyMs": round(latency, 6),
        },
    }
    validate_evaluation_result(result)
    case_evidence = {
        "caseId": case["id"],
        "fixtureDigest": f"sha256:{hashlib.sha256(canonical).hexdigest()}",
        "passed": passed,
        "metrics": evidence,
    }
    if execution_evidence is not None:
        case_evidence["execution"] = execution_evidence
    return result, case_evidence


def evaluate_case(
    case: dict[str, Any], suite_id: str = "cas-standalone", released_at: str = DEFAULT_RELEASED_AT
) -> dict[str, Any]:
    """Evaluate one fixture case and emit a shared-contract result."""
    result, _ = _evaluate_case_with_evidence(case, suite_id, released_at)
    return result


def evaluate_suite(path: str | Path) -> dict[str, Any]:
    """Evaluate all cases in a fixture file."""
    fixture_path = Path(path)
    suite = json.loads(fixture_path.read_text(encoding="utf-8"))
    released_at = suite.get("releasedAt", DEFAULT_RELEASED_AT)
    evaluated = [_evaluate_case_with_evidence(case, suite["suiteId"], released_at) for case in suite["cases"]]
    results = [result for result, _ in evaluated]
    evidence = [item for _, item in evaluated]
    return {
        "schemaVersion": "0.2.0",
        "suiteId": suite["suiteId"],
        "results": results,
        "evidence": evidence,
        "summary": {
            "total": len(results),
            "passed": sum(result["outcome"] == "passed" for result in results),
            "failed": sum(result["outcome"] != "passed" for result in results),
        },
    }
