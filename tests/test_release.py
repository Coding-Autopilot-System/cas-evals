import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from cas_evals.contracts import validate_evaluation_result
from cas_evals.release import RELEASE_VERSION, generate_release, verify_release

ROOT = Path(__file__).parents[1]
RELEASE_DIR = ROOT / "releases" / RELEASE_VERSION


class ReleaseTests(unittest.TestCase):
    def test_checked_in_release_is_byte_reproducible(self):
        verify_release(RELEASE_DIR)

    def test_manifest_digests_match_artifacts_and_fixtures(self):
        manifest = json.loads((RELEASE_DIR / "manifest.json").read_text(encoding="utf-8"))
        for suite in manifest["suites"]:
            artifact = RELEASE_DIR / suite["artifact"]
            fixture = ROOT / suite["fixture"]
            self.assertEqual(suite["artifactDigest"], f"sha256:{hashlib.sha256(artifact.read_bytes()).hexdigest()}")
            self.assertEqual(suite["fixtureDigest"], f"sha256:{hashlib.sha256(fixture.read_bytes()).hexdigest()}")

    def test_release_results_use_shared_contract(self):
        for path in RELEASE_DIR.glob("*-results.json"):
            suite = json.loads(path.read_text(encoding="utf-8"))
            for result in suite["results"]:
                validate_evaluation_result(result)

    def test_generation_writes_only_expected_json_files(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = generate_release(Path(directory))
            self.assertEqual([path.name for path in paths], ["adversarial-results.json", "golden-results.json", "manifest.json"])


if __name__ == "__main__":
    unittest.main()
