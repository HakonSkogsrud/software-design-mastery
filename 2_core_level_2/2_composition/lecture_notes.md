# Lecture Notes - Composition Over Inheritance (and Why Mixins Hurt)

## Overview

In the previous lesson, we separated responsibilities in the booking system by introducing service classes such as:

- `PricingService`
- `AvailabilityService`
- `NotificationService`
- `BookingPolicy`

This improved cohesion and made responsibilities clearer.

However, once multiple service classes exist, a new temptation appears:

> Several classes need the same behavior, so let's share it through inheritance.

Common examples include:

- logging
- retry behavior
- caching
- auditing

This lesson explores why inheritance and mixins often introduce hidden structural problems, and why composition is usually the safer default for application code.

The main CARDS forces are:

- **Alignment** — dependencies point in the right direction
- **Clarity** — code communicates intent clearly
- **Resilience** — small changes stay small

---

## The Temptation of Reuse Through Inheritance

Suppose several services need logging.

A common solution is to introduce a shared base class:

```python
class BaseService:
    def log(self, message):
        print(f"[LOG] {message}")
```

Services can then inherit from it:

```python
class PricingService(BaseService):
    ...
```

This reduces duplication and initially feels like a clean improvement.

However, inheritance creates a stronger relationship than we actually need.

The service is not a special kind of logging component.

It merely uses logging.

This distinction is important because inheritance affects the structure of the system, not just code reuse.

---

## Hidden Coupling Through Base Classes

Inheritance creates a dependency between parent and child classes.

When the parent changes, all subclasses are affected.

Consider a seemingly harmless modification:

```python
class BaseService:
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")
```

This change automatically alters the behavior of every subclass.

The subclasses changed without being modified directly.

This illustrates a key structural problem:

> A small change in a shared parent can ripple through many parts of the system.

This weakens **Resilience** because change spreads further than intended.

It also weakens **Alignment** because the true dependency—logging—is hidden behind inheritance.

---

## Why Mixins Are Not a Complete Solution

Python developers often recognize the risks of deep inheritance hierarchies and reach for mixins instead.

A mixin is usually a small class that provides reusable behavior:

```python
class LoggingMixin:
    def log(self, message):
        print(f"[LOG] {message}")
```

A service can then inherit from the mixin:

```python
class NotificationService(LoggingMixin):
    ...
```

This looks lighter and more modular.

However, the core structural problem remains.

The service still depends on logging behavior, but that dependency is not explicit.

It is hidden inside the inheritance list.

---

## Hidden Contracts

Mixins often evolve into something more dangerous.

Consider this example:

```python
class RetryMixin:
    def retry_count(self):
        return self.max_retries
```

The mixin now assumes that every class using it defines:

```python
self.max_retries
```

This requirement is not obvious from the mixin itself.

Nothing enforces it.

The design relies on convention and developer knowledge.

This is known as a **hidden contract**.

Hidden contracts are problematic because:

- required state is not obvious
- incorrect usage is easy
- errors appear at runtime
- maintenance becomes harder

This weakens both **Clarity** and **Resilience**.

---

## Multiple Inheritance and Ordering Sensitivity

Mixins can also make behavior depend on inheritance mechanics.

Consider:

```python
class ConsoleLoggingMixin:
    def log(self, message):
        print(f"[console] {message}")


class AuditLoggingMixin:
    def log(self, message):
        print(f"[audit] {message}")
```

Now:

```python
class Service(ConsoleLoggingMixin, AuditLoggingMixin):
    pass
```

Which `log()` method will be used?

The answer depends on Python's method resolution order.

The behavior is no longer determined solely by the design of the service itself.

Instead, it depends on inheritance ordering.

This introduces unnecessary complexity and makes systems harder to reason about.

---

## Composition as an Alternative

Instead of inheriting behavior, we can model it as a collaborator.

For example:

```python
class Logger:
    def log(self, message):
        print(f"[LOG] {message}")
```

And:

```python
class RetryPolicy:
    def retry_count(self):
        return 3
```

Services can then receive these collaborators explicitly:

```python
class NotificationService:
    def __init__(self, logger, retry_policy):
        self.logger = logger
        self.retry_policy = retry_policy
```

This is composition.

The service is assembled from smaller pieces rather than inheriting behavior from parents.

---

## Why Composition Improves Structure

### Alignment

Dependencies become visible.

Instead of hiding logging inside a parent class:

```python
class NotificationService(LoggingMixin):
    ...
```

we make the dependency explicit:

```python
class NotificationService:
    def __init__(self, logger):
        self.logger = logger
```

The structure now reflects reality.

---

### Clarity

Reading the constructor immediately reveals what the service needs.

There is no need to inspect parent classes or mixins to understand where behavior comes from.

The design becomes easier to understand.

---

### Resilience

Changes become more local.

Suppose we want a different retry policy:

```python
class ExponentialBackoffRetryPolicy:
    ...
```

We can introduce the new policy without modifying the service itself.

The change affects only the collaborator being replaced.

This keeps changes smaller and more contained.

---

## Composition Does Not Eliminate Reuse

A common misconception is that composition sacrifices reuse.

It does not.

We still reuse behavior.

The difference is where the reuse happens.

Inheritance reuses behavior through structural relationships.

Composition reuses behavior through explicit collaboration.

The latter tends to create systems that are easier to evolve over time.

---

## AI Guardrail

AI tools frequently suggest:

- base classes
- mixins
- inheritance hierarchies

because they quickly remove visible duplication.

However, reduced duplication does not automatically improve design.

Before accepting an inheritance-based solution, ask:

> Does this make the dependency structure clearer?

Or:

> Does it simply hide the dependency inside a parent class?

Good signs:

- dependencies are visible
- collaborators are explicit
- constructors communicate requirements clearly

Warning signs:

- helper base classes
- mixins with hidden assumptions
- behavior depending on inheritance order
- multiple inheritance used to assemble functionality

---

## Key Takeaways

- Inheritance is often introduced to reduce duplication.
- Base classes create coupling between parent and child classes.
- Changes to a parent can affect many subclasses.
- Mixins are lighter than inheritance hierarchies but often introduce hidden contracts.
- Multiple inheritance can make behavior depend on inheritance ordering.
- Composition makes dependencies explicit.
- Explicit collaborators improve:
  - **Alignment**
  - **Clarity**
  - **Resilience**

The most important lesson is:

> Services usually do not need to inherit behavior.
>
> They need to collaborate with behavior.

---

## Bridge to the Next Lesson

In this lesson we focused on making dependencies explicit by preferring composition over inheritance.

However, even when dependencies are explicit, there is still an important question:

> Which dependencies should a class actually know about?

In the next lesson, we will explore how dependency direction influences system stability and why stable boundaries often depend on introducing the right abstractions.