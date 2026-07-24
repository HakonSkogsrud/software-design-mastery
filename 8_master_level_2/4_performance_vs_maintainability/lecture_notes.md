# Lecture Notes - Performance vs Maintainability

# Overview

In this lesson, we explored one of the most common design mistakes in software development: **premature optimization**.

Performance matters, but so does the ability to understand, modify, and evolve a system. Optimizing too early often adds complexity before you know whether that complexity is actually justified. The result is software that may be faster in one area, but significantly harder to change everywhere else.

The key lesson is simple:

> **Don't optimize assumptions that are still changing.**

First understand the shape of the system. Then optimize that shape once real constraints emerge.

This lesson primarily strengthens the following CARDS principles:

- **Clarity** — keeping the design understandable while it evolves.
- **Alignment** — avoiding architectural boundaries based on guesses instead of the domain.
- **Resilience** — preventing small changes from spreading throughout the system.
- **Separation** — isolating optimizations behind clear boundaries.

---

# Performance Is a Trade-Off

Every optimization comes with a cost.

That cost is usually not additional CPU time or memory—it is **additional complexity**.

Performance optimizations often introduce:

- caches
- asynchronous processing
- batching
- precomputed data
- additional services
- more specialized implementations

These techniques can dramatically improve performance, but they also make a system harder to understand and change.

As software designers, our goal is not maximum performance.

Our goal is **enough performance while preserving maintainability**.

---

# A Real Example of Premature Optimization

The lesson began with a personal story.

While building a platform that generated websites for musicians, the system was immediately split into multiple services because it was expected to scale to thousands of customers.

The architecture looked impressive:

- separate backend
- separate authentication service
- separate deployment infrastructure

The problem was simple:

There were no customers yet.

Instead of solving the immediate problem—building features and validating the product—the architecture slowed development.

Every change crossed service boundaries.

Local development became more complicated.

Deployments became more involved.

The optimization addressed a future problem while making today's work more difficult.

This is a classic example of premature optimization at the architectural level.

---

# Performance in Python Systems

When discussing performance in Python, it is important to distinguish between **language-level performance** and **system-level performance**.

If absolute CPU performance is the primary requirement, languages such as Rust or C++ are often more appropriate than Python.

Fortunately, most Python applications are not limited by Python execution speed.

Instead, performance problems usually come from:

- database access
- network communication
- disk I/O
- processing unnecessarily large datasets
- repeated work
- inefficient interactions between components

For software designers, these system-level decisions usually have a much larger impact than micro-optimizing Python code.

---

# Why Early Optimization Is Dangerous

Requirements evolve rapidly early in a project.

Business rules change.

The domain becomes clearer.

New use cases appear.

Unfortunately, this is also when optimization causes the most damage.

Performance optimizations typically make implementations more specialized.

Examples include:

- caches
- queues
- precomputed projections
- batching
- separate services

These structures often improve performance, but they also make the implementation less flexible.

There is another subtle consequence:

Optimization can hide the underlying design.

Instead of asking:

> *What determines room availability?*

developers begin asking:

> *How do we invalidate the cache?*

Instead of asking:

> *Where should this business rule live?*

they ask:

> *Which service owns this API?*

The implementation details begin driving design decisions instead of the domain.

This reduces **Clarity** and can lead to poorer architectural decisions later.

---

# Optimizing Assumptions That Are Still Changing

One of the central ideas from this lesson is:

> **Don't optimize assumptions that are still changing.**

Before optimizing, first understand:

- the domain
- the responsibilities
- the boundaries
- the workflow

Once those stabilize, optimization becomes much safer because the underlying assumptions are less likely to change.

---

# Premature Optimization in the Booking System

Consider the booking platform while it is still under development.

Suppose the team expects millions of bookings in the future.

Instead of building a single application first, they immediately create separate services:

- Booking
- Pricing
- Availability
- Customer
- Notifications

Initially this appears scalable.

However, as the domain evolves, new dependencies emerge.

Pricing depends on availability.

