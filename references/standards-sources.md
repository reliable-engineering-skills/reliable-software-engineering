# Sources and authority boundaries

Relevant pages/sections inspected on 22 November 2026. Links are maintained references, not a requirement to load everything. Recheck adopted versions when implementing. Normative standards, professional frameworks, vendor behavior, and practitioner judgment have different authority; none is universal proof of correctness, security, or senior-engineer consensus.

The following prose is independently written. No third-party scripts, templates, schemas or agent workflows were copied or installed. ASVS/SSDF organize requirements/practices; using their names does not certify a project.

<a id="s01"></a>
## S01: GitHub Spec Kit pinned templates
[GitHub Spec Kit pinned templates](https://github.com/github/spec-kit/tree/a4d571229e164e440f8950cac034607bae7b7518/templates) — Maintainer workflow; spec, plan, tasks, independent stories; selectively adapted.

<a id="s02"></a>
## S02: Anthropic model prompting guidance
[Anthropic prompting guidance (Sonnet 5.5 edition; check the current model's page)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5) — Vendor model guidance; medium, scope, persistence and verification; not a task-length guarantee.

<a id="s03"></a>
## S03: OWASP ASVS
[OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) — Security verification requirements framework; select controls and record actual evidence.

<a id="s04"></a>
## S04: OWASP Authentication
[OWASP Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) — Authentication, throttling and recovery guidance.

<a id="s05"></a>
## S05: OWASP Session Management
[OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) — Cookie/session rotation, expiry and lifecycle guidance.

<a id="s06"></a>
## S06: OWASP Password Storage
[OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) — Password hashing, salts and current algorithm guidance.

<a id="s07"></a>
## S07: OWASP Secrets Management
[OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) — Provisioning, least privilege, auditing and rotation.

<a id="s08"></a>
## S08: NIST SP 800-63B-4
[NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html) — Digital authentication guideline; factors, authenticator lifecycle and recovery.

<a id="s09"></a>
## S09: W3C WebAuthn
[W3C WebAuthn](https://www.w3.org/TR/webauthn-3/) — Public-key credential standard, including device-bound and synchronized contexts.

<a id="s10"></a>
## S10: OpenID Connect Core
[OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) — Federated authentication protocol; do not conflate OAuth authorization with authentication.

<a id="s11"></a>
## S11: IETF RFC 9700
[IETF RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html) — OAuth security best current practice, including token and redirect protections.

<a id="s12"></a>
## S12: IETF RFC 9110
[IETF RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) — Normative HTTP semantics: methods, statuses, intermediaries and idempotent semantics.

<a id="s13"></a>
## S13: OWASP Injection Prevention
[OWASP Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html) — Safe APIs and parameterization; validation alone is insufficient.

<a id="s14"></a>
## S14: OWASP XSS Prevention
[OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) — Contextual encoding, sanitization and safe framework sinks.

<a id="s15"></a>
## S15: OWASP CSRF Prevention
[OWASP CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) — Framework/token/origin defenses selected for the authentication flow.

<a id="s16"></a>
## S16: OWASP SSRF Prevention
[OWASP SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) — URL, destination, redirect and network boundaries.

<a id="s17"></a>
## S17: OWASP File Upload
[OWASP File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) — Layered type/size/storage/serving/processing controls.

<a id="s18"></a>
## S18: OWASP HTTP Headers
[OWASP HTTP Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html) — CSP, transport, framing, MIME and effective response policy.

<a id="s19"></a>
## S19: OWASP Redirects
[OWASP Redirects](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html) — Canonical allowed redirect destinations and parser-aware validation.

<a id="s20"></a>
## S20: OWASP Path Traversal
[OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal) — File-path boundary and platform-aware containment guidance.

<a id="s21"></a>
## S21: OWASP Logging
[OWASP Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) — Security events, privacy, protection and evidence limits.

<a id="s22"></a>
## S22: OWASP Cryptographic Storage
[OWASP Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html) — Data encryption design and key lifecycle.

<a id="s23"></a>
## S23: PostgreSQL Row Security
[PostgreSQL Row Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) — Engine-specific RLS and bypass/ownership semantics; verify adopted version.

<a id="s24"></a>
## S24: PostgreSQL Indexes
[PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html) — Query benefit versus write/storage overhead.

<a id="s25"></a>
## S25: PostgreSQL Hot Standby
[PostgreSQL Hot Standby](https://www.postgresql.org/docs/current/hot-standby.html) — Read-only replica behavior, visibility and conflicts.

<a id="s26"></a>
## S26: PgBouncer Features
[PgBouncer Features](https://www.pgbouncer.org/features.html) — Pool modes and session-feature compatibility; no mandate to add PgBouncer.

<a id="s27"></a>
## S27: Microsoft Database Normalization
[Microsoft Database Normalization](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description) — Vendor explanation of functional organization and update anomalies.

<a id="s28"></a>
## S28: AWS Builders Library: retries
[AWS Builders Library: retries](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) — Practitioner/operator guidance on deadlines, retry amplification and jitter.

<a id="s29"></a>
## S29: OpenTelemetry Signals
[OpenTelemetry Signals](https://opentelemetry.io/docs/concepts/signals/) — Maintainer definitions for traces, metrics, logs and profiles.

<a id="s30"></a>
## S30: Kubernetes Pod Lifecycle
[Kubernetes Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/) — Platform-specific readiness/termination behavior; adapt the actual runtime, do not mandate Kubernetes.

<a id="s31"></a>
## S31: Google SRE Monitoring
[Google SRE Monitoring](https://sre.google/workbook/monitoring/) — Operational practice, relevant signals and diagnosis.

<a id="s32"></a>
## S32: Google SRE Alerting
[Google SRE Alerting](https://sre.google/workbook/alerting-on-slos/) — Actionable service-objective alerts, not arbitrary thresholds.

<a id="s33"></a>
## S33: Google SRE Managing Load
[Google SRE Managing Load](https://sre.google/workbook/managing-load/) — Load distribution, capacity and operational tradeoffs.

<a id="s34"></a>
## S34: W3C WCAG 2.2
[W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) — Accessibility standard; scoped manual/automated evidence is required for conformance claims.

<a id="s35"></a>
## S35: W3C Character Definitions
[W3C Character Definitions](https://www.w3.org/International/articles/definitions-characters/) — Characters, encodings, code points and user-perceived units.

<a id="s36"></a>
## S36: IANA Time Zone Database
[IANA Time Zone Database](https://www.iana.org/time-zones) — Maintained time-zone rules; fixed offsets are not full zones.

<a id="s37"></a>
## S37: Semantic Versioning
[Semantic Versioning](https://semver.org/) — Versioning specification conditional on a declared public API.

<a id="s38"></a>
## S38: Git Workflows
[Git Workflows](https://git-scm.com/docs/gitworkflows) — Maintainer guidance on coherent changes, branches and reviewable history.

<a id="s39"></a>
## S39: Google Engineering Practices: Review
[Google Engineering Practices: Review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) — Engineering practice: design, functionality, complexity, tests, names and comments; not a universal line-count standard.

<a id="s40"></a>
## S40: Google Software Engineering: Testing
[Google Software Engineering: Testing](https://abseil.io/resources/swe-book/html/ch11.html) — Practitioner testing guidance; risk/behavior over superficial test counts.

<a id="s41"></a>
## S41: IEEE Computer Society SWEBOK
[IEEE Computer Society SWEBOK](https://www.computer.org/education/bodies-of-knowledge/software-engineering) — Professional body-of-knowledge overview, not a project compliance certificate.

<a id="s42"></a>
## S42: OpenAPI Specification
[OpenAPI Specification](https://spec.openapis.org/oas/latest.html) — API contract standard; use the project-supported version rather than always migrating to latest.

<a id="s43"></a>
## S43: NIST SSDF
[NIST SSDF](https://www.nist.gov/itl/ssd/software-quality-group/secure-software-development-framework-ssdf) — Secure development practice framework; no invented certification.

<a id="s44"></a>
## S44: GDPR official text
[GDPR official text](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) — Legal primary text for applicable privacy requirements; applicability is not determined by this skill.

<a id="s45"></a>
## S45: Docker Development Docs
[Docker Development Docs](https://docs.docker.com/develop/) — Vendor container development documentation, not evidence containers alone provide complete isolation.

<a id="s46"></a>
## S46: GitHub Actions
[GitHub Actions](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions) — Vendor CI/CD workflow documentation; retain actual project tooling.

<a id="s47"></a>
## S47: Terraform Introduction
[Terraform Introduction](https://developer.hashicorp.com/terraform/intro) — Vendor IaC definition/lifecycle; generated plans do not authorize apply.

<a id="s48"></a>
## S48: MDN async functions
[MDN async functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) — Maintainer-language reference for promises/await; no automatic CPU parallelism.

<a id="s49"></a>
## S49: Twelve-Factor Configuration
[Twelve-Factor Configuration](https://12factor.net/config) — Practitioner configuration separation; environment variables are not a complete secret store.

<a id="s50"></a>
## S50: FIRST CVSS 4.0
[FIRST CVSS 4.0](https://www.first.org/cvss/v4.0/specification-document) — Severity scoring specification; use explicit justified vectors when requested.

<a id="s51"></a>
## S51: MITRE CWE
[MITRE CWE](https://cwe.mitre.org/about/index.html) — Weakness classification; a CWE label is not proof a weakness is present.

<a id="s52"></a>
## S52: Martin Fowler: YAGNI
[Martin Fowler: YAGNI](https://martinfowler.com/bliki/Yagni.html) — Original-author practitioner design guidance, not a mandatory infrastructure ban.

<a id="s53"></a>
## S53: Refactoring
[Refactoring](https://refactoring.com/) — Original-author behavior-preserving transformation literature.


<a id="s54"></a>
## S54: PostgreSQL Modifying Tables
[PostgreSQL Modifying Tables](https://www.postgresql.org/docs/current/ddl-alter.html) - Engine behavior for schema changes; plan deployment/migrations against the adopted version.

<a id="s55"></a>
## S55: PostgreSQL Backup and Restore
[PostgreSQL Backup and Restore](https://www.postgresql.org/docs/current/backup.html) - Engine backup approaches and restoration requirements; adapt actual engine/platform behavior.

<a id="s56"></a>
## S56: OWASP Web Security Testing Guide
[OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/) - Structured security testing guidance; requires an actual authorized scope.

## Attached-source provenance

- `guard-skills.zip`: SHA-256 `0988b170596db293f3738a56a2994703323b7f44c5d5c49a56dfb37f820e076c`; bundled source identifies amElnagdy/guard-skills revision `ffa26036b7b5e77b20b5d679304a703b6fd1a43d`, MIT Ahmed Nagdy 2026. Selected clean-code/formatting, test and documentation guidance was evaluated; not every language-specific reference was reviewed. Existing v6-derived test/documentation improvements were retained rather than duplicated.

- `security-audit-skill-main.zip`: SHA-256 `03978c2563b15b4ecb609f5f96029d89a12604e0457d0f2e69faf24a56c57ae1`; MIT Cloudflare 2025-2026 according to the archive license. Selected core/evidence/reporting guidance was evaluated. Other companion domains were not comprehensively audited. No archive code was run.

- `software_engineering_concepts_ar.md`: supplied terminology source with 109 unique terms across 11 categories. Its own provenance says it derives from five screenshots, with an inferred truncated penetration-testing label and unread/missing content. It is a coverage input, not a technical authority. The concept matrix corrects oversimplified definitions and links responsible sources.

- Spec Kit was pinned to commit `a4d571229e164e440f8950cac034607bae7b7518`; README and spec/plan/tasks templates were inspected. This is a selective portable adapter, not a Spec Kit installation or an assertion that all repository code was reviewed.

No full audit, multi-agent launch, branch creation, forced approval ceremony, fixed code-size threshold, or unmeasured performance claim was adopted from attachments. Independent checks are used only when available, relevant and authorized.
