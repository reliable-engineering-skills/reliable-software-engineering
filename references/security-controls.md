# Security controls selected by the affected boundary

Read only the applicable sections; use existing framework/provider mechanisms and current official versioned documentation. [Primary sources](standards-sources.md) distinguish standards, implementation guidance, and practitioner advice. These controls are engineering criteria, not certification or a mandate to add every security feature.

## Identity, sessions, and credentials

Separate authentication from resource authorization. Deny by default at trusted access paths, including background jobs, exports, alternate IDs, and tenant changes. RBAC groups privileges but does not replace ownership checks; RLS is a database policy, with owner/superuser/bypass behavior that must be tested under the actual application role.

Use the established identity provider/framework. MFA/2FA requires independent factors; a password plus another knowledge question is not two-factor authentication. Recovery and factor reset must not bypass the intended assurance. Passkeys use WebAuthn public-key credentials; credentials may be device-bound or synchronized, and correct challenge, origin, relying-party ID, signature, and account binding are still necessary. SSO is federation, not automatic authorization; OpenID Connect adds authentication to OAuth. Validate the selected protocol/issuer/audience/redirect/nonce/state/PKCE requirements using the actual library and flow.

Rotate session IDs at relevant authentication/privilege transitions, set idle/absolute expiry appropriate to the product, and revoke server sessions/tokens where required on logout/reset/compromise. Keep bearer secrets out of URLs/logs. API keys need restricted scope, storage, lifecycle, and revocation; do not expose a privileged service key to the browser. Verify access/refresh expiry, replay protection and rotation/revocation under the provider contract, with concurrent refresh behavior tested.

Protect login/reset with bounded retries/rate limits and detection, generic account-existence responses, and defenses against lockout abuse. Reset/magic-link tokens need cryptographic generation, purpose/account binding, short appropriate expiry, single-use consumption, safe redirects, and no leakage through logs/referrers. Magic links are not automatically phishing-resistant or suitable for every assurance level.

Set session cookies' Secure, HttpOnly, SameSite, scope, and lifetime appropriately. HttpOnly limits script reads, not all browser-originated misuse. SameSite depends on mode and navigation/request context; it is not a universal replacement for CSRF protection. Test real browser flows, including supported cross-site identity/payment flows.

Use framework password hashing with a current vetted adaptive password-hashing scheme and unique salts; a fast generic hash or reversible password encryption is unsuitable. Libraries generally manage salts. Follow current OWASP/NIST settings and migration guidance rather than freezing parameters here. Do not impose arbitrary periodic password replacement; rotate compromised credentials and keys according to their actual risk/provider lifecycle.

## Untrusted input, output, and files

Validate allowed fields/types/bounds at the server boundary. Prevent mass assignment with explicit writable fields; the UI and static types are not trust boundaries. Parameterize database values and allowlist non-parameterizable identifiers. Avoid shell interpretation; argument arrays still need protection against option injection and unsafe executable/argument choices.

For XSS, use contextual output encoding and safe framework sinks; sanitize permitted rich HTML with a maintained sanitizer. Validate URL schemes. CSP is defense in depth, not a replacement for safe sinks. For cookie-authenticated mutations use framework CSRF/origin controls appropriate to the flow; CORS is not authentication/authorization.

For outbound requests (SSRF), constrain schemes/destinations, normalize with a reliable URL parser, account for DNS resolution/rebinding and redirects, and block unintended internal/metadata access through application and network controls. For redirects validate canonical destinations rather than string-prefix matches. For paths enforce resolved containment and allowed file operations, considering encodings, symlinks, platform semantics, and archive entries.

Uploads need allowed types, size/count/decompression limits, server-generated names, safe storage/serving outside executable contexts, authentication/authorization, and relevant malware/parser defenses. Extension/MIME claims alone are insufficient. Verify download ownership and active-content behavior; test using bounded dummy fixtures.

## Transport, browser, storage, and supply chain

Use authenticated TLS and certificate verification on relevant hops. Encryption in transit and at rest address different risks; protect/manage keys separately, define access and rotation, and include backups/logs/exports in data scope. An environment variable is a configuration delivery mechanism, not a complete secrets-management system. Prefer the project's secret store, least privilege, auditability, and safe lifecycle; do not dump environment values into reports.

Deploy applicable HSTS, MIME protections, framing restrictions (CSP frame-ancestors and compatible X-Frame-Options where needed), and a tested CSP with suitable nonces/hashes. Header values depend on actual product/resource requirements; do not blindly copy a universal header set or break legitimate embedding. Check effective responses through proxies/CDNs and the target browser policy.

Verify dependencies and supported versions, lockfile changes, provenance and relevant advisories with the project's trusted tools; a scanner hit needs reachability/impact review. Do not install a plausibly named package without verification. Container/IaC/CI permissions and release credentials are part of the trust boundary; code signing/attestation does not prove behavior correctness.

Privacy requirements depend on data, purpose, actors, retention and jurisdiction. Minimize collection/access and define deletion/export/backup handling with the owner. Soft deletion preserves records; it is neither erasure nor a general GDPR compliance solution. Legal applicability and compliance claims require the actual requirement and appropriate expertise, not this checklist.

## Evidence and operational consequences

For the changed boundary, test allowed/denied users, malformed input, wrong owner/tenant, replay/expiry, and relevant failure/concurrency cases. Inspect actual fields/effects, not status 200 alone. Log security-relevant events with useful correlation and redaction. Audit records should be access-controlled, retained appropriately, and tamper-evident/resistant; writing a log does not make it immutable or prove non-repudiation. Avoid secrets, reset tokens, raw sessions, and unnecessary personal data.

A penetration test is an explicitly scoped/authorized adversarial assessment, not a synonym for code review or permission to probe live systems. Separate source review, local validation, scanner scope, and deployment observations in the final report.
