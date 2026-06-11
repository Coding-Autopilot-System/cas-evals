import json
import unittest
from pathlib import Path

from cas_evals.evaluator import evaluate_suite

ROOT = Path(__file__).parents[1]
GOLDEN_PATH = ROOT / "benchmarks/v0.2/golden.json"
ADVERSARIAL_PATH = ROOT / "benchmarks/v0.2/adversarial.json"


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        self.adversarial = json.loads(ADVERSARIAL_PATH.read_text(encoding="utf-8"))

    def test_case_ids_are_unique_across_corpus(self):
        cases = self.golden["cases"] + self.adversarial["cases"]
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))

    def test_golden_corpus_covers_representative_workflows(self):
        capabilities = {case["capability"] for case in self.golden["cases"]}
        self.assertEqual(
            capabilities,
            {"planning", "implementation", "debugging", "azure-identity", "foundry-agent", "evidence", "delivery", "contracts"},
        )

    def test_adversarial_corpus_covers_independent_safety_risks(self):
        capabilities = {case["capability"] for case in self.adversarial["cases"]}
        self.assertEqual(
            capabilities,
            {"secret-safety", "verification-safety", "repository-safety", "architecture-safety", "offline-safety", "metric-safety"},
        )

    def test_v02_suites_pass_all_mandatory_gates(self):
        for path in (GOLDEN_PATH, ADVERSARIAL_PATH):
            result = evaluate_suite(path)
            self.assertEqual(result["summary"]["failed"], 0)
            self.assertTrue(all(item["metrics"]["safety"]["passed"] for item in result["evidence"]))


if __name__ == "__main__":
    unittest.main()
