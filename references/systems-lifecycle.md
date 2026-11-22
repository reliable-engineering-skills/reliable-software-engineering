# Additional systems and lifecycle decisions

Read only the affected topic. These are conditional decisions and evidence, not a requirement to deploy every technology. Use [primary and maintainer sources](standards-sources.md).

## Data ownership and database behavior

Normalization expresses keys/dependencies and reduces update anomalies. Define the domain's functional dependencies before splitting tables. Deliberate denormalization, invoice snapshots, and reporting projections can serve different contracts; do not deduplicate away required transaction history. Verify representative create/update/delete constraints and reconciliation.

Soft deletion needs explicit visibility, uniqueness, relation, restoration, retention, and eventual-purge behavior. Check direct queries, exports, jobs, and tenant isolation. A deleted flag does not implement privacy erasure. Migrations preserve applied shared history; verify existing rows, compatibility, locking, duration, and recovery under the chosen engine.

Size connection pools across all processes/replicas against the server's capacity, with bounded acquire timeouts and cleanup. Check actual driver/pool mode and session-state behavior; do not let an old tenant's state leak through reused connections. Read replicas can lag and conflict with queries; choose where authoritative/read-after-write reads must go. Test lag/failure rather than assuming every replica is immediately current. Indexes need representative execution plans and write/storage cost, not automatic indexing of every column.

## Stateless services, routing, and scale

Stateless request handling means required durable state is not tied to one disposable instance, not that the application has no state. Choose state/session ownership and cross-instance behavior deliberately. Load balancers distribute work; readiness, draining, session requirements, backend capacity, and failure domains still matter. Horizontal scaling adds instances; vertical scaling adds capacity to an instance. Measure the actual bottleneck and budget before either.

Reverse proxies, API gateways, and CDNs are conditional routing/security/cache layers, not required architecture. Trust forwarded identity/client-address headers only from known controlled proxies, define TLS termination and hop trust, and enforce authorization at the trusted data/effect boundary. Check effective routes, timeout/body limits, cache isolation, and origin bypass paths. Rate limits need appropriate authenticated/anonymous keys, distributed behavior when relevant, response/retry semantics, and abuse considerations; one limit is not complete availability protection.

## Retries, failure containment, and shutdown

Use end-to-end deadlines and bounded dependency timeouts. Retry only suitable transient failures, with a capped attempt/time budget, backoff and jitter when useful, and idempotency before repeating sensitive effects. Avoid multiplying retries across layers or retrying a final validation/authorization rejection. A circuit breaker may limit repeated failing work, but requires a defined open/half-open recovery and safe fallback; do not add one by default.

Queues need durable receipt, retry/dead-letter handling, and duplicate-safe effects; concurrency does not guarantee ordering. Race conditions involve interleavings over shared state; verify invariants under competing work instead of merely adding a mutex.

On graceful shutdown stop admitting work, mark readiness appropriately, drain/cancel bounded in-flight work, release resources, and acknowledge only completed/durably accepted messages. Respect the runtime's termination deadline and test an actual interruption/restart. Keep liveness, readiness, startup checks, and external uptime probes distinct. A downstream outage should not cause an indiscriminate restart loop; a healthy process alone does not prove the user journey works.

## Observation, performance, and cost

Choose useful logs, metrics, traces, and profiles for the affected journey. Structured logs have stable fields and correlation while redacting secrets and minimizing personal data. Distributed tracing follows causal work; instrumentation, sampling, propagation, cardinality, and data exposure require deliberate choices. Error tracking groups actionable failures; uptime monitoring checks an externally meaningful path. Audit records serve accountability and need controlled retention/access and tamper resistance; ordinary log storage is not guaranteed immutable.

Monitoring measures meaningful service signals; alerting needs an actionable threshold/SLO, owner, and response. Do not add instrumentation frameworks or collect every event by default. Set performance budgets from actual requirements and representative measurements. Profile CPU, memory, I/O, allocation and retained resources as relevant; growth in one sample does not establish a memory leak. Use comparable repeated observations and check cleanup/subscriptions/timers/connections. Authorized load tests use representative data, operation mix, concurrency/rate, errors, tail latency and cost in an isolated environment; user count alone is insufficient.

Measure accepted task and service cost, including retries, background work, storage/egress, observability and verification where applicable. Do not infer savings from model names or instruction language alone.

## Delivery, configuration, and compatibility

Containers package runtime dependencies but are not a complete security boundary or a reason to adopt orchestration. CI/CD should run actual project checks and restrict tokens, events, artifacts and deployment permissions. Infrastructure as Code needs a reviewed plan/diff, state protection, least privilege and drift awareness; generating a configuration does not authorize applying it. Staging should reflect consequential engine/configuration behavior while isolating production credentials/data/effects.

Follow project branching/review conventions; preserve others' work and verify the merged revision when shared boundaries change. Semantic Versioning requires a declared public API; version labels alone do not prove compatibility. Use feature flags only for an accepted rollout/product need, with safe defaults, audience/permission handling, owner and retirement trigger; do not create speculative switches. A flag is not an authorization check.

## Text, time, and diagnostic evidence

Character encoding maps text to bytes; Unicode code points and visible grapheme clusters are not interchangeable. Use the actual protocol/DB encoding, preserve intended round trips, and test supported scripts/emoji/RTL and length boundaries. Normalize only under an explicit contract, particularly for identifiers, signatures, passwords, and file paths.

Distinguish an instant, local civil time, a time zone, a duration, and a recurrence. Use current IANA time-zone data where applicable; a fixed UTC offset is not a complete time-zone rule. Decide storage/display and DST ambiguity/missing-time behavior; test scheduled work across transitions. Prefer appropriate monotonic clocks for elapsed durations, not wall-clock assumptions.

Read original error messages, stack traces, environment and exact inputs before proposing a cause. Reproduce a bounded failure, inspect the responsible code/version, and change the cause rather than suppressing the symptom. Verify documentation commands/options/examples against actual definitions. Never upload secrets or the entire repository just because a troubleshooting page requests it.
