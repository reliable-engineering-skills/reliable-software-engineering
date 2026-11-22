# Async scheduling, progressive results, and cache lifecycle

Use only for new or changed async dependencies, section loading, caching/freshness, or a measured bottleneck. Do not parallelize an existing ordered flow during a behavior-preserving refactor without a separately justified behavior/performance change.

## Dependency-aware scheduling

Identify real prerequisites and the point where each result can be consumed. Preserve identity/authorization prerequisites, dependent lookups, transaction rules, and required ordering. Start safe independent I/O without unnecessary serialization; apply a resource/concurrency bound for large or user-controlled collections using existing batching/pooling mechanisms.

For JavaScript/TypeScript, `Promise.all` fits a bounded independent group needed at one consumption point when any rejection should fail that group. Start operations and pass their promises; passing already-awaited results does not overlap work. Rejecting the group does not cancel other operations, whose failures and effects must still be accounted for.

Use `Promise.allSettled` when the consumer needs all outcomes; it also waits for every operation. Independently useful UI sections can resolve at separate boundaries instead of waiting behind either aggregate. Use the framework's current loading/streaming/error mechanisms; do not add a new architecture for this rule. Concurrent I/O does not parallelize synchronous CPU work.

Observe every started operation. Removing `await` must not silently lose a required write or report premature success. Deferred work requires a suitable lifetime and durable execution mechanism when delivery matters. Preserve timeouts, safe cancellation, retries, and idempotency. See [UI and CSS](ui-css.md) for scoped rendering and feedback.

## Decide freshness before adding cache

Inspect relevant caches already present: client/query state, framework routes/server memory, browser/HTTP/CDN, and shared/distributed storage. An application can cache without explicit cache code. Check actual version/configuration when defaults matter. Skip cache discovery for an unrelated small edit.

Determine authoritative data, public/user/tenant scope, acceptable display staleness, read/write patterns, and required read-after-write behavior. Resolve consequential missing product/privacy requirements; do not ask the user to choose Redis or invent a universal TTL. An outcome of 'existing cache sufficient' or 'no cache needed' is valid.

## Cache contract

- **Ownership and placement:** use the existing appropriate layer. Do not stack caches or add a service by default. Identify source of truth, exclusions, owner, expiry/size bounds, and permitted failure behavior.
- **Keys and isolation:** include representation/query, locale/version, and trusted identity/tenant/permission scope where relevant. A cache hit does not grant access. Minimize personal data in keys and logs.
- **HTTP storage:** inspect effective framework, browser, and shared-cache policy for authenticated/private responses. `no-cache` permits storage with revalidation; it is not `no-store`. Changing headers does not demonstrate that old stored copies have been purged.
- **Invalidation:** include item/list/aggregate effects after successful authoritative writes, jobs/webhooks, deletion, logout, account switch, and permission changes where relevant. Address refill/invalidation races and missed updates when correctness depends on them. Avoid a broad production flush as routine repair.
- **Freshness:** TTL bounds age, not equality with latest state. Stale/offline or negative caching requires a compatible product contract. Do not relabel failure as success or use cached displays alone for final price, stock, balance, entitlement, or permission decisions.
- **Failure and load:** define bounded fallback and recovery. If neither safely current data nor explicitly permitted stale data is available, surface a clear error/pending state. Protect the source from concurrent refill storms with existing deduplication, batching, or locking when justified.
- **Client lifecycle:** invalidation and identity changes must prevent old-account data or obsolete reads from reappearing. Cache refresh should not block unrelated ready UI sections.

## Evidence

For scheduling changes, use controlled pending operations, request interception, or a timeline to verify overlap and real ordering. Delay/fail a secondary section and inspect essential content, local retries, cancellation, stale-result handling, and required side effects. Avoid a correctness test tied only to fixed milliseconds.

For cache changes, select relevant cold/warm, expiry, write-then-read, delete, invalidation/refill race, unavailable cache, and simultaneous-miss cases. Verify warm-hit and cold-miss isolation, permission revocation, and account/tenant switches. Use multiple instances when the design relies on their coherence. Configuration text or a high hit ratio is not proof of correctness.

Claim optimization only after comparable workload/data/environment measurements of useful content latency, tail latency, source load, errors, and resource cost as relevant, with data correctness preserved. State assumptions and unmet targets; do not fabricate performance commitments or load-test live systems outside authorization.
