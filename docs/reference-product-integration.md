# CAS Reference Product Integration

CAS Evals includes an opt-in deterministic adapter for the local
`cas-reference-product` `POST /api/v1/workflows` endpoint. The existing offline
evaluator remains the default and never requires a service, network access, or
secrets.

## Run The Golden Path

Start `cas-reference-product` in local mode from its own repository:

```powershell
.\scripts\run-local.ps1
```

Then run both reference-product corpora from `cas-evals`:

```powershell
python -m cas_evals.cli benchmarks/reference-product/v0.1/golden.json `
  --reference-product-url `
  --output artifacts/reference-product-golden.json

python -m cas_evals.cli benchmarks/reference-product/v0.1/adversarial.json `
  --reference-product-url `
  --output artifacts/reference-product-adversarial.json
```

Pass an explicit URL after `--reference-product-url` when the endpoint is not
`http://127.0.0.1:8080/api/v1/workflows`.

## Evidence Guarantees

For every case, the adapter:

- creates deterministic `correlationId`, `promptId`, `runId`, and W3C trace context;
- requires every returned lifecycle event to preserve those values;
- evaluates the actual returned `output`, not the fixture's reference response;
- records the source fixture digest and returned-output digest;
- removes server timestamps and endpoint-specific addresses from persisted evidence;
- uses fixture-observed normalized latency so identical service output produces byte-identical evidence.

The adapter fails closed for unavailable endpoints, invalid JSON, oversized
responses, empty outputs, invalid response shapes, or lifecycle metadata drift.
The HTTP timeout controls transport behavior but is not written into evidence.

## CI Boundary

CI runs the adapter contract against a local deterministic HTTP server. This
proves the executable HTTP path on Windows and Linux without coupling the
offline repository to another checkout or a hosted service. The full sibling
repository golden path is an explicit local integration check.
