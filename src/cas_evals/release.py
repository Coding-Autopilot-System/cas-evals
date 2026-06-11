"""Deterministic benchmark release artifact generation."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from .contracts import PROVENANCE_PATH, verify_vendored_contract
from .evaluator import EVALUATOR_VERSION, evaluate_suite

ROOT = Path(__file__).parents[2]
RELEASE_VERSION = "v0.2.0"
RELEASED_AT = "2026-06-11T12:00:00Z"
SUITES = {
    "golden": ROOT / "benchmarks" / "v0.2" / "golden.json",
    "adversarial": ROOT / "benchmarks" / "v0.2" / "adversarial.json",
}


def _payload(value: dict) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _digest(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def generate_release(output_dir: Path) -> list[Path]:
    """Generate deterministic release files and return their paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    provenance = verify_vendored_contract()
    suite_entries = []
    written = []

    for name, fixture_path in SUITES.items():
        result = evaluate_suite(fixture_path)
        result_bytes = _payload(result)
        artifact_name = f"{name}-results.json"
        artifact_path = output_dir / artifact_name
        artifact_path.write_bytes(result_bytes)
        written.append(artifact_path)
        suite_entries.append(
            {
                "artifact": artifact_name,
                "artifactDigest": _digest(result_bytes),
                "fixture": fixture_path.relative_to(ROOT).as_posix(),
                "fixtureDigest": _digest(fixture_path.read_bytes()),
                "suiteId": result["suiteId"],
                "summary": result["summary"],
            }
        )

    manifest = {
        "releaseVersion": RELEASE_VERSION,
        "releasedAt": RELEASED_AT,
        "evaluator": f"cas-evals/{EVALUATOR_VERSION}",
        "sharedContract": {
            "repository": provenance["repository"],
            "release": provenance["release"],
            "tag": provenance["tag"],
            "provenanceDigest": _digest(PROVENANCE_PATH.read_bytes()),
        },
        "suites": suite_entries,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_bytes(_payload(manifest))
    written.append(manifest_path)
    return sorted(written)


def verify_release(release_dir: Path) -> None:
    """Raise when checked-in release artifacts differ from fresh generation."""
    with tempfile.TemporaryDirectory() as directory:
        generated_dir = Path(directory)
        generated = generate_release(generated_dir)
        expected_names = {path.name for path in generated}
        actual_names = {path.name for path in release_dir.glob("*.json")}
        if actual_names != expected_names:
            raise ValueError(f"release file set mismatch: expected {sorted(expected_names)}, found {sorted(actual_names)}")
        for generated_path in generated:
            checked_in = release_dir / generated_path.name
            if checked_in.read_bytes() != generated_path.read_bytes():
                raise ValueError(f"release artifact is not reproducible: {checked_in}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or verify deterministic CAS benchmark release artifacts")
    parser.add_argument("--output", type=Path, default=ROOT / "releases" / RELEASE_VERSION)
    parser.add_argument("--check", action="store_true", help="Verify checked-in artifacts without changing them")
    args = parser.parse_args()

    if args.check:
        verify_release(args.output)
        print(f"Verified deterministic release artifacts in {args.output}")
    else:
        for path in generate_release(args.output):
            print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
