"""Command-line interface for CAS Evals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluator import evaluate_suite
from .reference_product import DEFAULT_REFERENCE_PRODUCT_URL, ReferenceProductError, evaluate_reference_suite


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic CAS evaluations")
    parser.add_argument("fixture", type=Path, help="Benchmark fixture JSON")
    parser.add_argument("--output", type=Path, help="Write result JSON")
    parser.add_argument(
        "--reference-product-url",
        nargs="?",
        const=DEFAULT_REFERENCE_PRODUCT_URL,
        help="Opt in to evaluating actual output from the local reference-product endpoint",
    )
    parser.add_argument("--timeout-seconds", type=float, default=5.0, help="Live adapter HTTP timeout")
    args = parser.parse_args()

    try:
        result = (
            evaluate_reference_suite(
                args.fixture,
                endpoint=args.reference_product_url,
                timeout_seconds=args.timeout_seconds,
            )
            if args.reference_product_url
            else evaluate_suite(args.fixture)
        )
    except ReferenceProductError as error:
        parser.error(str(error))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 1 if result["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
