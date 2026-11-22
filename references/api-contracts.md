# API and server contract engineering

Use for new or changed HTTP routes, framework server actions, RPC/GraphQL operations, and event/webhook boundaries. Keep the existing protocol and architecture. A static page does not require an API; internal server-rendered code may call an application service directly while retaining trusted identity, authorization, and input checks.

## Establish the contract before implementation

Identify consumers and deployment coupling, operation ownership, input/output representations, permitted actors, side effects, and failure outcomes. Use the existing source of truth: HTTP OpenAPI where independent consumers benefit, an existing RPC/GraphQL schema, or the framework's typed contract for a single full-stack application. Prefer supported generation over a second hand-maintained specification. A generated type is not runtime validation.

For a new boundary, establish these relevant decisions in the existing task or schema. For a small change inspect only the affected contract and consumers; do not demand a full specification document.

| Concern | Decision to make |
| --- | --- |
| Input | Allowed path/query/body/header/event fields, types, formats, lengths, ranges, omitted vs null, dates/time zones, and monetary units/precision. |
| Identity and ownership | Trusted identity source, required role, resource owner, tenant context, and authorization for reads as well as writes. Client-provided IDs identify a request, not authority. |
| Output | Explicit public fields and representation, excluding privileged/internal model data. Avoid exposing storage models directly when their shape includes private fields. |
| Errors | Existing protocol-appropriate statuses and stable machine-readable codes with safe messages and field details where useful. Distinguish failures without leaking resource existence, secrets, queries, or stack traces. |
| Work bounds | Payload/upload/list limits, allowed filters and sorting, pagination suited to data, timeouts, and abuse/resource limits appropriate to exposure. |
| Mutation | Atomicity, conflicts, final/unknown states, concurrency, idempotency identity and payload rules where repeating an effect is sensitive. |
| Compatibility | Existing consumers, additive changes, and migration/deprecation/versioning only when a breaking change needs it. Do not version every internal endpoint automatically. |

## Implement in the existing structure

Validate untrusted values at the trusted boundary with the project's runtime validation mechanism, then invoke the owned business operation. Reuse business behavior across routes, jobs, server actions, and webhooks rather than duplicating rules. Apply explicit writable fields to prevent clients assigning privilege or ownership fields. Compile-time types and a hidden UI control provide no security boundary.

Enforce authorization where data and effects are accessed, including direct service entry paths. Keep credentials and private decisions server-side. For browser APIs use the applicable origin/session/CSRF mechanisms; CORS does not authorize a caller. Use the established secure transport configuration outside local development.

Do not treat a submitted mutation's timeout as a confirmed failure. Reconcile unknown outcomes or retry only under a suitable idempotency contract. Read [data and payments](data-payments.md) for sensitive effects and [security](security.md) for ownership and tool/data boundaries.

When persistence changes, use the established migration mechanism. Preserve already-applied shared migrations; add a new migration for a further change. Verify old data, compatibility during rollout, and a data-safe forward fix or restoration path where rollback is inadequate. Execution in a shared or production environment still follows authorization.

## Integrate consumers

Use the existing API client or generated contracts, with one appropriate owner for base URLs and environment configuration. Handle the relevant empty/loading, invalid-input, expired-session, forbidden, conflict, timeout, and server-error outcomes. Ignore obsolete read results without confusing client cancellation with rollback of a server write. Keep sensitive calculations and entitlement decisions at a trusted server boundary.

Mocks or local adapters must be identified as simulations. Missing credentials do not justify replacing a protected live integration with hard-coded success, weakening its checks, or restructuring it solely to make a demo pass. Continue independent authorized work and distinguish local readiness, sandbox verification, and live activation. Follow real dependencies; do not postpone the integration when it is the user's current target.

## Contract evidence

Exercise the real affected handler/service boundary with a valid request and relevant malformed, forbidden, wrong-owner/tenant, and safe-error cases. Assert returned fields and absence of forbidden state changes, not just status 200. Add old-consumer compatibility, duplicate/conflict/concurrency, persistence, or migration cases when affected. Keep test environments separate from live providers and distinguish fakes from provider verification.

Use [async/cache controls](async-cache.md) when changing scheduling, caching, or freshness. A schema match, generated client, or mock response alone does not establish a working integration.
