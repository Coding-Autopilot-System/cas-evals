# Contributing

Contributions must preserve deterministic, secretless execution.

1. Add or update reviewable fixtures.
2. Explain metric and threshold changes.
3. Run `python -m unittest discover -s tests -v`.
4. Run both benchmark suites through the CLI.
5. Do not include real secrets, customer data, or network-dependent tests.

Changes that alter result shape must update the schema and include compatibility notes.
