# Lecture Notes - Consistency vs Availability

## Overview

In this lesson, we explored the trade-off between **consistency** and **availability**. Improving responsiveness often means accepting that different parts of a system may temporarily disagree. The challenge is not deciding whether a system should be consistent or available, but determining **which workflows require stronger consistency guarantees and where temporary inconsistency is acceptable**.

This lesson builds directly on the previous lesson about **Synchronous vs Asynchronous Systems**. There, we learned how moving work out of the critical path improves responsiveness. Here, we examine the consequences of that decision.

This lesson strengthens the following CARDS principles:

- **Clarity** — Make consistency guarantees explicit.
- **Separation** — Different workflows require different guarantees.
- **Resilience** — Systems continue operating when dependencies are slow or unavailable.
- **Domain Integrity** — Critical business rules remain protected.

---

# Consistency Is a Workflow Decision

Consistency and availability are often presented as system-wide properties.

In practice, they are decisions made **per workflow**.

Instead of asking:

> Should the system be consistent?

Ask:

> Where is temporary inconsistency acceptable, and where is it not?

The answer depends on the business consequences.

---

# Cached Account Balances

Suppose a finance platform displays a customer's account balance.

Initially, every request reads directly from the database.

As traffic grows, a cache is introduced to improve performance.

Benefits:

- Faster responses
- Reduced database load
- Improved availability

The downside is that cached data may become stale.

For example:

1. The user opens the dashboard.
2. The balance is cached.
3. A payment is processed.
4. The next request returns the cached balance.

The displayed balance is now outdated.

Nothing is broken—the cache is behaving exactly as intended.

The important observation is that the guarantees have changed.

Before introducing the cache:

> The displayed balance reflected the current stored value.

After introducing the cache:

> The displayed balance reflects a recent value.

---

## Different Workflows Require Different Guarantees

Whether stale data is acceptable depends on the workflow.

Examples where temporary staleness is often acceptable:

- Dashboards
- Portfolio overviews
- Reporting

Examples where it usually is **not** acceptable:

- Approving withdrawals
- Validating available funds
- Executing financial transactions

This is an example of **Separation**.

Different workflows require different consistency guarantees.

---

## Cache Invalidation

Adding a cache is usually straightforward.

The difficult part is deciding when cached data should no longer be trusted.

Every invalidation strategy creates a different window of inconsistency.

This is also where AI-generated code deserves careful review.

An AI assistant can easily wrap a slow query in a cache, but it cannot determine how much stale data the business can tolerate.

---

# Critical Operations Need Stronger Guarantees

Consistency problems are not limited to stale reads.

Concurrent updates can also violate business rules.

Imagine an account containing €100.

Two withdrawals of €80 arrive almost simultaneously.

If both operations:

1. Read the balance
2. Check whether enough money is available
3. Update the balance

both withdrawals may be approved.

Even though neither operation used cached data.

The problem is that checking and updating happen as separate operations.

A better design protects the business rule as a single atomic operation.

The important design principle is:

> Business invariants belong inside one protected operation.

This strengthens **Domain Integrity**.

---

# Retries and Unknown Outcomes

External systems introduce another consistency challenge.

Suppose a payment provider successfully processes a transfer.

Before the confirmation reaches our platform, the network times out.

Did the transfer succeed?

We don't know.

Retrying immediately may perform the transfer twice.

Instead of assuming success or failure, the system should represent the uncertainty explicitly.

For example:

- Pending confirmation
- Awaiting provider response

Using idempotency keys also allows repeated requests to be processed safely.

The important question is:

> Is it safe if this operation happens twice?

Retries improve availability, but they also change the guarantees of the system.

---

# Asynchronous Synchronization

This lesson builds directly on the previous lesson about **Synchronous vs Asynchronous Systems**.

Asynchronous processing improves responsiveness by moving work outside the original request.

However, it also means different parts of the system no longer update simultaneously.

Consider a completed stock purchase.

The system needs to:

- Record the trade
- Update the portfolio
- Update reporting

The trade is written to the ledger immediately.

Portfolio and reporting updates happen later.

For a short period:

- The ledger is correct.
- Portfolio data is outdated.
- Reporting is outdated.

Eventually, they all agree again.

The ledger is the **source of truth**.

Portfolio views and reports are **derived views**.

Derived views often tolerate temporary inconsistency.

Authoritative data usually cannot.

The key design question becomes:

> How long can different parts of the system disagree?

The answer depends on the business consequences.

---

# CARDS Perspective

## Clarity

Make consistency guarantees visible.

Developers should understand which information is authoritative and which may temporarily lag behind.

---

## Separation

Different workflows require different consistency guarantees.

Dashboards and financial transactions should not necessarily behave the same way.

---

## Resilience

Caches, retries, and asynchronous processing improve availability when dependencies are slow or temporarily unavailable.

---

## Domain Integrity

Critical business rules require stronger consistency guarantees.

Protect important invariants with atomic operations and explicit domain states.

---

# Key Takeaways

- Consistency and availability are trade-offs, not absolutes.
- Make these decisions per workflow, not for the entire system.
- Caches improve availability but introduce stale data.
- Cache invalidation determines how long stale data can exist.
- Critical business operations require stronger consistency guarantees than read-only views.
- Concurrent updates can violate business rules even without caching.
- Retries should only be used when repeated operations are safe.
- Unknown outcomes should be represented explicitly rather than guessed.
- Asynchronous processing improves responsiveness but creates temporary inconsistency between different parts of the system.

---

# Bridge to the Next Lesson

Throughout this lesson, we looked at multiple parts of a finance platform staying in sync:

- The transaction ledger
- Portfolio views
- Reporting
- External payment providers

Keeping these components consistent requires coordination.

But how should that coordination happen?

Should one component explicitly direct every step of the process?

Or should components simply react when something important happens?

In the next lesson, **Orchestration vs Choreography**, we'll explore these two approaches to coordinating systems, when each works well, and the trade-offs they introduce.
```