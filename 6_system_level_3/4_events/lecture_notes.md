# Lecture Notes - Event-Based Architecture

## Overview

In the previous lessons, we focused on keeping the domain independent from infrastructure by using Ports & Adapters and containing concerns like concurrency at the edges of the system.

In this lesson, we address a different kind of coupling.

As applications grow, individual use cases often become responsible for coordinating an increasing number of follow-up actions. Every new feature means adding another function call to an existing workflow, making those use cases difficult to maintain.

Event-based architecture offers a different approach. Instead of explicitly coordinating every step, a use case publishes an event describing what has happened. Other parts of the system can then react independently.

The result is a system that is easier to extend without constantly modifying existing workflows.

---

# The Growing Coordination Problem

Consider the `create_transaction()` use case.

Initially it only stores a transaction:

- Store the transaction in the repository.

As the application evolves, additional requirements appear:

- Refresh spending summaries.
- Update budget status.
- Send notifications.
- Record analytics.
- Notify external systems.

Each requirement seems perfectly reasonable.

The problem is not any individual function call.

The problem is that **the use case gradually becomes responsible for coordinating the entire application**.

The same thing happens to other use cases.

For example, generating a monthly report may start to:

- Cache the report.
- Send monthly emails.
- Record metrics.
- Check budget overruns.

Eventually many use cases evolve into orchestration layers that know far too much about the rest of the system.

This increases coupling because every new feature requires modifying existing workflows.

---

# Events Represent Business Facts

An event represents something that has already happened.

Instead of saying:

> "Do this."

An event says:

> "This happened."

For example:

- `TransactionCreated`
- `MonthlySpendingReportGenerated`

This distinction is important.

Events describe completed business actions.

They do **not** describe technical implementation details.

Good event names express domain concepts.

For example:

- `TransactionCreated`

Avoid names that expose infrastructure:

- `KafkaTransactionMessage`
- `WebhookPayload`

The domain should remain independent of how events are transported.

---

# Publishing Instead of Coordinating

Instead of directly calling every follow-up workflow, the use case publishes an event.

Its responsibility becomes very small:

1. Perform the core business action.
2. Publish an event describing what happened.

The use case no longer decides:

- who receives notifications
- whether analytics are updated
- whether webhooks are sent

It simply communicates that a transaction has been created.

This keeps the application logic focused on business behavior.

---

# Event Handlers

Independent event handlers react to published events.

For example:

- update summaries
- refresh budgets
- send notifications
- send webhooks
- record analytics

Adding new functionality often becomes much easier.

Instead of modifying an existing use case, you simply introduce another handler.

This is one of the biggest practical advantages of event-driven design.

Small changes remain small.

---

# Events Fit Naturally with Ports & Adapters

Events provide another architectural boundary.

The domain owns:

- entities
- value objects
- use cases
- ports
- events

Infrastructure adapters own:

- FastAPI
- databases
- notification services
- webhooks
- analytics
- queues

The domain publishes events.

Infrastructure decides how to react.

This keeps dependencies pointing toward the business domain instead of outward toward implementation details.

---

# New Capabilities

Representing business actions as events enables capabilities that would otherwise require much tighter coupling.

## Webhooks

External systems can subscribe to events without modifying existing use cases.

For example:

- accounting software
- budgeting applications
- third-party integrations

can all react to `TransactionCreated`.

---

## Event History

An event bus can maintain a history of published events.

This creates a timeline of business actions that is useful for:

- debugging
- customer support
- auditing
- understanding system behavior

Exposing an endpoint such as:

```
GET /events
```

allows inspection of the application's event history.

---

## Replayability

Historical events also make it possible to rebuild derived state.

For example:

- regenerate spending summaries
- rebuild analytics
- recreate reports

This is related to event sourcing, although this lesson only introduces the underlying idea.

---

# Events and Concurrency

Events also work well with asynchronous processing.

A published event may eventually be handled by:

- background workers
- message queues
- asynchronous tasks
- external services

Importantly, the **domain does not need to know this**.

The application publishes an event.

Infrastructure decides:

- when it runs
- where it runs
- how it runs

This follows exactly the same principle introduced in the previous lesson:

Keep infrastructure concerns at the edges.

---

# Trade-offs

Events improve decoupling.

However, they also introduce new complexity.

Challenges include:

- workflows become less visible
- debugging becomes harder
- failures require retries
- eventual consistency may appear
- tracing complete workflows becomes more difficult

The trade-off can be summarized as:

> Events reduce coupling, but increase coordination complexity.

Neither approach is universally better.

Choose the one that best fits the problem.

---

# Common Pitfalls

## Turning everything into events

Not every interaction deserves an event.

Simple workflows are often easier to understand with direct function calls.

---

## Leaking infrastructure into the domain

Domain events should express business meaning.

Avoid naming events after specific technologies.

---

## Long chains of events

One event triggering another, which triggers another, can quickly make a system difficult to understand.

Keep event flows intentional and observable.

---

## Mixing domain and infrastructure

Do not let asynchronous infrastructure concerns spread into domain logic.

The domain should publish events.

Infrastructure decides how they are delivered.

---

# Key Takeaways

- Direct calls tightly coordinate workflows.
- Growing systems often accumulate too much orchestration inside use cases.
- Events describe completed business actions.
- Publishing events reduces coupling between workflows.
- Independent handlers make systems easier to extend.
- Events naturally support integrations, webhooks, audit history, and replayability.
- Events also introduce operational complexity and should be used deliberately.
- Event-driven architecture is a tool, not a default style.

---

# Bridge to the Next Track

This concludes the **System Designer** phase.

Throughout this phase, you've learned how to design applications that remain maintainable as they grow. You've explored architectural boundaries, state ownership, resource lifecycles, concurrency, ports and adapters, and event-based workflows. More importantly, you've developed the ability to recognize the forces that shape software systems instead of simply applying patterns.

In the **Master Designer** phase, we'll build on that foundation by focusing on the architectural trade-offs that experienced software designers face every day. Instead of asking *how* to structure software, we'll ask *why* one design decision is preferable to another under different constraints.