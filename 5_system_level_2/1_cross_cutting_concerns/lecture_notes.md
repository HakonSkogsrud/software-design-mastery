# Lecture Notes - Dealing with Cross-Cutting Concerns

# Overview

In this lesson, we explored **cross-cutting concerns**: functionality that is needed throughout an application but is not part of the application's core business logic.

Using the personal finance platform as an example, we focused on **logging**, one of the most common cross-cutting concerns in software systems. We examined several ways of incorporating logging into an application, discussed the trade-offs of each approach, and learned that the real design question is not *whether* to use globals or dependency injection, but **who should own a cross-cutting concern**.

Along the way, we connected these ideas to the CARDS principles, particularly **Alignment**, **Separation**, **Clarity**, and **Domain Integrity**.

---

# What Is a Cross-Cutting Concern?

A cross-cutting concern is functionality that supports many parts of a system without being part of its core business logic.

Typical examples include:

- Logging
- Configuration
- Metrics and monitoring
- Authentication and authorization
- Caching
- Tracing and request IDs
- Feature flags

These concerns often appear throughout an application, regardless of which business feature is being implemented.

For example, transaction importing, report generation, and budget notifications may all need logging, even though logging is not their primary responsibility.

This widespread use is what makes cross-cutting concerns both useful and potentially dangerous.

---

# Why Cross-Cutting Concerns Matter

The difficulty is not that cross-cutting concerns are shared.

The difficulty is **how they become shared**.

A poor design allows infrastructure concerns to spread through the application until almost every component depends on them.

As more components become coupled to shared infrastructure, changes become harder to isolate and the overall architecture becomes more difficult to understand.

---

# Option 1 — Global Access

The simplest solution is to expose the concern globally.

For example, many applications have a globally accessible logger that can be used from anywhere.

Advantages:

- Very little setup
- Minimal boilerplate
- Easy to use
- Works well for small applications

Disadvantages:

- Dependencies become invisible
- Components quietly rely on global infrastructure
- Testing becomes more difficult
- Configuration changes affect many parts of the system

Although the method signatures appear simple, they hide an important dependency: the logger.

This weakens **Clarity**, because readers cannot immediately see what a component depends on.

---

# Why Logging Becomes More Complex

Logging often begins with simple messages:

- Import started
- API call completed
- Synchronization finished

As systems grow, however, logging usually needs additional context:

- Request IDs
- User IDs
- Job IDs
- Source systems
- Execution time
- Error details

At that point, logging becomes an architectural concern rather than just a utility.

Questions naturally arise:

- Where does this information come from?
- Who owns it?
- How is it replaced during testing?
- How do background jobs differ from web requests?

These are design questions rather than implementation details.

---

# Option 2 — Passing Dependencies Explicitly

Instead of relying on global state, the logger can be passed explicitly through the workflow.

This makes the dependency visible at every point where it is required.

Benefits:

- Dependencies are obvious
- Tests can substitute fake implementations
- Different workflows can use different logging configurations
- Hidden coupling disappears

This improves:

- **Clarity**
- **Testability**
- **Alignment**

However, another problem appears.

The logger must now be threaded through multiple method calls, even when intermediate components merely forward it.

This creates **parameter plumbing**.

The dependency is explicit, but the code becomes noisier.

---

# Explicit Does Not Always Mean Better

Making every dependency explicit is not automatically the best design.

Passing a logger through an entire call chain can lead to interfaces that primarily exist to forward infrastructure concerns.

This raises an important architectural question:

**Does this component actually own the dependency, or is it merely passing it along?**

Ownership matters more than visibility alone.

---

# Option 3 — Let Workflow Components Own the Concern

Instead of passing the logger everywhere, a workflow-level component can own it.

In the finance application, the `TransactionSynchronizer` is responsible for coordinating imports.

Because it owns the synchronization workflow, it also makes sense for it to own the logging related to that workflow.

Advantages:

- Less parameter plumbing
- Clear ownership
- Logging stays close to the workflow
- Domain components remain simpler

This strengthens:

