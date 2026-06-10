# Pitfalls Research

| Pitfall | Warning Sign | Prevention |
|---------|--------------|------------|
| Non-deterministic scoring | Same commit produces different scores | Pure functions, fixed arithmetic, fixture hashes |
| Metric gaming | Aggregate score hides unsafe behavior | Safety is an independent mandatory gate |
| Opaque results | Score lacks reasons or provenance | Emit metric details, thresholds, evaluator version, fixture digest |
| Unrealistic benchmarks | Only happy paths pass | Include adversarial prompts and explicit unsafe expected outcomes |
| Cost ambiguity | Provider pricing changes silently alter results | Fixture-supplied normalized cost inputs in v0.1 |
