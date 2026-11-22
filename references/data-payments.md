# Data consistency, history, and payments

## Data, transactions, and history

### General data rules

- Enforce critical constraints at a trusted boundary, using appropriate database constraints when they protect the invariant.
- Define what must succeed or roll back together. One successful step does not establish complete success.
- Handle concurrency using engine/contract-appropriate conditional updates, locks, or uniqueness constraints; verify actual behavior.
- Define currency, units, rounding, and time zones. Avoid numeric representations that cause unacceptable financial precision loss.
- Separate source input, computed result, and explanation; retain enough provenance to trace numbers.
- A few records do not prove query efficiency or migration correctness.

### Prices, invoices, and subscriptions

Store transaction-time unit price, quantity, discount, applicable tax, currency, total, and appropriate references on the order/invoice. Rendering an old invoice must not depend on today's product price.

The current catalog price may change while historical transactions remain correct. Subscriptions/agreements needing stable tariffs require plan/price versions, effective dates, and explicit treatment of existing subscribers. Do not create a plan version for every cosmetic edit without financial meaning.

For rewards, retain source event, grant identity, and rule version where needed. Decide whether a new rule affects only future events or reevaluates history, including user rights and event records.

**Acceptance evidence:** changing today's price leaves old invoices intact; processing the same event twice does not duplicate points; rerunning a scheduled job does not create unintended rewards.

### Inventory and reservations

When inventory decreases is a business decision: reservation, payment confirmation, or shipment may fit. Define reservation expiry, release on cancel/timeout, quantity limits, and payment confirmation arriving after reservation expiry.

Do not read available stock and then decrement without concurrency protection. Test two requests competing for the final item, repeated cancellation, payment failure, and delayed payment messages. The requirement is the inventory invariant, not always adding a lock.

### Accounting integration and generated reports

For an ERP/accounting integration (for example Odoo), distinguish source-data collection, metric calculation, and natural-language reporting. Implement defined accounting rules/calculations reproducibly; use the model for explanation/summary with figures tied to sources.

Generated prose is neither the accounting ledger nor sufficient evidence of correctness. Record reporting period, extraction time, source record/import batch IDs, and calculation-rule version. Define missing-data, currency, late-adjustment, and company-isolation policies.

Reconcile totals and detail samples against the source. Test repeated sync and mid-batch failure. Sharing one company's report with another is an authorization defect even if calculations are correct.

## Design payment failures before release

Implementation follows the chosen provider's versioned contract.

### Payment invariants

1. An order has a stable internal operation ID traceable to the provider operation.
2. Retrying the same logical operation does not create another financial effect.
3. UI state or a return-page URL alone cannot establish success.
4. Represent an unknown result instead of forcing every outcome into success/failure.
5. State transitions prevent duplication and erroneous backward transitions.
6. Detect and reconcile local/provider disagreement.

### Illustrative states

```text
created -> pending -> succeeded
                  -> failed
                  -> canceled
                  -> unresolved -> verify/reconcile -> confirmed outcome

succeeded -> refund_pending -> refunded or partially_refunded
```

These are illustrative names, not ready-made API states. Map to provider states and distinguish authorization, capture, and settlement where its contract does. Give unresolved outcomes a follow-up deadline, alert, and owner.

### Failure and acceptance matrix

| Situation | Required behavior | Evidence |
| --- | --- | --- |
| Double click or page reload | Associate retries with the same operation under its contract. | One financial effect and one confirmed order. |
| Connection lost after submission | Do not infer failure or blindly charge again. | Trusted provider query/event establishes the result. |
| Response timeout | Pending/unknown state with follow-up. | Correct transition after delayed confirmation. |
| Insufficient funds or final rejection | Understandable result without unjustified repeat requests. | Classified rejection and no unintended charge. |
| Duplicate webhook | Deduplicate delivery and business effect safely. | No duplicate order, credit, or reward. |
| Out-of-order events | Do not rely solely on arrival order. | An older event cannot incorrectly replace confirmed state. |
| Server failure after provider success | Reconcile disagreement. | Recover state without a new charge. |
| Failure after recording event, before processing completes | Resume without losing the event or duplicating its effect. | Restart completes one logical operation. |
| Successful payment, failed order persistence | Detect inconsistency and execute a designed remedy. | Customer has an order or a clear explanation and follow-up. |
| Partial or repeated refund | Track amounts and refund-operation identities. | Total refunded does not exceed the permitted amount. |

### Idempotency and event handling

[Stripe's idempotent-request documentation](https://docs.stripe.com/api/idempotent_requests) describes retry semantics under that API. For another provider, verify key scope, retention, and error behavior rather than transferring Stripe assumptions.

A fresh key for every retry is insufficient: key identity must follow the logical operation under the provider contract. Local concurrency controls must also prevent one purchase intent creating separate operations.

[Stripe's webhook documentation](https://docs.stripe.com/webhooks) describes duplicate delivery, unordered events, signature verification, and event selection. Use durable receipt, processing state, business-effect deduplication, and asynchronous processing where justified. Arrival alone does not guarantee exactly-once execution.

With a queue, acknowledge only after sufficiently durable receipt under the delivery contract. Processing must remain retryable after verified/recorded receipt followed by a crash. A unique event ID must not cause a received-but-unprocessed event to be discarded.

### Fees, limits, and external effects

A transfer can pass one check and then breach another once fees apply; make rule order explicit.

Define whether daily limits include fees, required available funds, and concurrent limit consumption. Check prerequisites before an external effect where possible, then preserve consistency/reconciliation through partial failure.

Prechecking alone does not remove concurrency races. A local database transaction cannot automatically roll back an external provider call. Design failure states, compensation, status queries, and reconciliation instead of assuming one transaction covers the entire internet.
