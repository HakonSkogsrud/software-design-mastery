> Don't read any further until you tried coming up with a solution yourself!

# Solution & Analysis

## Overview

The main challenge in this exercise was **not** removing a global logger. The real challenge was deciding **who should own the logging concern**.

Logging is a classic example of a **cross-cutting concern**: it supports many parts of the application, but it is not part of the warehouse domain itself.

A good solution makes that ownership explicit while keeping the domain model focused on warehouse operations.

---

# The Problem with the Original Design

The starting point used a globally accessible logger that every component imported directly.

This has some immediate advantages:

- Very little setup
- Clean-looking method signatures
- Easy to add logging anywhere

However, it also creates hidden dependencies.

For example, the `InventoryService` appears to depend only on its method parameters, but in reality it also depends on:

- the global logger
- the logging configuration
- any handlers attached to that logger

None of those dependencies are visible in its interface.

As more components adopt the same pattern, the application's structure becomes increasingly difficult to understand.

---

# Making Dependencies Visible

One obvious improvement is to remove the global logger and pass it explicitly.

While this improves visibility, it often creates another problem:

```text
workflow(...)
↓
inventory.reserve(logger)
↓
route_planner.calculate(logger)
↓
robot_gateway.dispatch(logger)
```

The logger is no longer hidden, but it now flows through almost every method call.

This is often referred to as **parameter plumbing**.

Although explicit dependencies are generally preferable to hidden ones, passing infrastructure through the entire call chain is rarely the best long-term design.

---

# Ownership Matters More Than Visibility

The key design question is not:

> Should I use globals?

Instead, it is:

> Who actually owns this concern?

In the solution, the logging responsibility belongs to the **workflow coordinator**:

```text
PickingOperation
```

This class coordinates the entire picking operation, making it the natural place to:

- log the start and end of the operation
- record metrics
- include operation IDs
- provide execution context

This keeps the logging close to the workflow that it describes.

---

# Why the Services No Longer Log

Notice that classes such as:

- `InventoryService`
- `RoutePlanner`
- `RobotGateway`
- `TaskRepository`

no longer perform logging.

Instead, they simply perform their own responsibilities.

For example:

- reserve inventory
- calculate routes
- dispatch robots
- store tasks

This separation makes each component easier to understand and easier to test.

If logging behavior changes, these services remain unchanged.

---

# Keeping the Domain Clean

The domain objects remain extremely simple:

- `PickingTask`
- `Route`

Neither object knows anything about:

- logging
- metrics
- request IDs
- operation IDs

This protects **Domain Integrity**.

The domain models warehouse concepts rather than infrastructure.

---

# OperationContext Has a Single Purpose

The solution introduces:

```text
OperationContext
```

Unlike a large application context, this object contains only information that changes per execution:

- operation ID
- initiating user

This is an example of a **focused context object**.

Its purpose is to represent one execution of the workflow.

It does **not** become a container for every service in the application.

That distinction is important.

A context object should describe a workflow, not the entire system.

---

# Metrics Follow the Same Ownership

Metrics are another cross-cutting concern.

Notice that metrics are owned by the same workflow component that owns logging.

The workflow decides when:

- an operation starts
- a task is created
- a route is calculated
- an operation completes

Those events describe the workflow itself, making the coordinator the natural place to record them.

This avoids introducing another global dependency.

---

# Separating Behavior from Observability

One important improvement over the starting point is that warehouse services no longer produce output.

Instead:

- services perform work
- the logger records what happened
- metrics count events
- `main()` prints the final state for demonstration purposes

These are four separate responsibilities.

Keeping them separate makes the architecture easier to evolve.

For example, replacing console logging with structured logging would only affect the logger implementation, not the warehouse services.

---

# Testing Becomes Easier

The refactored design is also much easier to test.

Tests can replace:

- the logger
- metrics
- repositories
- robot gateways
- inventory services

without relying on global state.

Each dependency can be substituted independently.

This leads to smaller, more focused unit tests.

---

# CARDS Connections

## Clarity

Dependencies become visible through construction rather than hidden global imports.

---

## Alignment

Infrastructure concerns are owned by the application workflow instead of leaking into the domain.

---

## Separation

Warehouse services perform warehouse operations.

Logging and metrics remain separate concerns.

---

## Domain Integrity

Domain objects represent business concepts only.

They remain independent of infrastructure.

---

## Resilience

Because concerns are isolated, changing logging or metrics requires changes in far fewer places.

Small changes remain small.

---

# Trade-Offs

No design is free.

Compared to the original implementation, this solution introduces:

- more constructor parameters
- more explicit composition
- additional setup at the application boundary

However, those costs buy something valuable:

- visible ownership
- improved testability
- reduced hidden coupling
- clearer architectural boundaries

As systems grow, those benefits typically outweigh the additional wiring.

---

# Key Takeaways

- Cross-cutting concerns should have clear owners.
- Global access hides dependencies.
- Passing dependencies explicitly is better, but can create parameter plumbing.
- Workflow-level components often provide the right ownership boundary.
- Context objects should remain focused on a single workflow.
- Domain objects should remain free of infrastructure concerns.
- The most important design question is not *"Should this be global?"* but *"Who should own this concern?"*