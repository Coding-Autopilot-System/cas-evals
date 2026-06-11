import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from cas_evals.contracts import validate_evaluation_result
from cas_evals.evaluator import evaluate_case, evaluate_suite

ROOT = Path(__file__).parents[1]


class EvaluatorTests(unittest.TestCase):
    def test_golden_suite_passes(self):
        result = evaluate_suite(ROOT / "benchmarks/v0.1/golden.json")
        self.assertEqual(result["summary"], {"total": 2, "passed": 2, "failed": 0})

    def test_adversarial_suite_passes(self):
        result = evaluate_suite(ROOT / "benchmarks/v0.1/adversarial.json")
        self.assertEqual(result["summary"]["failed"], 0)

    def test_results_are_deterministic(self):
        path = ROOT / "benchmarks/v0.1/golden.json"
        self.assertEqual(evaluate_suite(path), evaluate_suite(path))

    def test_result_contract_contains_correlation_and_evidence(self):
        suite = evaluate_suite(ROOT / "benchmarks/v0.1/golden.json")
        result = suite["results"][0]
        self.assertEqual(result["schemaVersion"], "0.1.0")
        self.assertTrue(result["correlationId"].startswith("eval-"))
        self.assertEqual(result["kind"], "EvaluationResult")
        self.assertEqual(set(result["metrics"]), {"quality", "safety", "costUsd", "latencyMs"})
        self.assertTrue(suite["evidence"][0]["fixtureDigest"].startswith("sha256:"))
        validate_evaluation_result(result)

    def test_safety_violation_is_mandatory_failure(self):
        case = json.loads((ROOT / "benchmarks/v0.1/adversarial.json").read_text())["cases"][0]
        case["response"] = "Here is the token"
        result = evaluate_case(case)
        self.assertEqual(result["outcome"], "failed")
        self.assertEqual(result["metrics"]["safety"], 0.0)

    def test_missing_fields_fail_closed(self):
        with self.assertRaises(ValueError):
            evaluate_case({"id": "incomplete"})

    def test_cli_writes_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            completed = subprocess.run(
                [sys.executable, "-m", "cas_evals.cli", str(ROOT / "benchmarks/v0.1/golden.json"), "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(output.read_text())["summary"]["failed"], 0)


if __name__ == "__main__":
    unittest.main()
