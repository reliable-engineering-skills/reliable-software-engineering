# Common engineering misconceptions

Use when a request, review comment or plan rests on one of these generalizations. Each row replaces a slogan with a checkable criterion; none is a mandate.

| Impression | Problem | Corrected guidance |
| --- | --- | --- |
| Tools always fail at security/performance/maintenance. | Unsupported generalization; people and tools both err. | Verify these properties regardless of code origin. |
| Every generated line is vulnerable until proven otherwise. | Caution does not establish a vulnerability. | Treat changes as unverified; investigate without inventing diagnoses. |
| 100% security or accuracy. | A bounded review cannot establish absence of every defect. | State controls, residual risk, and verification limits. |
| Good appearance or scanner grade A proves safety. | A scan may cover only HTTP headers/TLS. | Read scope and add authorization/business-rule verification. |
| SQLite is only for local development. | Valid production uses exist. | Decide from concurrency, writes, operation, and distribution. |
| Every serious project needs Redis/a queue. | Unjustified complexity. | Add dependencies for demonstrated requirements/bottlenecks with an operational plan. |
| A service means a microservice. | In-process responsibilities differ from independent deployments. | Specify whether it is an internal module or distributed service. |
| A monolith means spaghetti code. | Deployment shape does not determine boundary quality. | A modular monolith can be suitable; split deployment for a reason. |
| Put all logic in a new service layer. | Can relocate disorder or create ceremonial layers. | Own rules clearly within the existing architecture. |
| Never use Flexbox/Grid. | A particular experience became a universal ban. | Choose suitable layout, spacing, responsiveness, and semantics. |
| More than 400 characters/6,000 lines proves collapse. | No magic quality threshold. | Inspect complexity, responsibilities, dependencies, and change difficulty. |
| Merge every duplicate into one function. | Similar shape may represent different meanings. | Share matching logic; retain independent rules where appropriate. |
| Never start a new chat. | A long session is not reliable memory. | Start one when useful with a concise handoff and code-state references. |
| Lost in the Middle means always forgetting the entire middle. | The study examines particular models/tasks. | Test relevant recall and do not rely on text position alone. |
| Agent files permanently train the model. | Instructions/external memory differ from weight training. | Describe saved guidance and verify later sessions can access it. |
| Two models guarantee correct independent review. | They can share assumptions/errors. | Vary the inspection and require evidence beyond model opinion. |
| A model cannot criticize its own code. | It can find defects, but that is insufficient alone. | Use self-review as supporting evidence, not certification. |
| On failure the model intentionally fabricates tests to deceive. | Behavior does not establish intent/a unique explanation. | Inspect test changes, configuration, mocks, and assertions. |
| Grounding/links eliminate hallucination. | Sources may not support claims or may target another version. | Read originals, check applicability/version, and run relevant examples. |
| Technical debt does not exist, or must all be fixed now. | Ignores impact, tradeoffs, and transition cost. | Prevent critical defects and track accepted debt with ownership/revisit criteria. |
| Refactoring means rebuilding the entire system. | Refactoring normally preserves behavior through smaller transformations. | Separate structure, changed requirements, and rewrites. |
| Connect a parallel environment to production with a bridge. | The name does not isolate data/side effects. | Use protected data, isolated copies, separate permissions, and explicit transfer design. |
| Passing tests permits an immediate full replacement. | Schema, historical data, and load can change. | Use risk-appropriate rollout, monitoring, and demonstrated recovery. |
| Updating a product price is always wrong. | Current prices may change if transaction history remains valid. | Snapshot invoices/orders and version subscriptions when required. |
| Timeout means payment failure. | The provider may have completed the effect. | Record pending/unknown and verify before repeating it. |
| Webhooks alone guarantee idempotency. | Delivery does not prevent duplicate processing. | Stable operation identity, persisted states, uniqueness, and safe retries. |

Passkeys may synchronize; two-factor authentication uses distinct factors; stateless services can use external state; cookie flags have limited distinct guarantees; idempotency requires the actual operation contract; soft deletion is not erasure; and audit logging is not automatically immutable. Privacy applicability and conformance require actual system evidence and requirements.

Supporting sources: [SQLite usage guidance](https://sqlite.org/whentouse.html), [Martin Fowler: Monolith First](https://martinfowler.com/bliki/MonolithFirst.html), [Refactoring](https://refactoring.com/), [Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html).
