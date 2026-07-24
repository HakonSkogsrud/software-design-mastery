# Lecture Notes - Synchronous vs Asynchronous Systems

## Overview

In this lesson, we explored one of the most important architectural decisions in software systems: **should work happen synchronously or asynchronously?**

Although this often appears to be a technical implementation choice, it fundamentally changes how a system behaves. Once work no longer finishes during the original request, the system must explicitly model waiting, communicate progress, and deal with failures that happen after the caller has already received a response.

The examples in this lesson use a finance platform, but the principles apply to virtually every modern application.

---

# Synchronous vs Asynchronous

A **synchronous** operation completes before returning a result.

The caller waits until the work has finished.

```text
Request
   │
   ▼
Work completes
   │
   ▼
Response
```

An **asynchronous** operation accepts the work first, but the final result becomes available later.

```text
Request
   │
   ▼
Work accepted
   │
   ▼
Response (Pending)
   │
   ▼
Work completes later
```

> **Important:** This lesson is **not** about Python's `async` and `await`.

`asyncio` is a Python mechanism for concurrency. It allows a single process to make progress on multiple tasks while waiting for I/O.

The architectural trade-off discussed here is different:

> **Does the business operation complete before the request returns, or afterwards?**

You can build:

- synchronous systems using `asyncio`
- asynchronous systems without `asyncio`

The architectural behavior is what matters.

---

# The Synchronous Transfer

The lesson began with a straightforward money transfer.

The system:

1. moves the money
2. sends a confirmation
3. refreshes portfolio positions
4. returns success

Benefits:

- Easy to understand
- Easy to debug
- Immediate result
- Immediate consistency

From the CARDS perspective, this provides excellent **Clarity** because the complete execution flow is visible.

However, every dependency becomes part of the critical path.

If one dependency is slow or unavailable, the user must wait.

---

# When Synchronous Stops Fitting

Suppose the destination account belongs to another bank.

The transfer might take minutes—or even hours—to complete.

Keeping the original request open is no longer practical.

Instead, the system accepts the request and creates a transfer in the `PENDING` state.

```text
Request
   │
   ▼
Transfer accepted
(Status = Pending)
   │
   ▼
Background processing
```

The important architectural change is **not the queue**.

The important change is that the business operation itself is now incomplete.

The domain model must reflect that reality.

This protects **Domain Integrity**.

A transfer should never be reported as completed if the money has not yet moved.

---

# Delayed Results

Once work finishes later, the system behaves differently.

Instead of returning a final result immediately, it returns an operation that is still in progress.

That raises new design questions:

- What should the user interface display?
- Can users refresh the current status?
- Can they cancel the operation?
- What does customer support see?
- What happens if processing eventually fails?

These questions arise because the system must now manage the lifecycle of work that continues after the original request has ended.

---

# Eventual Consistency

Delayed processing also introduces **eventual consistency**.

Different parts of the system may temporarily contain different views of reality.

For example:

- the transfer request has been accepted
- the money has not moved yet
- reporting has not been updated
- the confirmation email has not been sent

Eventually, everything converges to the correct state.

This is called **eventual consistency**.

Whether this is acceptable depends entirely on the business.

Examples:

Usually acceptable:

- delayed notification emails
- delayed reporting
- delayed analytics

Often unacceptable:

- incorrect account balances
- incorrect transfer status
- duplicate financial transactions

A useful question to ask is:

> **Which parts of the system are allowed to be temporarily out of date?**

---

# Events Naturally Reappear

Earlier in the program, events were introduced to reduce coupling.

In asynchronous systems, they also solve another problem.

The original request has already finished.

So how does the rest of the system know that the transfer completed?

The transfer processor publishes a `TransferCompleted` event.

Other components react independently.

For example:

- send confirmation email
- refresh portfolio positions
- update reporting

This provides two important benefits:

- low coupling
- no direct dependency on the original request

