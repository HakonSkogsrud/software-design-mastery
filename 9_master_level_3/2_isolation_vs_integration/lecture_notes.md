# Lecture Notes - Isolation vs Integration

## Overview

As software systems grow, one of the most important architectural decisions is whether different parts of the system should remain integrated or be isolated into separate services.

This is often framed as the choice between a **monolith** and **microservices**, but that framing is too simplistic. The real design question is:

> **Which parts of the system should evolve together, and which should evolve independently?**

This lesson explores the trade-off between **Integration** and **Isolation**, discusses when microservices are beneficial, explains why many teams accidentally build distributed monoliths, and shows why a **modular monolith** is often the best place to start.

---

# A Personal Lesson

When building a website builder for musicians, I made a mistake that many teams still make today.

We immediately adopted a microservice architecture. We separated payment handling, authentication, and other functionality into individual services before we really understood the product.

Looking back, this was the wrong decision for two reasons:

- We simply didn't need separate services yet. The additional operational complexity slowed down development.
- Some of the service boundaries weren't based on business capabilities. Authentication, for example, was used throughout the application, making it a poor candidate for an isolated service.

Instead of making the system easier to evolve, we made everyday development more difficult.

The lesson is simple:

> Don't isolate parts of your system before you have a good reason to do so.

---

# Integration vs Isolation

Imagine our booking platform has grown significantly.

Different teams now work on:

- Reservations
- Payments
- Notifications
- Reporting

The architectural question becomes:

- Should everything remain one application?
- Or should these become separate services?

This is the trade-off between:

- **Integration** — keeping components together.
- **Isolation** — allowing components to evolve independently.

Neither approach is inherently better. The correct choice depends on how the system changes over time.

---

# Starting with a Modular Monolith

A common misconception is that a monolith must be poorly organized.

A **modular monolith** is a single application with clearly separated modules:

```text
booking/
├── reservations/
├── payments/
├── notifications/
└── reporting/
```

Everything still runs:

- in one deployment
- in one process
- typically against one database

However, the internal architecture already has clear boundaries.

### Benefits

- Simple deployment
- Simple debugging
- Straightforward transactions
- Clear internal organization
- Lower operational complexity

From the CARDS perspective:

- **Clarity**: related functionality lives together.
- **Alignment**: dependencies remain straightforward.
- **Domain Integrity**: transactions can maintain consistent state.

For many applications, this architecture remains sufficient for years.

---

# When Growth Creates Pressure

As applications grow, different modules begin to evolve differently.

Examples:

- Reporting performs heavy analytical workloads.
- Marketing frequently changes notification workflows.
- Payments require regulatory compliance.
- Reservations remain the core transactional workflow.

These differences create pressure to isolate certain parts of the system.

Good reasons to isolate include:

- Different teams own the component.
- Different release schedules.
- Different scaling requirements.
- Different availability requirements.
- Different regulatory constraints.

The motivation should come from the business—not from architectural trends.

---

# Microservices

Splitting the system into separate services provides several benefits.

Potential advantages include:

- Independent deployments
- Independent scaling
- Better fault isolation
- Clear ownership by different teams

However, every service boundary introduces additional complexity.

Instead of local function calls, communication now involves:

- Network requests
- Authentication
- Timeouts
- Retries
- Monitoring
- Version compatibility
- Failure recovery

This complexity is often underestimated.

---

# The Distributed Monolith

One of the most common architectural mistakes is the **distributed monolith**.

This occurs when an application has been split into multiple services, but those services still need to evolve together.

Typical symptoms include:

- Every feature touches multiple services.
- Deployments must be coordinated.
- API changes ripple throughout the system.
- Teams cannot work independently.
- Small changes require large integration efforts.

Although the code is physically separated, the coupling remains.

As a result, the organization experiences:

- the operational complexity of microservices
- without the independence that microservices are supposed to provide

In many cases, this is worse than a well-designed monolith.

---

# Shared Databases

A common cause of distributed monoliths is a shared database.

For example:

```text
Reservation Service
        │
        ▼
 Shared Database
        ▲
        │
Payment Service
```

This creates several problems.

Any service can:

- modify another service's data
- introduce breaking schema changes
- affect the performance of unrelated services

As a result, service boundaries become meaningless.

A useful principle is:

> **A service doesn't truly own a capability if another service writes directly to its database.**

True isolation requires ownership of both:

- behavior
- data

---

# Modular Boundaries

One advantage of a modular monolith is that architectural boundaries can already exist before deployment boundaries do.

Modules communicate through abstractions rather than concrete implementations.

For example, a reservation module may depend on a `PaymentGateway` interface instead of directly depending on Stripe.

This improves:

- flexibility
- testability
- future evolution

If payments eventually become a separate service, much of the structural work has already been completed.

The goal is not to design for microservices.

The goal is to design for change.

---

# Choosing the Right Boundaries

Rather than asking:

> Can this become its own service?

Ask:

> Does this actually evolve independently?

Some components naturally evolve independently.

Examples include:

- Reporting
- Analytics
- Recommendation systems

Other components are tightly connected.

Examples include:

- Reservations
- Payments
- Inventory allocation

If two components almost always change together, separating them often increases coordination rather than reducing it.

A useful heuristic is:

> **If two parts of the system usually change together, they probably belong together.**

Architecture should optimize for how the business evolves—not for the number of services.

---

# AI and Architectural Decisions

Modern AI tools can generate a microservice architecture in seconds.

Creating service boundaries has become much easier.

Choosing the correct boundaries has not.

AI does not understand:

- how your teams collaborate
- how frequently features cross module boundaries
- organizational constraints
- operational costs
- long-term maintenance

As AI lowers the cost of introducing architectural complexity, careful design becomes even more valuable.

Good software architecture protects systems from both human and AI-generated mistakes.

---

# Key Takeaways

- Integration and isolation are competing architectural forces.
- More services do not automatically produce a better architecture.
- Start with a modular monolith whenever possible.
- Isolate business capabilities rather than technical utilities.
- A service should own both its behavior and its data.
- Avoid shared databases between services.
- Watch out for distributed monoliths—many services that still change together.
- Design boundaries around how the business evolves, not around architectural trends.

---

# CARDS Connections

This lesson reinforces several parts of the CARDS framework.

### Alignment

Dependencies should point in the correct direction, and service boundaries should reflect real business capabilities.

### Separation

Components should remain isolated only when they genuinely benefit from independent evolution.

### Resilience

Good boundaries reduce the impact of change and prevent modifications from spreading throughout the system.

### Domain Integrity

Keeping closely related workflows together often makes it easier to preserve consistency.

---

# Bridge to the Next Lesson

Architectural boundaries don't just affect maintainability—they also influence how we ensure software behaves correctly.

As systems become more distributed, validating changes, testing workflows, and maintaining consistency becomes increasingly difficult.

In the next lesson, **Correctness vs Delivery Speed**, we'll explore how experienced software designers decide how much verification, testing, and review is enough before shipping software, and why the fastest path to production isn't always the fastest path in the long run.