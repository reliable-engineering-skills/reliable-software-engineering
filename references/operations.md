# Operations, deployment, and recovery

## Environment parity and background work

### Operational contract

Establish versions from project files and actual runtime: language, framework, package manager, database, extensions, and external services. Preserve lockfiles and specify build/run/check commands. Distinguish required constants from environmental settings; document secret locations, not values.

[Twelve-Factor: Dev/Prod Parity](https://12factor.net/dev-prod-parity) explains how differing database/cache services can cause production failures despite local test success. Bring relevant environments close enough to verify actual engine/service behavior while isolating data and permissions.

Parity does not mean production credentials/customer data or reproducing the full production infrastructure on a developer's machine.

### Workers and queues

When a feature requires a worker, readiness includes:

1. Startup and restart after deployment/crash.
2. Connection, target queues, timeout, and concurrency settings.
3. Retry policy distinguishing transient errors from invalid input/permanent rejection.
4. Duplicate-effect protection on redelivery.
5. Failed/stuck-job visibility and safe reprocessing.
6. Oldest-job age, backlog, and failure measures, not just a live process.

A successful manual script does not prove a persistent worker is operating. Configuring a service does not mean the model monitors it after the session ends.

### Scheduled work

Specify schedule/time zone, allowed overlap, missed-run handling, duplicate protection, and last-success signal. Verify the scheduler on the actual deployment platform; do not assume local settings transfer.

### Backup and recovery

Creating a backup job is weaker evidence than working recovery:

- Define scope, frequency, retention, location, permissions, and content protection.
- Check last successful backup age, size, write status, and remaining capacity.
- Alert a real responding owner about failure, delay, or approaching capacity.
- Restore into isolation, then check data integrity and core journeys.
- Agree acceptable data loss and recovery time; do not invent targets and present them as requirements.

A backup file does not prove restorability. A generic success message may omit files or a database. Assess how deletion/encryption of the source affects backups according to system value and recovery requirements.

## Deployment, CI/CD, and recovery

### Gates follow risk and authorization

Before authorized deployment, tie the release to a specific revision/build and relevant checks. Verify environment settings, background work, migrations, and compatibility with other services.

CI success is not deployment success, and deployment success is not a correct user journey. After deployment perform bounded safe checks of core behavior and feature-specific signals, not only the home page.

### Recoverable release strategy

Use a limited rollout, feature flag, blue/green switch, or direct deployment according to risk/platform capabilities. [Google SRE: Canarying Releases](https://sre.google/workbook/canarying-releases/) describes evaluating a change on part of a service; do not impose that infrastructure on a simple website.

For a limited rollout, define comparisons, expansion stop conditions, a suitable observation window/sample, and a decision owner. Do not invent success measurements without representative data.

### Migration and compatibility

Test migrations in a representative environment, including locks, duration, constraints, and existing values. When needed, stage changes so versions can coexist before old fields are removed.

Application rollback does not automatically undo destructive migrations or provider transactions. Define rollback, forward fix, or restore and their impact on data written after deployment. Keeping old code alone is not a rollback plan.

### Monitoring after release

Choose meaningful signals: journey success, integration failures, latency, queue backlog, unresolved payments, and backup age. The team should know who receives each alert and what action follows.

During an incident, contain impact, retain necessary evidence without exposing sensitive data, diagnose, restore service, and prevent recurrence. Do not turn every alert into random production changes.


For affected pooling, replicas, retry budgets, shutdown, routing, observability, text/time and delivery controls, read the relevant section of [systems lifecycle](systems-lifecycle.md).