The transfer processor simply announces:

> "The transfer completed."

It does not need to know who is interested.

This strengthens **Separation**.

---

# Asynchronous Does Not Mean Queue

One of the most common misconceptions is that asynchronous always means:

- message queues
- workers
- event buses

Not necessarily.

Consider account activation.

A customer submits identification documents.

A compliance officer manually verifies them.

Only then does the account become active.

No queue is involved.

Yet the process is still asynchronous because the result becomes available later.

Other examples include waiting for:

- another bank
- a payment provider
- customer input
- manual approval

The defining characteristic is **waiting**, not the implementation technology.

---

# Workflows

Long-running processes often become explicit workflows.

A workflow coordinates multiple steps that may involve:

- software
- external systems
- manual approval

Instead of pretending everything happens inside one request, the workflow explicitly models the lifecycle of the business process.

---

# The Trade-Off

## Synchronous

Advantages

- Immediate results
- Easier reasoning
- Easier debugging
- Easier testing
- Fewer operational components
- Strong immediate consistency

Disadvantages

- Users wait
- Slow dependencies delay requests
- Long-running operations become difficult

---

## Asynchronous

Advantages

- Faster responses
- Better resilience
- Easier retries
- Supports long-running work
- Supports manual workflows
- Independent scaling

Disadvantages

- Pending states
- Delayed failures
- Status tracking
- Eventual consistency
- Operational complexity
- More infrastructure

Neither approach is universally better.

The execution model should match the business process.

---

# Operational Complexity

Asynchronous systems often appear deceptively simple.

Publishing a message may only require one line of code.

Operating that system reliably is a different challenge.

Typical operational concerns include:

- workers
- monitoring
- retries
- dead-letter queues
- idempotency
- replay tools
- message versioning

Modern AI tools make generating this infrastructure easy.

Operating it successfully over time remains a human architectural responsibility.

---

# AI and Architecture

AI coding assistants frequently recommend introducing queues, workers, and event-driven processing.

Those suggestions may be technically correct.

However, AI cannot answer business questions such as:

- Should this operation be pending?
- Should users wait?
- Is eventual consistency acceptable?
- Which state should be shown to the customer?

Those decisions require architectural judgment.

AI can generate infrastructure.

Architects decide whether that infrastructure reflects the business correctly.

---

# CARDS Reflection

## Clarity

Synchronous execution is generally easier to follow.

Asynchronous systems require explicit states and visible workflows.

---

## Alignment

The execution model should reflect the real business process.

If work takes time, the design should communicate that honestly.

---

## Resilience

Asynchronous processing isolates slow or failing dependencies.

However, it introduces new failure modes that must be managed.

---

## Domain Integrity

Pending work should be represented as pending.

The domain should never claim unfinished work is complete.

---

## Separation

Events allow components to react independently after work completes.

Workflows separate the lifecycle of the process from the original request.

---

# Key Takeaways

- Synchronous systems return a result after the work finishes.
- Asynchronous systems return before the work finishes.
- This lesson is about delayed business operations, **not** Python's `asyncio`.
- The biggest consequence of asynchronous execution is **waiting**.
- Waiting introduces pending states, eventual consistency, and new architectural responsibilities.
- Event-driven architecture naturally complements asynchronous processing.
- Workflows coordinate long-running processes across software and people.
- AI can generate asynchronous infrastructure, but architectural decisions remain your responsibility.
- Choose the execution model that best matches the business process—not the newest technology.

---

# Bridge to the Next Lesson

In this lesson, we deliberately chose where temporary inconsistency was acceptable by introducing asynchronous processing.

In distributed systems, however, that choice is not always entirely under our control.

When networks fail or services become unavailable, we may be forced to choose between keeping the system available and keeping every piece of data perfectly consistent.

In the next lesson, we'll explore one of the most fundamental trade-offs in distributed systems: **Consistency vs Availability.**