- **Alignment**, because infrastructure belongs to the application layer.
- **Separation**, because domain objects remain focused on business concepts.

---

# Option 4 — Partial Application

Sometimes a function legitimately depends on a cross-cutting concern, but repeatedly passing the same arguments becomes tedious.

Python's `functools.partial()` allows a function to be configured once and reused later.

This offers several benefits:

- Configuration happens at the application boundary.
- The dependency remains explicit.
- Repetitive wiring is reduced.
- Functions remain reusable.

Partial application provides a lightweight way of managing dependencies without introducing global state.

Like any tool, however, it should be used thoughtfully.

Too much hidden configuration can reduce readability.

---

# Option 5 — Focused Context Objects

When several related cross-cutting concerns frequently appear together, they can be grouped into a context object.

Examples include:

- Logger
- Import configuration
- Request ID
- Job ID

A focused context object can simplify method signatures while still keeping dependencies visible.

The key word is **focused**.

A context should represent the needs of a specific workflow or boundary.

---

# The Danger of Giant Context Objects

Context objects often begin with just a few fields.

Over time, they may accumulate:

- Database connections
- Cache clients
- Email services
- Metrics collectors
- Current user information
- Feature flags

Eventually, everything depends on the context.

At that point, the context object has effectively become another form of global state.

The hidden coupling has returned.

A useful rule of thumb is:

> A context object should represent a workflow, not the entire application.

---

# Keep Cross-Cutting Concerns Out of the Domain

One of the most important architectural boundaries is the domain model.

Domain objects should represent business concepts.

For example, a `Transaction` should contain financial information.

It should **not** know:

- How to log
- How to send metrics
- Who the current user is
- Which request is being processed

Infrastructure concerns belong around the domain, not inside it.

This protects **Domain Integrity** by preventing infrastructure from leaking into business logic.

---

# AI Guardrail

AI coding assistants often favor convenience.

They frequently generate solutions that import globally available services because this minimizes the amount of code required.

While these solutions often look clean locally, they may quietly introduce hidden coupling throughout the application.

When working with AI tools, it is worth asking:

- Who owns this concern?
- Is this dependency explicit?
- Does this belong in the domain model?
- Am I introducing unnecessary global state?

Good architecture helps prevent both human and AI-generated design mistakes.

---

# Design Guidelines

When introducing a cross-cutting concern, ask yourself:

- Is it really needed everywhere?
- Does it require request-specific context?
- Will tests need to replace it?
- Does the domain actually need to know about it?
- Should a workflow component own it?
- Would a focused context object improve clarity?
- Am I accidentally recreating global state?

Rather than asking:

> "Should this be global?"

ask:

> "Who should own this concern?"

Ownership is usually the most valuable design question.

---

# CARDS Connections

### Clarity

Making dependencies visible helps readers understand how components interact.

### Alignment

Infrastructure concerns should be owned by application workflows rather than leaking into the domain.

### Separation

Business logic and infrastructure should remain distinct responsibilities.

### Domain Integrity

Domain objects should model business concepts without depending on logging, metrics, configuration, or other infrastructure concerns.

---

# Key Takeaways

- Cross-cutting concerns support many parts of a system.
- Logging is one of the most common examples.
- Global access is convenient but hides dependencies.
- Passing dependencies explicitly improves visibility but can create parameter plumbing.
- Workflow-level components often provide a better ownership boundary.
- Partial application reduces repetitive wiring while keeping dependencies explicit.
- Context objects should remain focused on a specific workflow.
- Giant context objects often become hidden globals.
- Keep infrastructure concerns out of the domain model.
- Good architecture is primarily about assigning ownership intentionally.

---

# Bridge to the Next Lesson

Cross-cutting concerns often involve shared data such as configuration, caches, exchange rates, or synchronization status.

Once multiple parts of a system begin reading and modifying the same information, another important design question appears:

**Who actually owns that state?**

In the next lesson, we'll explore how shared mutable state creates new forms of coupling, and how clear ownership helps prevent synchronization problems as systems continue to grow.