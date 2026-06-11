import copy
import unittest

from cas_evals.contracts import ContractValidationError, validate_evaluation_result, verify_vendored_contract
from cas_evals.evaluator import evaluate_suite

from pathlib import Path

ROOT = Path(__file__).parents[1]


class SharedContractTests(unittest.TestCase):
    def setUp(self):
        self.result = evaluate_suite(ROOT / "benchmarks/v0.1/golden.json")["results"][0]

    def test_vendored_contract_provenance_is_valid(self):
        provenance = verify_vendored_contract()
        self.assertEqual(provenance["tag"], "v0.1.0")
        self.assertEqual(len(provenance["schemas"]), 2)

    def test_emitted_result_validates(self):
        validate_evaluation_result(self.result)

    def test_missing_shared_field_fails_closed(self):
        invalid = copy.deepcopy(self.result)
        del invalid["traceContext"]
        with self.assertRaises(ContractValidationError):
            validate_evaluation_result(invalid)

    def test_unevaluated_field_fails_closed(self):
        invalid = copy.deepcopy(self.result)
        invalid["localDetails"] = {}
        with self.assertRaises(ContractValidationError):
            validate_evaluation_result(invalid)

    def test_invalid_numeric_metric_fails_closed(self):
        invalid = copy.deepcopy(self.result)
        invalid["metrics"]["quality"] = True
        with self.assertRaises(ContractValidationError):
            validate_evaluation_result(invalid)


if __name__ == "__main__":
    unittest.main()
