# Architecture & Design

This document describes the architectural logic and data flow of **CAS Evals**.

## Core Logic

CAS Evals is built around a deterministic evaluation pipeline that evaluates LLM-generated responses against expected baselines. It supports two distinct execution paths:

1.  **Offline Mode (Default):** Evaluates pre-recorded fixture data directly. It is completely offline, ensuring maximum reproducibility.
2.  **Live Reference Product Mode:** Opt-in mode using the `--reference-product-url` flag. It posts a `PromptEnvelope` to a live, local HTTP endpoint (`cas-reference-product`), extracts the dynamic output, and runs it through the same deterministic evaluation pipeline.

### Evaluation Criteria

For each case, CAS Evals enforces strict gating rules:
- **Quality:** Fraction of expected keyword concepts present in the response versus a configured minimum threshold.
- **Safety:** Absence of prohibited unsafe content (requires a 100% pass rate).
- **Cost:** Cost in USD validated against a configured maximum threshold.
- **Latency:** Duration in milliseconds validated against a configured maximum threshold.

Any threshold violation fails the case, resulting in a failed suite.

### Schema Contracts and Evidence

Every per-case result generates an `EvaluationResult` conforming to the pinned `cas-contracts` version. The evidence payload includes:
- SHA-256 fixture digests to guarantee immutability.
- Strict lifecycle metadata (e.g., `correlationId`, `traceContext`) that must be preserved by live reference products.
- Granular metric results (`value`, `threshold`, `passed`, `details`).

## System Architecture Diagram

The following Mermaid diagram visualizes the evaluation pipeline across both offline and live modes.

```mermaid
flowchart TD
    %% CLI and Input
    CLI[cas_evals.cli]
    FixtureJSON[("Fixture JSON\n(e.g., golden.json)")]

    CLI -->|Parses| FixtureJSON
    FixtureJSON -->|Yields Suite & Cases| Router{Live Mode\nEnabled?}

    %% Branch: Offline vs Live
    Router -- "No (--output)" --> OfflineEv[Offline Evaluator\nevaluator.py]
    Router -- "Yes (--reference-product-url)" --> LiveRef[Reference Product Adapter\nreference_product.py]

    %% Live Reference Product Flow
    subgraph Live Reference Product Adapter
        LiveRef --> BuildEnv[Build PromptEnvelope]
        BuildEnv --> HTTPPost[HTTP POST\n/api/v1/workflows]
        HTTPPost --> HTTPResp[Extract Response & Events]
        HTTPResp --> ValidateMeta{Validate Lifecycle\nEvents/Metadata}
        ValidateMeta -- Invalid --> RefError((ReferenceProductError))
        ValidateMeta -- Valid --> LiveCase[Inject live 'output'\nas 'response']
    end
    
    LiveCase --> SharedEval

    %% Offline Flow
    OfflineEv --> SharedEval[Shared Core Evaluator\n_evaluate_case_with_evidence]

    %% Core Evaluation Logic
    subgraph Evaluation Pipeline
        SharedEval --> MetricQ[Calculate Quality\n(expected keywords)]
        SharedEval --> MetricS[Calculate Safety\n(prohibited words)]
        SharedEval --> MetricC[Extract Cost\n(observed USD vs limits)]
        SharedEval --> MetricL[Extract Latency\n(observed ms vs limits)]
        
        MetricQ --> Agg[Aggregate Evidence]
        MetricS --> Agg
        MetricC --> Agg
        MetricL --> Agg
        
        Agg --> ValidateContract[Validate EvaluationResult Schema]
    end

    %% Output
    ValidateContract --> PassFail{Passed\nAll Metrics?}
    PassFail -- Yes --> Success((Suite Pass))
    PassFail -- No --> Fail((Suite Fail))

    %% Contract references
    casContracts[("cas-contracts\nvendor/cas-contracts/")] -.-> ValidateContract

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef error fill:#ffe6e6,stroke:#cc0000;
    classDef success fill:#e6ffe6,stroke:#006600;
    class RefError,Fail error;
    class Success success;
```

## Module Responsibilities

- **`cli.py`:** Parses arguments, loads the fixture suite, handles top-level error formatting, and writes JSON results to `stdout` and/or the `--output` file.
- **`evaluator.py`:** Contains the pure evaluation kernel (`_evaluate_case_with_evidence`), responsible for scoring quality, safety, and validating cost/latency against thresholds. Forms the standard `EvaluationResult`.
- **`reference_product.py`:** Contains the HTTP transport and metadata validation logic for live endpoint evaluations. It wraps the core evaluator by providing it with dynamic responses instead of fixture responses.
- **`contracts.py`:** Integrates the pinned `cas-contracts` JSON schemas from `vendor/cas-contracts/` to ensure offline validation of all evidence.
