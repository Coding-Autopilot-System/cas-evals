"""Command-line interface for CAS Evals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluator import evaluate_suite


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic CAS evaluations")
    parser.add_argument("fixture", type=Path, help="Benchmark fixture JSON")
    parser.add_argument("--output", type=Path, help="Write result JSON")
    args = parser.parse_args()

    result = evaluate_suite(args.fixture)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 1 if result["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
