# Agent context, cost, automation, and learning

## Agent context, instructions, and cost

### Practical knowledge structure

Keep a short project entrypoint with purpose, correct run/check commands, module structure, critical rules, and links to details. Put feature/decision documentation near its subject and give each fact one canonical owner where practical.

Do not duplicate the codebase in Markdown or repeat a rule across ten files. Persistent instructions hold stable knowledge; a temporary session log does not automatically belong in every context.

There is no magic two-page limit. Judge relevance, clarity, loading cost, and maintenance. Preserve critical constraints even when longer, and enforce them with automated checks when useful.

### Task context package

Load the goal and constraints, related files/callers, data contracts, focused tests, and the latest consequential decision. Expand reading when dependencies require it; reduced context does not justify ignoring known consumers.

For a new session, hand over the revision/branch, completed work, changed files, evidence, decisions, remaining problem, and next action. Verify repository state; do not resume from a summary alone after the repository changes.

[Lost in the Middle](https://arxiv.org/abs/2307.03172) reports position-related performance degradation for studied models/tasks in long contexts. This supports selective retrieval and checking constraint application. It does not establish that every current model always forgets the middle or that placing a rule first guarantees compliance.

### Evaluate model selection

| Work | Suggested policy |
| --- | --- |
| Clear bounded formatting/transformation | Try a deterministic tool first; use sufficient model capability if needed. |
| Repository investigation and evidence collection | Targeted search/read tools with verifiable locations. |
| Complex design or ambiguous diagnosis | Appropriate reasoning capability, relevant context, and failure examples. |
| Independent review | Risk questions, evidence, and tests; merely asking another model is insufficient. |
| Implementing a stable plan | A less costly model when evaluation shows it preserves acceptance quality. |

Separating planning and execution can help, but lost handoff information or retries can negate savings. Do not hard-code model names/rankings into permanent policy.

Measure accepted task completion cost: inference, tools, retries, review, correction, and operation; record time and quality too. Compare languages only when the cost matters. Clarity and correct requirements outweigh cosmetic language switching. Do not assume every context token has identical billing: cache and pricing behavior depend on the service.

### Avoid unsupported agreement

Expose consequential assumptions, alternatives, and reasons for rejecting unsuitable proposals. Do not require disagreement with everything; habitual objection wastes time and creates artificial conflict. Criticism needs evidence and proportionate action.

Do not call instructions 'model training' unless weights were actually trained or fine-tuned. Usually they are guidance/external memory whose value depends on being loaded and correct.

## Automation, collaboration, and learning

### Automated content pipelines

For tools that draft lessons, articles, images or link/content updates, keep sourced drafting, review and publication boundaries explicit; do not assume an agent can safely do everything alone.

Suggested policy:

1. Define sources and permitted additions. A lesson assignment should connect to material actually taught.
2. Separate drafting, approval, and publication where the context requires review.
3. Check changing links, versions, and facts; similar names do not establish replacement-tool compatibility.
4. Retain change evidence and a previous-version reference for recovery.
5. Use tables for parallel data, steps for sequence, and diagrams for relationships; do not force one presentation form onto all explanations.
6. Avoid distracting future concepts and explain unfamiliar terms for the audience.
7. For already-authorized recurring publication, provide suitable checks, limits, and failure handling; do not add unnecessary approval for every run.

Saved/loaded guidance and corrections can improve behavior without proving a mistake cannot recur. Generating a similar face, voice, or image does not establish usage rights; determine actual rights and authorization when relevant.

### Parallel work and delegation

Parallel execution does not replace clear contracts and ownership. Before dividing work among people or tools, define task responsibility, shared files/interfaces, integration order, and compatibility review.

Use isolated branches/workspaces where they prevent conflicts. Do not launch several agents against one sensitive change without coordination and authorization. Measure the human review bottleneck; more implementation can increase the queue of unreviewed work.

One successful model task does not remove the team's technical responsibility. Staffing depends on the product, operations, knowledge, and review load, not a single demo.

### Estimates and communication

Estimate understanding, implementation, integration, verification, deployment, and follow-up with explicit uncertainty. Do not generalize an exceptional day or initial prototype speed to all later work.

When questioning a release, provide reproducible behavior, impact, scope, and an actionable choice: reduce scope, release narrowly, or fix first. Avoid alarmism and vague architectural language; do not wait for or cause an incident to prove a point.

For example: changing a report ID allowed company A's user to read company B's data in a test environment; require server authorization and report-isolation checks before wider access. That is more useful than saying the code will explode.
