# Lecture Notes - Orchestration vs Choreography

# Overview

In the previous lessons, we looked at ways to reduce coupling and build systems that are easier to evolve. One of the techniques we introduced was event-driven architecture, where components communicate through domain events instead of direct dependencies.

This lesson builds on that idea by exploring **two different ways of coordinating work**:

- **Orchestration**, where one component owns and coordinates a complete workflow.
- **Choreography**, where independent components react to events without a central coordinator.

Neither approach is inherently better. They solve different problems.

The goal of this lesson is to learn **where a business process should live**. Some processes need a single visible owner, while others are better expressed as independent reactions. Understanding the difference helps you design systems that remain understandable as they grow.

This lesson primarily strengthens the following CARDS principles:

- **Clarity** – important workflows remain easy to understand.
- **Alignment** – dependencies point in the right direction.
- **Resilience** – changes remain localized.
- **Domain Integrity** – business processes preserve valid state.

---

# Orchestration

Orchestration means that **one component owns the complete workflow**.

That component decides:

- which steps execute,
- in what order,
- when the process stops,
- and what happens when something fails.

The entire process is visible in one place.

## Example: Monthly Spending Report

The `generate_monthly_spending_report()` use case is an orchestrated process.

It coordinates several dependent steps:

1. Load transactions.
2. Filter the requested month.
3. Validate that transactions exist.
4. Calculate totals.
5. Build the report.

These steps are not independent.

For example:

- Totals cannot be calculated before filtering.
- The report cannot be created before validation succeeds.

Keeping these steps together makes the workflow easy to understand.

This is an example of **Clarity**.

---

# Why Not Use Events Here?

Technically, each step could publish an event.

For example:

```text
ReportRequested
→ TransactionsFiltered
→ TotalsCalculated
→ ReportGenerated
```

This would work.

However, it would not improve the design.

These steps:

- always happen together,
- do not evolve independently,
- and belong to one business operation.

Splitting them across event handlers would simply make the workflow harder to follow.

When a process naturally belongs together, orchestration is usually the better choice.

---

# Choreography

Choreography works differently.

Instead of one coordinator controlling the process, components react independently to something that already happened.

In the finance platform, creating a transaction publishes a `TransactionCreated` event.

Several handlers react independently:

- refresh the budget,
- send a notification,
- send a webhook.

Conceptually:

```text
TransactionCreated
├── Refresh budget
├── Send notification
└── Send webhook
```

Notice that none of these handlers controls transaction creation.

The transaction already exists.

Each handler simply reacts to a meaningful domain fact.

This is choreography.

---

# When Choreography Works Well

Choreography is most useful when reactions are **independent consequences**.

Characteristics include:

- reactions do not depend on each other,
- ordering is unimportant,
- new reactions can be added easily,
- the producer does not need to know its consumers.

Examples include:

- updating analytics,
- refreshing read models,
- sending emails,
- publishing webhooks,
- logging.

This supports several CARDS principles:

### Separation

The transaction use case remains focused on creating transactions.

It does not contain notification or integration logic.

### Resilience

Adding another consumer usually requires only a new event handler.

Existing code remains unchanged.

---

# The Trade-Off

Event-driven systems are often described as "decoupled."

That is only partly true.

Direct coupling is reduced.

However, a different form of coupling appears.

All consumers now depend on the event contract.

For example:

```python
TransactionCreated(
    transaction_id,
    category,
    amount,
    currency,
    ...
)
```

Changing this event may affect:

- budget calculations,
- notifications,
- webhooks,
- analytics,
- external integrations.

The coupling has not disappeared.

It has moved from direct method calls to shared contracts.

---

# Organizational Coordination

As systems grow, event contracts become shared agreements between teams.

Imagine different teams own:

- transaction creation,
- notifications,
- analytics,
- budgeting,
- webhooks.

Changing one event schema now requires communication between multiple teams.

This illustrates an important architectural principle:

> Technical coupling may decrease while organizational coordination increases.

Architecture affects both software and teams.

---

# A Common Design Smell

