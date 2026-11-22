# Move-sensitive contracts

| When touching | Preserve and inspect |
| --- | --- |
| Errors, catch blocks, adapters | Error categories, codes, relevant messages, partial results, wrapping cause, and logging obligations. Moving across a handler or transaction can change failure behavior. Translate at the boundary that owns the external representation. |
| Retry, timeout, fallback | Repeatability assumptions, retry count/backoff, deadlines, cancellation, and which failures are terminal or unknown. Do not add recovery policies as an incidental cleanup. |
| Async work and concurrency | When work starts, required order, concurrency limits, cancellation propagation, locks with their guarded state, backpressure, and shutdown/resource cleanup. Preserve the contract's timing constraints, not exact wall-clock durations. |
| Transactions | Atomic changes, isolation assumptions, and which side of the transaction external calls occupy. A local transaction cannot roll back an external effect by itself. |
| Models and serialization | Field names, defaults, units, nullability, encoding, and stable public shape. Separate transport/storage models only where their semantics require it. Make new internal states harder to misuse without changing public behavior silently. |
| Modules and initialization | Import/export paths, registration, startup side effects, resource ownership, and disposal. Shared modules need a clear job; do not create a catch-all or rename established modules solely for style. |
| Constants/configuration | Canonical owner, units and distinct meanings, precedence, loading time, validation, and defaults. Equal values with different meanings need not be merged. Keep secrets out of client-visible settings. |

Read when a change, move or refactor touches one of these concerns. These contracts often break silently because tests exercise the happy path.
