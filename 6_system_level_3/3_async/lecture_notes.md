# Lecture Notes - Concurrency and Keeping It Out of the Domain

## Overview

As applications grow, they naturally start doing more work concurrently. REST APIs handle multiple requests simultaneously, databases perform asynchronous I/O, and external services such as bank APIs introduce network latency.

The important design question is **not** whether to use concurrency. Modern Python applications often benefit from asynchronous execution.

The real question is:

> **Where should concurrency live?**

The key idea of this lesson is that **concurrency is primarily an infrastructure concern, not a domain concern**.

By keeping async code at the edges of the system—in adapters and orchestration layers—you preserve an application core that is easier to understand, test, and evolve.

This lesson primarily reinforces the CARDS principles of **Alignment**, **Separation**, and **Resilience**.

---

# Why concurrency becomes necessary

Our finance platform has grown considerably since the beginning of this phase.

It now contains:

- REST API endpoints
- Database access
- Report generation
- External bank integrations

These introduce situations where multiple operations may happen simultaneously:

- Several API requests arriving at once
- Database operations waiting for I/O
- Bank API requests waiting on the network
- Background synchronization jobs

These are all natural places for asynchronous execution.

The important observation is that **business rules themselves usually do not become concurrent**. Instead, concurrency appears because the system interacts with external resources.

---

# Async belongs at the edges

Within a Ports & Adapters architecture, async naturally belongs in infrastructure.

Typical examples include:

- REST API adapters
- Database adapters
- External API clients
- Background workers
- Orchestration workflows

These components coordinate execution, wait for external systems, and manage communication.

Business logic generally does none of these things.

Business logic answers questions such as:

- Is this transaction valid?
- Which transactions belong to this month?
- How much was spent in each category?

Those questions are independent of how quickly the data arrived.

---

# The danger of async leaking inward

A common design mistake is allowing the infrastructure to define the application.

Imagine that the repository port itself becomes asynchronous simply because the database driver is asynchronous.

The application use cases now also become asynchronous because they depend directly on that port.

Nothing about the business rules changed.

Only the infrastructure changed.

This creates several problems:

- Business logic becomes coupled to execution mechanics.
- Tests require asynchronous setup.
- CLI applications require an event loop.
- Infrastructure decisions shape the application layer.

This is an example of **architectural leakage**.

The problem is **not** async itself.

The problem is that an infrastructure concern has crossed the architectural boundary.

---

# Keep the application core synchronous

The application core should focus on business behavior.

Typical responsibilities include:

- Creating transactions
- Filtering transactions
- Generating spending reports
- Applying business rules

These operations do not inherently require asynchronous execution.

The application should describe **what** needs to happen rather than **how** it is executed.

Keeping the application core synchronous provides several benefits:

- Simpler business logic
- Easier testing
- Better reuse
- Independence from infrastructure decisions

The domain remains focused on solving business problems instead of coordinating execution.

---

# Async infrastructure is still valuable

Keeping the application synchronous does **not** mean avoiding async infrastructure.

A database adapter may still use an asynchronous database driver.

Likewise, an external bank API client naturally performs asynchronous network operations.

This is exactly where async belongs.

Infrastructure components know how to communicate with external systems.

The domain does not need to know those implementation details.

---

# Boundary adapters

The improved design introduces a boundary between the application core and the infrastructure.

The application depends on a **synchronous repository port**.

Behind that port sits an adapter that communicates with an asynchronous database implementation.

This reverses the dependency:

- The application does **not** adapt to the database.
- The database adapter adapts to the application.

This is one of the central ideas behind Ports & Adapters.

Infrastructure exists to satisfy the needs of the application—not the other way around.

---

# Bank synchronization

The same idea applies to the external bank integration.

The bank API client remains asynchronous because it performs network I/O.

An orchestration workflow:

1. Awaits the bank API.
2. Receives domain transactions.
3. Invokes the normal synchronous application use case.

This creates a clean separation of responsibilities.

The workflow coordinates execution.

The application performs business operations.

The domain never needs to know that the data originated from an asynchronous API call.

---

# Thin REST endpoints

REST endpoints are adapters.

Their responsibilities are to:

- Translate HTTP requests into domain objects.
- Invoke application use cases.
- Translate results into HTTP responses.

The endpoint itself may be asynchronous.

That does **not** imply that the application core should become asynchronous as well.

The endpoint coordinates.

The domain decides.

Keeping these responsibilities separate makes the architecture easier to evolve.

---

# Concurrency and shared state

Concurrency increases the importance of proper state ownership.

Potential issues include:

- Duplicate transaction imports
- Concurrent modifications
- Inconsistent reads
- Duplicate notifications

Concurrency does not create these design problems.

It simply exposes weak boundaries more quickly.

A resilient design therefore prefers:

- Immutable domain objects
- Idempotent synchronization
- Transaction boundaries
- Database constraints
- Repositories that own persistence concerns

Notice that these solutions all live at the infrastructure boundary rather than inside the business logic.

---

# AI Guardrail

AI coding assistants often over-apply async.

Without architectural guidance, they may convert every layer into asynchronous code simply because one adapter performs asynchronous operations.

A better instruction is:

> **Keep the application core synchronous. Use async only in adapters and orchestration layers.**

Architectural constraints help AI generate code that preserves the overall design instead of merely following implementation details.

---

# Practical Heuristics

Prefer async for:

- Database adapters
- External API clients
- Background jobs
- Workflow orchestration
- Web adapters

Prefer synchronous code for:

- Domain entities
- Value objects
- Business calculations
- Report generation
- Application use cases

Watch for warning signs:

- Repository ports becoming async because one adapter is async
- Async tests for ordinary business logic
- Infrastructure types appearing in application code
- Execution mechanics leaking into business rules

---

# CARDS Connection

## Alignment

The application defines the ports.

Infrastructure adapts to those ports.

Dependencies point toward the application core instead of away from it.

## Separation

Execution mechanics remain isolated from business behavior.

The domain focuses on meaning, while adapters focus on communication.

## Resilience

Concurrency concerns stay localized.

Changes to infrastructure have minimal impact on the application core.

## Clarity

Business logic remains easy to read because it is expressed in terms of business operations rather than execution mechanics.

---

# Key Takeaways

- Concurrency is primarily an infrastructure concern.
- Keep business logic synchronous whenever possible.
- Repository ports should represent application needs rather than infrastructure mechanics.
- Use boundary adapters to connect synchronous business logic to asynchronous infrastructure.
- Let orchestration coordinate concurrent workflows.
- Keep domain logic focused on business behavior.
- Give AI coding tools architectural constraints instead of asking them to "make everything async."

---

# Bridge to the Next Lesson

So far, we've focused on **where** concurrent work should execute.

The next challenge is coordination.

As systems grow, direct calls between components become increasingly limiting. In the next lesson, we'll look at how **event-based architecture** allows independently running workflows to communicate without tightly coupling the system together.