One warning sign is event handlers publishing additional events that trigger the next handler.

For example:

```text
TransactionSubmitted
→ TransactionValidated
→ DuplicateCheckPassed
→ FraudCheckPassed
→ TransactionCreated
```

Each handler performs one step before publishing another event.

Nothing is technically incorrect.

However, this creates an important question:

Are these really independent reactions?

Usually, the answer is no.

These steps have become one ordered workflow.

The choreography is hiding an orchestrated process.

---

# Why Hidden Workflows Are Problematic

When a workflow is spread across event handlers:

- no single place describes the process,
- debugging becomes more difficult,
- ordering becomes implicit,
- failures become harder to trace.

For example:

If `TransactionCreated` never occurs:

- Did validation fail?
- Did duplicate checking fail?
- Did fraud detection fail?
- Did one event never get published?

Understanding the system now requires following a chain of events.

This reduces **Clarity**.

It can also reduce **Resilience**, because changing one step may affect an invisible workflow.

---

# Making the Process Explicit

A better design is to explicitly coordinate the business process.

For example, a `TransactionImportWorkflow` can perform:

1. validation,
2. duplicate checking,
3. fraud checking,
4. persistence,
5. publishing `TransactionCreated`.

The important distinction is that the event is published **after** the process completes successfully.

This combines both approaches:

```text
TransactionImportWorkflow
├── Validate
├── Check duplicates
├── Fraud check
├── Persist
└── Publish TransactionCreated

TransactionCreated
├── Refresh budget
├── Send notification
└── Send webhook
```

The workflow is orchestrated.

The independent consequences are choreographed.

---

# Stripe's PaymentIntent

Stripe provides an excellent real-world example of orchestration.

A payment moves through a lifecycle:

```text
requires_payment_method
→ requires_action
→ processing
→ succeeded
```

The `PaymentIntent` owns that lifecycle.

It coordinates:

- payment state,
- authentication,
- retries,
- completion.

Stripe also emits webhook events.

However, those events do not coordinate the payment process.

Instead, they notify external systems that something meaningful has already happened.

For example:

- fulfil an order,
- send a confirmation email,
- update inventory.

The distinction is important:

- **PaymentIntent orchestrates the process.**
- **Webhooks choreograph the reactions.**

---

# Choosing Between Orchestration and Choreography

Prefer **orchestration** when:

- steps belong to one business process,
- ordering matters,
- failures should stop the workflow,
- the process has meaningful state,
- the workflow should be easy to understand.

Prefer **choreography** when:

- reactions are independent,
- consumers evolve separately,
- adding new consumers should not change the producer,
- something meaningful has already happened.

---

# Practical Questions

Before introducing events, ask yourself:

- Is this a business process or a consequence?
- Does the order of execution matter?
- Should failure stop later steps?
- Are these components truly independent?
- Who owns the event contract?
- Could this become a hidden workflow?
- Would one explicit coordinator make the system easier to understand?

These questions are usually more important than the choice of messaging technology.

---

# Key Takeaways

- Orchestration gives one component responsibility for a workflow.
- Choreography lets components react independently to meaningful events.
- Orchestration improves workflow visibility.
- Choreography improves extensibility and separation.
- Event-driven systems reduce direct coupling but introduce shared contracts.
- Event handlers repeatedly publishing new events can indicate a hidden workflow.
- Many systems benefit from combining both approaches.
- The goal is not to eliminate coupling—it is to place coordination where it is easiest to understand and evolve.

---

# Bridge to the Next Lesson

This lesson showed that architectural decisions rarely remove complexity—they move it.

Orchestration improves visibility but introduces direct dependencies.

Choreography reduces direct dependencies but introduces coordination through shared contracts and event-driven communication.

The same pattern appears when optimizing software performance.

Caching, batching, asynchronous processing, denormalized data, and precomputed results can make a system significantly faster, but they also introduce new complexity and maintenance costs.

In the next lesson, **Performance vs Maintainability**, we'll explore how to balance those competing forces without sacrificing the long-term health of the system.