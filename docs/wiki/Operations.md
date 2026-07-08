# Operations

## Setup and run

```powershell
python -m pip install -e .
python -m unittest discover -s tests -v
python -m cas_evals.cli benchmarks/v0.2/golden.json --output artifacts/golden.json
python -m cas_evals.cli benchmarks/v0.2/adversarial.json --output artifacts/adversarial.json
python -m cas_evals.release --check
```

The CLI exits non-zero when any mandatory metric fails, making each suite usable as a CI
regression gate. Windows users can run the complete verification path with
`.\scripts\verify.ps1`.

## Live reference-product mode (opt-in)

```powershell
python -m cas_evals.cli benchmarks/reference-product/v0.1/golden.json --reference-product-url
python -m cas_evals.cli benchmarks/reference-product/v0.1/adversarial.json --reference-product-url
```

## CI (`.github/workflows/ci.yml`, matrix: ubuntu-latest + windows-latest, Python 3.11 + 3.13, 10-minute timeout)

1. `actions/checkout` (pinned to commit SHA)
2. `actions/setup-python` (pinned to commit SHA)
3. `python -m pip install -e .`
4. `python -m unittest discover -s tests -v`
5. `python -m unittest discover -s tests -p test_reference_product.py -v`
6. `python -m cas_evals.cli benchmarks/v0.2/golden.json`
7. `python -m cas_evals.cli benchmarks/v0.2/adversarial.json`
8. `python -m cas_evals.release --check` — the CLI-exit-code gate; **not** a coverage badge,
   since no formal coverage-percentage gate exists in this repo.

A separate `.github/workflows/codeql.yml` runs CodeQL analysis, and `.github/workflows/
pages.yml` publishes documentation (badges in the root `README.md`). A registry-fetch smoke
check (live HTTP verification of the Pages registry) is in progress — see
[Architecture](./Architecture.md) and PR #9.

<!-- docs-verified: 4fe936cc83ffdc4fd6ad825c373e949b1edbe0eb 2026-07-08 -->
