"""Opt-in deterministic adapter for the local CAS reference product."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from .contracts import CONTRACT_VERSION
from .evaluator import DEFAULT_RELEASED_AT, _evaluate_case_with_evidence, lifecycle_metadata

DEFAULT_REFERENCE_PRODUCT_URL = "http://127.0.0.1:8080/api/v1/workflows"
REFERENCE_PRODUCT_TARGET = "cas-reference-product/api/v1/workflows"
MAX_RESPONSE_BYTES = 2_000_000
Transport = Callable[[dict[str, Any]], dict[str, Any]]


class ReferenceProductError(RuntimeError):
    """Raised when the reference-product contract is unavailable or invalid."""


def _digest_text(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"


def _http_transport(endpoint: str, timeout_seconds: float) -> Transport:
    parsed = urlsplit(endpoint)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ReferenceProductError("reference product endpoint must be an HTTP(S) URL")
    if timeout_seconds <= 0:
        raise ReferenceProductError("reference product timeout must be greater than zero")

    def post(envelope: dict[str, Any]) -> dict[str, Any]:
        request = Request(
            endpoint,
            data=json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                payload = response.read(MAX_RESPONSE_BYTES + 1)
        except HTTPError as error:
            raise ReferenceProductError(f"reference product returned HTTP {error.code}") from None
        except (URLError, TimeoutError, OSError):
            raise ReferenceProductError("reference product is unavailable") from None
        if len(payload) > MAX_RESPONSE_BYTES:
            raise ReferenceProductError("reference product response exceeds the size limit")
        try:
            value = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ReferenceProductError("reference product returned invalid JSON") from None
        if not isinstance(value, dict):
            raise ReferenceProductError("reference product response must be an object")
        return value

    return post


def _build_envelope(case: dict[str, Any], suite_id: str, released_at: str) -> dict[str, Any]:
    metadata = lifecycle_metadata(case["id"], suite_id, released_at)
    return {
        "kind": "PromptEnvelope",
        **metadata,
        "repo": "Coding-Autopilot-System/cas-evals",
        "actor": {"id": "cas-evals", "type": "service"},
        "schemaVersion": CONTRACT_VERSION,
        "intent": case.get("capability", case["kind"]),
        "prompt": case["prompt"],
        "constraints": case.get("constraints", []),
    }


def _validate_response(response: dict[str, Any], envelope: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    output = response.get("output")
    events = response.get("events")
    if (
        response.get("runId") != envelope["runId"]
        or not isinstance(output, str)
        or not output
        or not isinstance(events, list)
    ):
        raise ReferenceProductError("reference product response contract is invalid")
    if not events:
        raise ReferenceProductError("reference product response contains no lifecycle events")

    expected = {
        "correlationId": envelope["correlationId"],
        "promptId": envelope["promptId"],
        "runId": envelope["runId"],
        "traceContext": envelope["traceContext"],
    }
    normalized_events = []
    for event in events:
        if not isinstance(event, dict) or any(event.get(field) != value for field, value in expected.items()):
            raise ReferenceProductError("reference product did not preserve lifecycle metadata")
        normalized_events.append(
            {
                **expected,
                "eventType": event.get("eventType"),
                "sequence": event.get("sequence"),
                "status": event.get("status"),
            }
        )
    return output, normalized_events


def evaluate_reference_suite(
    path: str | Path,
    *,
    endpoint: str = DEFAULT_REFERENCE_PRODUCT_URL,
    timeout_seconds: float = 5.0,
    transport: Transport | None = None,
) -> dict[str, Any]:
    """Evaluate a fixture suite against the local reference-product workflow endpoint."""
    fixture_path = Path(path)
    suite = json.loads(fixture_path.read_text(encoding="utf-8"))
    released_at = suite.get("releasedAt", DEFAULT_RELEASED_AT)
    invoke = transport or _http_transport(endpoint, timeout_seconds)
    evaluated = []

    for source_case in suite["cases"]:
        envelope = _build_envelope(source_case, suite["suiteId"], released_at)
        output, events = _validate_response(invoke(envelope), envelope)
        live_case = {**source_case, "response": output}
        evidence = {
            "adapter": "cas-reference-product",
            "target": REFERENCE_PRODUCT_TARGET,
            "lifecycle": {
                field: envelope[field]
                for field in ("correlationId", "promptId", "runId", "traceContext")
            },
            "responseDigest": _digest_text(output),
            "events": events,
            "timing": {
                "latencyMs": float(source_case.get("observed", {}).get("latency_ms", 0.0)),
                "normalization": "fixture-observed",
            },
        }
        evaluated.append(
            _evaluate_case_with_evidence(
                live_case,
                suite["suiteId"],
                released_at,
                source_case=source_case,
                metadata=envelope,
                execution_evidence=evidence,
            )
        )

    results = [result for result, _ in evaluated]
    return {
        "schemaVersion": "0.2.0",
        "suiteId": suite["suiteId"],
        "results": results,
        "evidence": [evidence for _, evidence in evaluated],
        "summary": {
            "total": len(results),
            "passed": sum(result["outcome"] == "passed" for result in results),
            "failed": sum(result["outcome"] != "passed" for result in results),
        },
    }
