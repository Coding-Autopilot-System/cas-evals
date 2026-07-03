# CAS Evals Developer Documentation

Welcome to the developer documentation for **CAS Evals**, the reproducible evaluation framework for the [Coding Autopilot System](https://github.com/Coding-Autopilot-System).

## Overview

CAS Evals provides a deterministic, offline-first evaluation kernel for assessing AI engineering claims. It runs versioned golden tasks and adversarial prompts against reference responses, producing machine-readable evidence for quality, safety, cost, and latency. 

By eliminating the need for secrets, model-provider accounts, or network access in its default mode, CAS Evals ensures that benchmark inputs, thresholds, scoring logic, fixture digests, and pass/fail decisions are fully reviewable and reproducible.

## Key Principles

- **Deterministic & Offline-First:** Default test runs use pre-recorded responses. No network connectivity or live LLM calls are required to reproduce the baseline.
- **Traceable:** Every evaluation result conforms to the published `cas-contracts` schema (`EvaluationResult`). Execution evidence includes SHA-256 fixture digests and robust lifecycle metadata.
- **Strict Verification:** Evals rigorously checks for expected concepts (Quality), absence of prohibited content (Safety), and verifies cost and latency limits. Any failure in mandatory metrics fails the entire suite.
- **Opt-in Live Integration:** Seamlessly evaluate live workflow outputs via the local `cas-reference-product` endpoint while enforcing metadata preservation.

## Getting Started

### Local Setup
Ensure you have Python 3.11+ installed. Install the package in editable mode:
```powershell
python -m pip install -e .
python -m unittest discover -s tests -v
```

### Running Evaluations

Run an offline evaluation using a benchmark fixture:
```powershell
python -m cas_evals.cli benchmarks/v0.2/golden.json --output artifacts/golden.json
```

Evaluate a live workflow using the reference product adapter:
```powershell
python -m cas_evals.cli benchmarks/reference-product/v0.1/golden.json --reference-product-url
```

## Documentation Map

- **[Architecture & Design](architecture.md):** Deep dive into the evaluation workflow, live adapter logic, and see the system architecture diagram.
- **[Reference Product Integration](reference-product-integration.md):** Learn how to integrate and validate live workflows.
- **[Benchmark Reports]:** Review the checked-in, reproducible public baselines (e.g., [v0.2](benchmark-report-v0.2.md)).

## Contributing

See our [CONTRIBUTING.md](../CONTRIBUTING.md) guide for instructions on how to submit changes, run tests, and adhere to our development standards. Security concerns should be reported according to [SECURITY.md](../SECURITY.md).