Availability depends on bookings.

Bookings depend on pricing.

Simple function calls become network communication.

The team now has to manage:

- APIs
- retries
- synchronization
- duplicated data
- error handling

The issue is not that microservices are inherently wrong.

The issue is introducing architectural boundaries before understanding the domain.

This weakens:

- **Alignment**, because dependencies no longer reflect the business model.
- **Resilience**, because a small change now affects multiple services.

---

# Small Optimizations Can Also Be Premature

Premature optimization is not limited to architecture.

It can also happen inside individual functions.

A straightforward implementation that clearly communicates intent is often the best solution until performance measurements indicate otherwise.

Replacing simple code with more clever constructs—whether suggested by an AI assistant or written manually—should only happen when there is evidence that the code is actually a bottleneck.

Before optimizing, ask:

- Has this code been measured?
- Is it actually slow?
- Is the improvement meaningful?
- Is the added complexity worth it?

AI coding assistants frequently optimize the code they can see without understanding the larger context.

They do not know:

- how often code executes
- how stable the requirements are
- whether readability is more valuable than small performance gains

---

# Streaming Large Exports

The lesson then demonstrated a justified optimization using generators.

The initial implementation loaded every booking into memory before exporting.

For small datasets, this approach is perfectly reasonable.

When the requirement changed to exporting millions of bookings, a generator became a better solution.

Returning an `Iterator` allows bookings to be processed incrementally rather than storing the entire export in memory.

Benefits include:

- lower memory usage
- incremental processing
- support for very large datasets

However, this optimization also changes the interface.

Unlike a list, an iterator:

- is consumed only once
- cannot be indexed
- cannot easily be reused

The optimization introduces complexity, but this time the complexity is justified by a real requirement.

Most importantly, the optimization remains localized.

Only the export interface changes.

The rest of the application remains unaffected.

This is a good example of **Separation**.

---

# Caching Availability

Caching demonstrates another important trade-off.

Suppose calculating room availability becomes expensive.

A cache can significantly improve performance.

However, introducing a cache immediately creates a new design problem:

**When is the cached data no longer correct?**

Initially, perhaps only a new booking invalidates the cache.

Later, availability may also depend on:

- cancellations
- maintenance periods
- temporary reservations
- opening hours
- staffing levels

Each new business rule expands the cache invalidation logic.

The optimization improves performance, but maintaining correctness becomes more difficult.

This affects:

- **Domain Integrity**, because stale data can produce invalid results.
- **Resilience**, because every rule change now affects cache management.

Keeping the cache behind a dedicated service boundary limits how far this complexity spreads.

---

# Choosing the Right Optimizations

Not every optimization has the same cost.

The first optimizations are often inexpensive while delivering significant improvements.

Examples include:

- removing unnecessary database queries
- adding indexes
- batching requests
- avoiding repeated work

These typically provide excellent returns.

More advanced optimizations often introduce much greater complexity.

Examples include:

- distributed caches
- background workers
- precomputed read models
- separate services

These should only be introduced when real performance constraints justify them.

The objective is not maximum performance.

The objective is software that is **fast enough** while remaining understandable and maintainable.

---

# Key Takeaways

- Performance improvements always introduce maintenance costs.
- Early in a project, optimization is particularly risky because requirements are still evolving.
- Premature optimization can obscure the underlying design and make future architectural decisions more difficult.
- Optimize only after measuring a real performance problem.
- Prefer optimizations that remain isolated behind clear boundaries.
- System-level optimizations often have a much greater impact than language-level micro-optimizations.
- Aim for software that is fast enough rather than theoretically optimal.

---

# Bridge to the Next Lesson

Performance optimizations often make software more resistant to change.

Sometimes that resistance is exactly what we want.

A stable architecture protects the system from unnecessary modifications.

Other times, stability simply slows down development and makes evolution more expensive.

In the next lesson, **Stability vs Speed of Change**, we'll explore how experienced software designers decide when stability becomes an asset—and when it becomes an obstacle.