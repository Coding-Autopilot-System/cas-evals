[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot

try {
    python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw "Unit tests failed." }

    python -m cas_evals.cli benchmarks/v0.1/golden.json --output artifacts/golden.json
    if ($LASTEXITCODE -ne 0) { throw "Golden benchmark failed." }

    python -m cas_evals.cli benchmarks/v0.1/adversarial.json --output artifacts/adversarial.json
    if ($LASTEXITCODE -ne 0) { throw "Adversarial benchmark failed." }
}
finally {
    Pop-Location
}
