# Requirements and architectural decisions

## Establish the task contract before coding

### Gather the minimum information that changes the decision

Answer from available files and evidence first:

- What problem is being solved, and for whom? What is the current and accepted behavior?
- Is this a prototype, internal tool, or public service with real data?
- What data exists, who owns it, and does it include money, sensitive information, or multiple tenants?
- What versions, database engine, hosting environment, and deployment process are in use?
- What usage, concurrency, and data volume are expected? Which values are measured and which estimated?
- Which API, file, data, integration, and user-experience contracts must remain compatible?
- What are the acceptance criteria, relevant checks, and authorization boundaries?

Do not stop a clear task over an immaterial missing detail. Use a stated, reversible assumption. Do not silently guess when a decision risks real data or changes an external contract.

### Convert broad language into verifiable behavior

| Broad request | Verifiable engineering interpretation |
| --- | --- |
| Make the website fast | Identify a journey, representative data, expected load, and an agreed response-time target. |
| Secure the dashboard | Define roles, resources, operations, and isolation; test allowed and denied access. |
| Fix payments | Define states/transitions, provider confirmation, duplicate handling, and reconciliation. |
| Clean up the project | Identify a module, maintenance problem, and outcome while preserving agreed behavior. |
| Save tokens | Compare accepted task completion cost, including retries and review. |
| Test everything | Select risk-bearing journeys and affected integrations; a large test count is not a test plan. |

### Establish invariants

Examples: one company's user cannot access another company's report; the same event cannot grant a reward twice; allocated inventory cannot exceed availability; today's price cannot change yesterday's invoice.

These are business invariants, not incidental implementation details. Check them in design, code, and relevant tests. Do not infer a requirement solely from a screen's appearance.

## Choose technology and architecture

### Decision order

1. Reuse the adopted technology when it meets requirements.
2. Identify an actual limitation before proposing replacement.
3. Compare the smallest useful set of alternatives using data correctness, operation, team experience, cost, licensing, support, and transition effort.
4. Record the reason for the choice and the condition that would justify revisiting it.
5. Run the smallest experiment that resolves a consequential uncertainty; do not build an entire system to test a small assumption.

### Conditional options

| Option | Appropriate when | Verify |
| --- | --- | --- |
| Modular monolith | Business boundaries fit one deployment and a small or medium team. | Responsibility boundaries, cycles, and scattered business rules. |
| Independent service | Deployment, ownership, load, or requirements need isolation. | Network cost, partial failure, identity, observability, and consistency. |
| SQLite | Storage, writes, distribution, and operation suit its capabilities. | Write concurrency, durable storage, backups, and deployment constraints. |
| Server database such as PostgreSQL or MySQL | Central access, multiple processes, or engine requirements justify it. | Configuration, capacity, transactions, indexes, compatibility, and migration. |
| Synchronous operation | Work is short/bounded and its result is required for the response. | Timeout, provider failure, and retry effects. |
| Job queue | Work is long, needs retries, or should outlive the request. | Durability, duplicate delivery, workers, monitoring, and recovery. |
| Cache | Repeated load and a performance goal justify the complexity. | Invalidation, staleness, isolation keys, and sensitive data. |
| New index | A measured query benefits. | Execution plan, write cost, and storage. |
| Rewrite | Bounded changes cannot address the limitations at acceptable cost. | Behavior, historical data, compatibility, coexistence, and project failure/recovery. |

Docker, Kubernetes, or a new language does not automatically demonstrate maturity. Select them for operational requirements and team capacity. Do not impose Next.js because the source mentioned it; page type, interaction, indexing, experience, and hosting determine the choice.

### Internal boundaries

For a conventional web application, adapt these responsibilities to its existing framework:

- Input: shape validation, context, authentication, dispatch, and response translation.
- Business behavior: rules, invariants, and state transitions with clear transaction boundaries.
- Data access and integrations: persistence and provider-specific details.
- Presentation: data and loading/empty/error states; the UI is not authoritative for permissions or financial calculations.

Do not add a layer for every line. Simple formatting in a controller is not inherently wrong; entangled rules that are hard to understand, test, or change are the problem.

### Reuse without forced abstraction

Before adding a function or component:

1. Search names, concepts, callers, and tests, not only the proposed new name.
2. Inspect existing contracts, assumptions, and side effects.
3. Reuse matching meaning, or extend the contract compatibly when appropriate.
4. Keep different meanings independent and explain misleading similarity when needed.

The source's pagination example suggests sharing a component or contract when appropriate, not a generic function with dozens of options coupling unrelated flows.

### Server contracts and data-related performance

For new or changed APIs/server actions, read [API contracts](api-contracts.md). For affected scheduling or caching, read [async and cache lifecycle](async-cache.md). These references own the details; do not impose OpenAPI, a separate API, or a cache service on an application that does not need them.


For requested multi-session task decomposition, use the `rse-task-packs` skill with the existing specification system. Do not create an execution pack for every small edit.
