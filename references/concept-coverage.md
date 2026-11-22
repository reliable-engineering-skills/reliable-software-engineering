# Engineering concept coverage

Use this as a lookup for the supplied terminology, not a required checklist or a vocabulary to insert into every answer. All 109 unique input terms have a conditional application and evidence criterion. Read the linked owner and only relevant source sections.

Primary control standards and protocols differ from vendor-specific behavior and practitioner guidance; see [source authority](standards-sources.md). No technology, security feature, abstraction or test layer is mandatory merely because it appears here.

## Backend engineering

| Concept | Application / evidence | Owner | Sources |
| --- | --- | --- | --- |
| Authentication | Verify the trusted actor with the adopted provider and test failed authentication. | [security-controls.md](security-controls.md) | [S04](standards-sources.md#s04), [S08](standards-sources.md#s08) |
| Authorization | Enforce actor/resource/tenant permissions at every trusted access path. | [security-controls.md](security-controls.md) | [S03](standards-sources.md#s03) |
| Session Management | Check rotation, expiry, revocation and session-store ownership. | [security-controls.md](security-controls.md) | [S05](standards-sources.md#s05) |
| Two-Factor Authentication (2FA) | Require distinct factors and protect recovery; two knowledge checks are not two factors. | [security-controls.md](security-controls.md) | [S08](standards-sources.md#s08) |
| Input Validation | Allowlist fields/types/bounds at untrusted boundaries and test rejection. | [api-contracts.md](api-contracts.md) | [S03](standards-sources.md#s03) |
| Data Validation on the Server | Server checks are authoritative; UI checks/static types are insufficient. | [security-controls.md](security-controls.md) | [S03](standards-sources.md#s03) |
| HTTP Status Codes | Use protocol semantics and safe stable errors, not 200 for every result. | [api-contracts.md](api-contracts.md) | [S12](standards-sources.md#s12) |
| Error Handling | Preserve failure meaning; recover or report instead of fabricating success. | [code-quality.md](code-quality.md) | [S39](standards-sources.md#s39) |
| Async / Await | Respect dependencies, cancellation and effects; awaiting does not make CPU work parallel. | [async-cache.md](async-cache.md) | [S48](standards-sources.md#s48) |
| Webhooks | Verify authenticity, durable receipt, replay/duplicate handling and out-of-order events. | [data-payments.md](data-payments.md) | [S03](standards-sources.md#s03), [S12](standards-sources.md#s12) |
| Background Jobs | Demonstrate worker lifecycle, retry, duplicate safety, backlog and failure handling. | [operations.md](operations.md) | [S41](standards-sources.md#s41) |
| Cron Jobs | Define time zone, overlap, missed runs, last success and actual platform schedule. | [operations.md](operations.md) | [S36](standards-sources.md#s36), [S41](standards-sources.md#s41) |
| Stateless Services | Externalize required durable state and test cross-instance requests; state still exists. | [systems-lifecycle.md](systems-lifecycle.md) | [S12](standards-sources.md#s12), [S33](standards-sources.md#s33) |
| Graceful Shutdown | Stop admission, drain safely, release resources and test termination/restart. | [systems-lifecycle.md](systems-lifecycle.md) | [S30](standards-sources.md#s30) |

## Database engineering

| Concept | Application / evidence | Owner | Sources |
| --- | --- | --- | --- |
| Database Indexing | Measure plans and representative reads against write/storage cost. | [systems-lifecycle.md](systems-lifecycle.md) | [S24](standards-sources.md#s24) |
| Database Migrations | Test existing data, locks, coexistence and data-safe recovery; preserve applied history. | [operations.md](operations.md) | [S54](standards-sources.md#s54) |
| Backups | Verify freshness/capacity and isolated restoration, not merely job creation. | [operations.md](operations.md) | [S55](standards-sources.md#s55) |
| Database Normalization | Use domain dependencies to prevent update anomalies without destroying required snapshots. | [systems-lifecycle.md](systems-lifecycle.md) | [S27](standards-sources.md#s27) |
| Soft Deletes | Define visibility, uniqueness, restore and purge; a deleted flag is not erasure. | [systems-lifecycle.md](systems-lifecycle.md) | [S03](standards-sources.md#s03), [S44](standards-sources.md#s44) |
| Connection Pooling | Budget total connections and verify actual pool/session-state semantics. | [systems-lifecycle.md](systems-lifecycle.md) | [S26](standards-sources.md#s26) |
| Read Replicas | Account for lag/conflicts and route authoritative/read-after-write decisions correctly. | [systems-lifecycle.md](systems-lifecycle.md) | [S25](standards-sources.md#s25) |
| Cache Invalidation | Test write/delete/account-switch invalidation and refill races. | [async-cache.md](async-cache.md) | [S03](standards-sources.md#s03), [S12](standards-sources.md#s12) |

## Security engineering

| Concept | Application / evidence | Owner | Sources |
| --- | --- | --- | --- |
| Secrets Management | Use restricted secret delivery/storage with redacted evidence and lifecycle ownership. | [security-controls.md](security-controls.md) | [S07](standards-sources.md#s07) |
| Secret Rotation | Plan replacement, overlap/revocation and incident response under the provider contract. | [security-controls.md](security-controls.md) | [S07](standards-sources.md#s07) |
| Environment Variables | Separate deploy configuration; an environment variable is not a secret-management system. | [systems-lifecycle.md](systems-lifecycle.md) | [S07](standards-sources.md#s07), [S49](standards-sources.md#s49) |
| HTTPS / TLS | Verify authenticated transport on relevant hops and effective proxy termination. | [security-controls.md](security-controls.md) | [S03](standards-sources.md#s03), [S12](standards-sources.md#s12) |
| Encryption in Transit | Protect actual network hops and certificate verification, not just a browser padlock. | [security-controls.md](security-controls.md) | [S03](standards-sources.md#s03), [S12](standards-sources.md#s12) |
| Encryption at Rest | Define threat/key/access scope including backups, logs and exports. | [security-controls.md](security-controls.md) | [S22](standards-sources.md#s22) |
| Hashing vs Encryption | Use password hashing for passwords and authenticated encryption for recoverable secrets. | [security-controls.md](security-controls.md) | [S06](standards-sources.md#s06), [S22](standards-sources.md#s22) |
| Salting | Use a unique per-password salt via a vetted password-hashing library. | [security-controls.md](security-controls.md) | [S06](standards-sources.md#s06) |
| Data Privacy (GDPR) | Establish actual applicable purpose, minimization, retention and rights; no compliance guarantee. | [security-controls.md](security-controls.md) | [S44](standards-sources.md#s44) |
| Principle of Least Privilege | Limit application, tool and operational permissions to the authorized task. | [security-controls.md](security-controls.md) | [S03](standards-sources.md#s03), [S43](standards-sources.md#s43) |
| Role-Based Access Control (RBAC) | Map role permissions while still enforcing ownership and tenant boundaries. | [security-controls.md](security-controls.md) | [S03](standards-sources.md#s03) |
| Row-Level Security (RLS) | Test database policies using actual application roles and known bypass/owner behavior. | [security-controls.md](security-controls.md) | [S23](standards-sources.md#s23) |
| Brute Force Protection | Bound attempts and detect abuse without exposing account existence. | [security-controls.md](security-controls.md) | [S04](standards-sources.md#s04), [S08](standards-sources.md#s08) |
| Account Lockout | Balance throttling/recovery with attacker-induced denial of service risk. | [security-controls.md](security-controls.md) | [S04](standards-sources.md#s04) |
| Password Reset Flows | Use purpose-bound, expiring, single-use tokens and non-enumerating responses. | [security-controls.md](security-controls.md) | [S04](standards-sources.md#s04), [S08](standards-sources.md#s08) |
| Magic Links | Protect one-time bearer links and safe redirects; do not assume phishing resistance. | [security-controls.md](security-controls.md) | [S04](standards-sources.md#s04), [S08](standards-sources.md#s08) |
| Passkeys | Validate WebAuthn challenge/origin/RP/signature and distinguish synced/device-bound credentials. | [security-controls.md](security-controls.md) | [S09](standards-sources.md#s09) |
| Single Sign-On (SSO) | Verify federation protocol and account binding; SSO does not grant resource permissions. | [security-controls.md](security-controls.md) | [S10](standards-sources.md#s10), [S11](standards-sources.md#s11) |
| API Keys | Restrict scope/storage and implement expiry or revocation as the provider contract requires. | [security-controls.md](security-controls.md) | [S07](standards-sources.md#s07), [S03](standards-sources.md#s03) |
| Token Expiration and Refresh | Verify issuer/audience/expiry, replay and refresh rotation/revocation/concurrency. | [security-controls.md](security-controls.md) | [S11](standards-sources.md#s11) |
| Cookie Flags (HttpOnly, Secure, SameSite) | Test actual cookie scope/lifetime and browser flows; flags do not replace CSRF controls. | [security-controls.md](security-controls.md) | [S05](standards-sources.md#s05) |
| SQL Injection | Parameterize values and allowlist identifiers; validation alone is insufficient. | [security-controls.md](security-controls.md) | [S13](standards-sources.md#s13) |
| Command Injection | Avoid shells and reject unsafe executable/options/arguments at the boundary. | [security-controls.md](security-controls.md) | [S13](standards-sources.md#s13) |
| XSS (Cross-Site Scripting) | Use context-aware encoding, safe sinks and maintained sanitization where HTML is allowed. | [security-controls.md](security-controls.md) | [S14](standards-sources.md#s14) |
| CSRF (Cross-Site Request Forgery) | Use flow-appropriate framework/token/origin defenses and test cross-site mutations. | [security-controls.md](security-controls.md) | [S15](standards-sources.md#s15) |
| SSRF (Server-Side Request Forgery) | Constrain resolved destinations, protocols, redirects and network access. | [security-controls.md](security-controls.md) | [S16](standards-sources.md#s16) |
| Open Redirects | Validate parsed canonical redirect destinations against intended allowlists. | [security-controls.md](security-controls.md) | [S19](standards-sources.md#s19) |
| Path Traversal | Enforce resolved containment and platform/archive/symlink boundaries. | [security-controls.md](security-controls.md) | [S20](standards-sources.md#s20) |
| Clickjacking | Apply actual framing policy and test permitted/forbidden embedding. | [security-controls.md](security-controls.md) | [S18](standards-sources.md#s18) |
| IDOR (Insecure Direct Object Reference) | Change resource/tenant IDs in denied-access cases and verify no unauthorized effects. | [security-controls.md](security-controls.md) | [S03](standards-sources.md#s03) |
| Mass Assignment | Allowlist writable fields; never accept client-assigned privilege/owner fields implicitly. | [api-contracts.md](api-contracts.md) | [S03](standards-sources.md#s03) |
| Dependency Vulnerabilities | Verify package existence/version/provenance and investigate relevant advisories/reachability. | [security-controls.md](security-controls.md) | [S43](standards-sources.md#s43) |
| File Upload Security | Layer size/type/storage/serving/parser defenses and check download ownership. | [security-controls.md](security-controls.md) | [S17](standards-sources.md#s17) |
| Content Security Policy (CSP) | Use a tested resource/framing policy; CSP is defense in depth, not XSS elimination. | [security-controls.md](security-controls.md) | [S18](standards-sources.md#s18), [S14](standards-sources.md#s14) |
| Security Headers | Verify effective headers through actual proxies/CDNs and supported browser behavior. | [security-controls.md](security-controls.md) | [S18](standards-sources.md#s18) |

## Infrastructure and DevOps

| Concept | Application / evidence | Owner | Sources |
| --- | --- | --- | --- |
| Docker | Use reproducible runtime images when justified; containers alone are not a complete security boundary. | [systems-lifecycle.md](systems-lifecycle.md) | [S45](standards-sources.md#s45) |
| CI/CD | Run real project checks and restrict workflow credentials/artifacts/deploy permissions. | [systems-lifecycle.md](systems-lifecycle.md) | [S46](standards-sources.md#s46), [S43](standards-sources.md#s43) |
| Infrastructure as Code (IaC) | Review plan/diff, state, permissions and drift; generating code does not authorize apply. | [systems-lifecycle.md](systems-lifecycle.md) | [S47](standards-sources.md#s47) |
| Staging Environments | Match consequential behavior while isolating real credentials/data/effects. | [operations.md](operations.md) | [S41](standards-sources.md#s41), [S43](standards-sources.md#s43) |
| Reverse Proxies | Define trusted forwarded headers, hop TLS, routing and bypass paths. | [systems-lifecycle.md](systems-lifecycle.md) | [S12](standards-sources.md#s12), [S33](standards-sources.md#s33) |
| API Gateways | Justify central routing/limits and retain authorization at the trusted business boundary. | [systems-lifecycle.md](systems-lifecycle.md) | [S12](standards-sources.md#s12), [S33](standards-sources.md#s33) |
| CDN (Content Delivery Network) | Check cache scope/invalidation, origin access and private response handling. | [systems-lifecycle.md](systems-lifecycle.md) | [S12](standards-sources.md#s12), [S33](standards-sources.md#s33) |
| Branching Strategies | Use project conventions and coherent changes without implicit push/history rewrite. | [systems-lifecycle.md](systems-lifecycle.md) | [S38](standards-sources.md#s38) |
| Code Review | Prioritize design/functionality/security and meaningful evidence over style-only churn. | [code-quality.md](code-quality.md) | [S39](standards-sources.md#s39) |

## Scalability and performance

| Concept | Application / evidence | Owner | Sources |
| --- | --- | --- | --- |
| Load Balancing | Verify health, draining, capacity and request/state behavior across instances. | [systems-lifecycle.md](systems-lifecycle.md) | [S33](standards-sources.md#s33) |
| Horizontal vs Vertical Scaling | Choose instance count versus instance capacity from measured bottlenecks and costs. | [systems-lifecycle.md](systems-lifecycle.md) | [S33](standards-sources.md#s33) |
| Rate Limiting | Choose meaningful keys/windows, distributed behavior and retry/abuse semantics. | [systems-lifecycle.md](systems-lifecycle.md) | [S03](standards-sources.md#s03), [S33](standards-sources.md#s33) |
| Caching | Define freshness, ownership, isolation and failure behavior before adding a cache. | [async-cache.md](async-cache.md) | [S03](standards-sources.md#s03), [S12](standards-sources.md#s12) |
| Load Testing | Use authorized representative workload/data and inspect latency/errors/resources. | [verification.md](verification.md) | [S33](standards-sources.md#s33), [S40](standards-sources.md#s40) |
| Profiling | Measure actual CPU/memory/I/O/retention hotspots before optimizing. | [systems-lifecycle.md](systems-lifecycle.md) | [S29](standards-sources.md#s29), [S31](standards-sources.md#s31) |
| Performance Budgets | Agree measurable journey/resource budgets and verify comparable workloads. | [systems-lifecycle.md](systems-lifecycle.md) | [S31](standards-sources.md#s31), [S33](standards-sources.md#s33) |
| Memory Leaks | Use repeated retention/resource evidence; one growth sample does not prove a leak. | [systems-lifecycle.md](systems-lifecycle.md) | [S29](standards-sources.md#s29), [S31](standards-sources.md#s31) |
| Cost Monitoring | Measure accepted task/service cost including retries/tools/review/operation. | [agent-context.md](agent-context.md) | [S31](standards-sources.md#s31), [S33](standards-sources.md#s33) |

## Reliability and distributed systems

| Concept | Application / evidence | Owner | Sources |
| --- | --- | --- | --- |
| Timeouts | Use bounded dependency timeouts within an end-to-end deadline; an effect may be unknown. | [systems-lifecycle.md](systems-lifecycle.md) | [S28](standards-sources.md#s28) |
| Exponential Backoff | Cap attempts/time, select retryable failures and use jitter when useful. | [systems-lifecycle.md](systems-lifecycle.md) | [S28](standards-sources.md#s28) |
| Idempotency | Protect one logical effect under replay/concurrency; retry identity and persisted state matter. | [data-payments.md](data-payments.md) | [S12](standards-sources.md#s12), [S28](standards-sources.md#s28) |
| Circuit Breakers | Add only when justified; define recovery, bounded fallback and observed failure behavior. | [systems-lifecycle.md](systems-lifecycle.md) | [S28](standards-sources.md#s28) |
| Message Queues | Check durable receipt, redelivery, worker operation and duplicate-safe business effects. | [operations.md](operations.md) | [S41](standards-sources.md#s41) |
| Race Conditions | Exercise competing interleavings and assert shared-state invariants. | [systems-lifecycle.md](systems-lifecycle.md) | [S41](standards-sources.md#s41) |
| Concurrency | Separate actual prerequisites from safe bounded overlap and preserve required ordering. | [async-cache.md](async-cache.md) | [S48](standards-sources.md#s48), [S28](standards-sources.md#s28) |
| Health Checks | Distinguish readiness, liveness, startup and external journey checks. | [systems-lifecycle.md](systems-lifecycle.md) | [S30](standards-sources.md#s30), [S31](standards-sources.md#s31) |
| Disaster Recovery | Agree data-loss/recovery targets and demonstrate restoration, compatibility and core behavior. | [operations.md](operations.md) | [S41](standards-sources.md#s41), [S43](standards-sources.md#s43) |

## Monitoring and observability

| Concept | Application / evidence | Owner | Sources |
| --- | --- | --- | --- |
| Logging | Record useful events with ownership, redaction, retention and access controls. | [systems-lifecycle.md](systems-lifecycle.md) | [S21](standards-sources.md#s21) |
| Structured Logging | Use stable fields/correlation and avoid secrets or uncontrolled cardinality. | [systems-lifecycle.md](systems-lifecycle.md) | [S21](standards-sources.md#s21), [S29](standards-sources.md#s29) |
| Monitoring | Observe meaningful service behavior, not process existence alone. | [systems-lifecycle.md](systems-lifecycle.md) | [S31](standards-sources.md#s31) |
| Alerting | Set actionable SLO/risk-based signals with a responding owner and runbook. | [systems-lifecycle.md](systems-lifecycle.md) | [S32](standards-sources.md#s32) |
| Distributed Tracing | Verify causal propagation/sampling and sensitive-data boundaries across services. | [systems-lifecycle.md](systems-lifecycle.md) | [S29](standards-sources.md#s29) |
| Error Tracking | Group actionable failures with context while redacting sensitive data. | [systems-lifecycle.md](systems-lifecycle.md) | [S21](standards-sources.md#s21), [S31](standards-sources.md#s31) |
| Uptime Monitoring | Probe a representative external journey and report actual coverage. | [systems-lifecycle.md](systems-lifecycle.md) | [S31](standards-sources.md#s31) |
| Audit Logs | Protect actor/action/time evidence and tamper resistance; immutability is not automatic. | [security-controls.md](security-controls.md) | [S21](standards-sources.md#s21) |

## Testing and quality assurance

| Concept | Application / evidence | Owner | Sources |
| --- | --- | --- | --- |
| Automated Testing | Automate meaningful observable acceptance and record actual execution/limits. | [verification.md](verification.md) | [S40](standards-sources.md#s40) |
| Unit Testing | Check isolated rules with independent expectations and useful boundaries. | [verification.md](verification.md) | [S40](standards-sources.md#s40) |
| Integration Testing | Exercise actual affected service/database contracts instead of only mocks. | [verification.md](verification.md) | [S40](standards-sources.md#s40) |
| End-to-End (E2E) Testing | Verify representative user journeys/failures without treating one green path as exhaustive. | [verification.md](verification.md) | [S40](standards-sources.md#s40) |
| Debugging | Read original errors, reproduce, trace the cause and verify the targeted fix. | [systems-lifecycle.md](systems-lifecycle.md) | [S39](standards-sources.md#s39), [S41](standards-sources.md#s41) |
| Penetration Testing | Require explicit scope/authorization and bounded evidence; it is not ordinary code review. | `rse-security-review` skill | [S56](standards-sources.md#s56) |

## API engineering

| Concept | Application / evidence | Owner | Sources |
| --- | --- | --- | --- |
| API Versioning | Identify consumer coupling and migrate breaking contracts only where required. | [api-contracts.md](api-contracts.md) | [S42](standards-sources.md#s42), [S37](standards-sources.md#s37) |
| API Documentation | Use the adopted source of truth and verify actual methods/fields/errors/examples. | [api-contracts.md](api-contracts.md) | [S42](standards-sources.md#s42) |

## Software development practices

| Concept | Application / evidence | Owner | Sources |
| --- | --- | --- | --- |
| Semantic Versioning | Declare the public API and apply compatible/incompatible version rules. | [systems-lifecycle.md](systems-lifecycle.md) | [S37](standards-sources.md#s37) |
| Technical Debt | Record justified shortcuts with impact, ownership and revisit triggers when useful. | `rse-refactoring` skill | [S53](standards-sources.md#s53), [S52](standards-sources.md#s52) |
| Reading Documentation | Check the official installed-version definition, not plausible APIs or search summaries alone. | [verification.md](verification.md) | [S39](standards-sources.md#s39), [S41](standards-sources.md#s41) |
| Reading Error Messages | Retain exact diagnostics and environment while explaining the cause/evidence to the user. | [systems-lifecycle.md](systems-lifecycle.md) | [S39](standards-sources.md#s39), [S41](standards-sources.md#s41) |
| Feature Flags | Use only an accepted rollout/product need, safe defaults, ownership and retirement. | [systems-lifecycle.md](systems-lifecycle.md) | [S52](standards-sources.md#s52), [S33](standards-sources.md#s33) |

## Frontend and user experience

| Concept | Application / evidence | Owner | Sources |
| --- | --- | --- | --- |
| Accessibility | Verify applicable WCAG behavior with manual and automated evidence, including keyboard/focus. | [ui-css.md](ui-css.md) | [S34](standards-sources.md#s34) |
| Mobile Responsiveness | Check intermediate widths, zoom, long text, keyboard overlap and supported input modes. | [ui-css.md](ui-css.md) | [S34](standards-sources.md#s34) |
| Character Encoding | Distinguish bytes/code points/graphemes and test intended Unicode round trips. | [systems-lifecycle.md](systems-lifecycle.md) | [S35](standards-sources.md#s35) |
| Time Zones | Separate instants/civil times/durations and test actual IANA/DST recurrence behavior. | [systems-lifecycle.md](systems-lifecycle.md) | [S36](standards-sources.md#s36) |
