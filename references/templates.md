# Task, decision, handoff, and acceptance templates

These templates are written in English for the agent. Render user-facing labels, questions, reasons, findings, and results in the user's language. Preserve code, identifiers, and exact evidence.

## Implementation task template

Use this template only for implementation requests. For review/planning, request findings/a plan and suitable evidence without applying proposed changes. Fill the fields before use; brackets indicate inputs, not facts about a real project.

```text
Implement the following task using the supplied engineering decision guide.

Goal and accepted behavior: [clear description and acceptance example]
Available context: [repository/files/version/environment]
Scope and authorization: [requested work, access, and deployment boundaries]
Known constraints: [data/permissions/contracts/operation/time]

Start with available evidence and related existing functionality.
Identify consequential assumptions and continue authorized work.
Choose a small sufficient change; justify new services/patterns.
Handle applicable failures, concurrency, and duplicate effects.
Protect historical data and permissions; do not expand access implicitly.
Perform proportionate verification; do not weaken tests to hide a defect.
Report actual work, evidence, and limits; do not claim deployment/security without evidence.
If missing information blocks one step, ask a focused question and continue independent work.

Outputs for the user:
- What changed and why.
- Decision rationale for consequential tradeoffs.
- Verification evidence and applicable environment.
- Unchecked behavior or required decisions, their impact, and next action.
```

## Short documentation templates

### Engineering decision

```text
Decision: [title]
Context: [problem, constraints, evidence]
Actual alternatives: [smallest useful set]
Choice and rationale: [requirements-related reason]
Effects/tradeoffs: [correctness/operation/cost/maintenance]
Verification: [evidence that resolves the decision]
Rollback/transition: [when consequential]
Revisit trigger: [changed requirement or measurement]
```

Do not create a decision record for every variable/style edit. Use it for cross-module, data, operational, or hard-to-reverse decisions.

### Finding/defect

```text
Finding: [observable behavior]
Evidence/reproduction: [steps/inputs/environment/location]
Expected vs actual: [specific difference]
Impact/scope: [who is affected and when]
Confidence: [confirmed/likely/needs verification]
Smallest suitable remedy: [reasoned proposal]
Resolution evidence: [relevant check]
Owner/next action: [when useful]
```

### New-session handoff

```text
Goal/scope: [...]
Repository/branch/revision state: [...]
Completed changes and affected files: [...]
Established decisions and references: [...]
Executed checks and results: [...]
Actual assumptions/risks/gaps: [...]
Next action: [...]
```

Do not include secrets/sensitive data copies. Refer to the setting/evidence location without revealing its secret value.

### Honest completion report

```text
Outcome: [available behavior]
Main changes and reasons: [...]
Executed verification: [check/result/environment/revision]
Unchecked behavior: [if any; reason and impact]
Operational state: [local/preview/test/production as actually verified]
Remaining work: [specific required work or none within scope]
```

## Adaptable acceptance checklist

Use only applicable items. Explain non-applicability briefly when useful; every success claim needs evidence. Checked boxes do not replace engineering judgment. In a review/planning task, report assessment rather than implying implementation.

- [ ] Goal, scope, and acceptance criteria are clear.
- [ ] Project instructions and affected files/contracts were read.
- [ ] Existing behavior was searched before adding a duplicate.
- [ ] Versions, engine, and required services are known.
- [ ] Design fits requirements and operational capacity.
- [ ] Business invariants/state transitions are defined for consequential operations.
- [ ] Permissions, ownership, and tenant isolation are checked where relevant.
- [ ] Financial/business history is preserved where applicable.
- [ ] Retry, concurrency, interruption, and delayed-result cases are addressed where required.
- [ ] Required workers/cron have configuration, monitoring, and demonstrated operation.
- [ ] Test-data policy prevents unintended writes/external effects.
- [ ] Checks are meaningful/proportionate and not weakened to bypass defects.
- [ ] Evidence applies to the current change/revision.
- [ ] Affected interface, responsive behavior, and error states were inspected.
- [ ] Secrets/sensitive data are absent from code, documentation, and responses.
- [ ] Required migration/recovery plans are established.
- [ ] Deployment happened only within authorization and was verified appropriately.
- [ ] The report distinguishes completed, proposed, and unverified work.
