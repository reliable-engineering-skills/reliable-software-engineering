# Verification, performance, and interfaces

## Tests and review without false confidence

### Match checks to risk

| Change | Proportionate evidence |
| --- | --- |
| Low-impact text/spacing | Affected preview and quick checks when useful; no new suite just to increase counts. |
| Calculation or business condition | Independent acceptance examples, boundaries, invalid inputs, and deterministic checks. |
| Query or migration | Adopted engine, representative data/constraints, and migration checks. |
| Permissions or tenancy | Allowed/denied actors, direct access, and changed owner/ID. |
| Payments or inventory | Concurrency, duplicates, partial failure, unknown outcomes, and reconciliation. |
| External integration | Contract/sandbox verification when available; failure, delay, and unexpected responses. |
| Worker or cron | Bounded actual execution, restart, failed job, and metrics. |
| Refactoring | Behavior/contract checks and review of new boundaries. |

Not every check applies to every task. Expand verification when results reveal a new failure/risk, not merely because more checks are possible.

### Detect superficial tests

Check whether the test invokes the intended code, asserts a meaningful outcome, and uses expected values independent of the bug. Inspect disabled tests, weakened assertions, mocks that guarantee success, and global configuration that conceals failures.

For a consequential behavioral defect, a representative case failing before the fix and passing after it is strong evidence. Changed requirements may justify changing a test with an explanation of the new contract. Do not forbid all test edits or silently edit tests to hide defects.

### Complementary evidence

- Code review exposes structure, responsibility/data leakage, and assumptions not exercised by tests.
- Unit tests check isolated rules but do not prove real integration behavior.
- Integration tests expose service, contract, and database differences.
- Journey checks exercise user flows and failure states.
- Dependency/architecture checks can prevent forbidden coupling without proving all design quality.
- Visual previews expose usability/responsiveness issues without establishing server security.

Human review can also fail. Its value is responsibility, expertise, and another perspective, not a ceremonial signature or equal manual reading of every generated file. Focus on the diff, impact boundaries, and critical paths.

### Honest verification report

Report check/command, environment, result, and limits. Distinguish executed, proposed, and unavailable checks. A previous revision's successful checks do not establish the current revision's behavior; rerun what the new change affects.

### Review affected tests and documentation

- Assert consumer behavior, outcomes, state, and consequential effects. Use real values/models where practical; introduce controlled substitutes at meaningful boundaries rather than every internal function.
- Parameterize similar inputs only when setup and contract actually match. Do not combine unrelated scenarios just to reduce files. Each test should detect a meaningful defect.
- Do not test only framework guarantees; test the project's use of them where configuration, schema, or security is at risk. A fake store cannot establish real-engine behavior when persistence is the subject.
- Do not remove past-incident protection merely to simplify tests. Move, replace, or retire it with evidence that the behavior was removed or equivalent protection remains.
- LLM application tests check contracts, state transitions, and untrusted inputs. Avoid pinning exact answers/prompts unless consumed as a system contract. Call/retry/audit counts are valid assertions when they represent real cost, reliability, or security requirements; do not ban them categorically.
- For affected documentation, verify claims against definitions/execution: commands/flags, API methods/fields, configuration keys/defaults, versions, examples, and links. Running an example or checking the definition is stronger than finding a name used elsewhere. Do not rewrite documentation to excuse a bug or create a new guide for every edit.
- Tie review findings to location, evidence, impact, and a proposed remedy. State what missing sources/environments prevent verifying. Reviewing instructions is not itself automated testing or independent review.

## Performance and scalability

### Measure the journey before adding infrastructure

Use a representative journey and data. Inspect request counts/payloads, database queries/plans, connections, memory, processing time, and errors. Distinguish client, server, provider, and network latency.

For repeated reward operations or one request per notification, trace the source before assuming duplication is wrong. Check lifecycle, subscriptions, retries, concurrency, and triggers; establish which repetition is unnecessary.

Do not load-test a magic '5,000 users.' Data volume, active users, request rate, and operation mix differ. Model the actual question and choose an authorized environment that protects live services.

### Cache and scheduling

When affected, read [async/cache contracts and verification](async-cache.md). That reference owns freshness, isolation, invalidation, failure, and checks; do not add cache infrastructure to satisfy a generic list.

## Interfaces and CSS

For a changed interface/theme/shared component, read [UI and CSS](ui-css.md). It owns visual-system inspection, tokens, states, responsive/accessibility behavior, and visual evidence. Check representative consumers of shared changes; do not turn a small edit into a general redesign.
