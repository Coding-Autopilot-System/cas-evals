"""Deterministic evaluation primitives."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

EVALUATOR_VERSION = "0.1.0"


def _metric(value: float, threshold: float, passed: bool, details: dict[str, Any]) -> dict[str, Any]:
    return {"value": round(value, 6), "threshold": threshold, "passed": passed, "details": details}


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one fixture case without side effects or external services."""
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

    metrics = {
        "quality": _metric(quality, float(limits["min_quality"]), quality >= float(limits["min_quality"]), {"matched": matched, "expected": keywords}),
        "safety": _metric(safety, 1.0, safety == 1.0, {"violations": violations}),
        "cost_usd": _metric(cost, float(limits["max_cost_usd"]), cost <= float(limits["max_cost_usd"]), {"source": "fixture"}),
        "latency_ms": _metric(latency, float(limits["max_latency_ms"]), latency <= float(limits["max_latency_ms"]), {"source": "fixture"}),
    }
    passed = all(metric["passed"] for metric in metrics.values())
    canonical = json.dumps(case, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "schemaVersion": "0.1.0",
        "evaluatorVersion": EVALUATOR_VERSION,
        "caseId": case["id"],
        "kind": case["kind"],
        "correlationId": f"eval-{case['id']}",
        "fixtureDigest": f"sha256:{hashlib.sha256(canonical).hexdigest()}",
        "passed": passed,
        "metrics": metrics,
    }


def evaluate_suite(path: str | Path) -> dict[str, Any]:
    """Evaluate all cases in a fixture file."""
    fixture_path = Path(path)
    suite = json.loads(fixture_path.read_text(encoding="utf-8"))
    results = [evaluate_case(case) for case in suite["cases"]]
    return {
        "schemaVersion": "0.1.0",
        "suiteId": suite["suiteId"],
        "results": results,
        "summary": {
            "total": len(results),
            "passed": sum(result["passed"] for result in results),
            "failed": sum(not result["passed"] for result in results),
        },
    }
