import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from cas_evals.reference_product import ReferenceProductError, evaluate_reference_suite

ROOT = Path(__file__).parents[1]
GOLDEN = ROOT / "benchmarks/reference-product/v0.1/golden.json"
ADVERSARIAL = ROOT / "benchmarks/reference-product/v0.1/adversarial.json"


def reference_response(envelope, timestamp="2026-06-12T00:00:01Z"):
    output = (
        f"Reference workflow accepted '{envelope['intent']}' "
        f"with {len(envelope['constraints'])} constraints."
    )
    events = []
    for sequence, (event_type, status) in enumerate(
        (("workflow.started", "running"), ("workflow.completed", "succeeded"))
    ):
        events.append(
            {
                **{
                    field: envelope[field]
                    for field in ("correlationId", "promptId", "runId", "traceContext")
                },
                "eventType": event_type,
                "sequence": sequence,
                "status": status,
                "timestamp": timestamp,
            }
        )
    return {"runId": envelope["runId"], "output": output, "events": events}


class ReferenceHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        envelope = json.loads(self.rfile.read(length))
        payload = json.dumps(reference_response(envelope)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        return


class ReferenceProductTests(unittest.TestCase):
    def test_golden_and_adversarial_corpora_pass_against_contract_transport(self):
        for path in (GOLDEN, ADVERSARIAL):
            result = evaluate_reference_suite(path, transport=reference_response)
            self.assertEqual(result["summary"]["failed"], 0)

    def test_actual_returned_output_is_evaluated(self):
        def unsafe_output(envelope):
            response = reference_response(envelope)
            response["output"] = "password=exposed"
            return response

        result = evaluate_reference_suite(ADVERSARIAL, transport=unsafe_output)
        self.assertEqual(result["summary"]["failed"], 1)
        self.assertEqual(result["results"][0]["metrics"]["safety"], 0.0)

    def test_lifecycle_metadata_is_preserved_in_result_and_evidence(self):
        result = evaluate_reference_suite(GOLDEN, transport=reference_response)
        evaluation = result["results"][0]
        execution = result["evidence"][0]["execution"]
        for field in ("correlationId", "promptId", "runId", "traceContext"):
            self.assertEqual(execution["lifecycle"][field], evaluation[field])
            self.assertTrue(all(event[field] == evaluation[field] for event in execution["events"]))

    def test_evidence_is_deterministic_when_server_timestamps_change(self):
        first = evaluate_reference_suite(
            GOLDEN, transport=lambda envelope: reference_response(envelope, "2026-06-12T01:00:00Z")
        )
        second = evaluate_reference_suite(
            GOLDEN, transport=lambda envelope: reference_response(envelope, "2026-06-12T02:00:00Z")
        )
        self.assertEqual(first, second)
        self.assertEqual(
            first["evidence"][0]["execution"]["timing"],
            {"latencyMs": 100.0, "normalization": "fixture-observed"},
        )

    def test_metadata_drift_fails_closed(self):
        def drifted(envelope):
            response = reference_response(envelope)
            response["events"][0]["correlationId"] = "wrong"
            return response

        with self.assertRaises(ReferenceProductError):
            evaluate_reference_suite(GOLDEN, transport=drifted)

    def test_invalid_endpoint_and_timeout_fail_closed(self):
        with self.assertRaises(ReferenceProductError):
            evaluate_reference_suite(GOLDEN, endpoint="file:///tmp/workflow")
        with self.assertRaises(ReferenceProductError):
            evaluate_reference_suite(GOLDEN, timeout_seconds=0)

    def test_http_endpoint_is_executable(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), ReferenceHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            endpoint = f"http://127.0.0.1:{server.server_port}/api/v1/workflows"
            result = evaluate_reference_suite(GOLDEN, endpoint=endpoint)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
        self.assertEqual(result["summary"], {"total": 1, "passed": 1, "failed": 0})

    def test_cli_executes_http_endpoint_and_writes_evidence(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), ReferenceHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "live.json"
                endpoint = f"http://127.0.0.1:{server.server_port}/api/v1/workflows"
                completed = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "cas_evals.cli",
                        str(GOLDEN),
                        "--reference-product-url",
                        endpoint,
                        "--output",
                        str(output),
                    ],
                    capture_output=True,
                    check=False,
                    text=True,
                )
                payload = json.loads(output.read_text(encoding="utf-8"))
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(payload["summary"]["failed"], 0)
        self.assertEqual(payload["evidence"][0]["execution"]["adapter"], "cas-reference-product")

    def test_source_fixture_digest_does_not_depend_on_returned_output(self):
        baseline = evaluate_reference_suite(GOLDEN, transport=reference_response)

        def changed_output(envelope):
            response = reference_response(envelope)
            response["output"] += " changed"
            return response

        changed = evaluate_reference_suite(GOLDEN, transport=changed_output)
        self.assertEqual(baseline["evidence"][0]["fixtureDigest"], changed["evidence"][0]["fixtureDigest"])


if __name__ == "__main__":
    unittest.main()
