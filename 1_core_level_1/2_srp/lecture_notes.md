# Lecture Notes - Designing Clear Responsibilities (SRP Done Right)

## Overview

In this lesson, we examined one of the most commonly misunderstood design principles: the Single Responsibility Principle (SRP).

Many developers learn SRP as a rule about keeping functions or classes small. In practice, this often leads to excessive abstraction and fragmented code. The real goal of SRP is not small units—it is cohesive units that change for a single reason.

Using the hotel booking system, we explored how mixed responsibilities create unnecessary coupling, reduce clarity, and make systems harder to evolve. We then refactored the code to separate responsibilities based on change vectors rather than arbitrary size limits.

By the end of the lesson, you should understand:

- What SRP actually means
- How to identify responsibility blur
- Why cohesion matters
- How to evaluate refactorings using CARDS
- Why over-refactoring can be just as harmful as under-refactoring
- How to assess AI-generated refactorings critically

---

# Responsibility Is About Change Vectors

The traditional definition of SRP is:

> A unit should have one reason to change.

The important word here is **change**.

A responsibility is not defined by what code does at runtime. Instead, it is defined by why the code might need to be modified in the future.

Consider the original `book_room()` function.

It handled:

- Validation
- Availability checks
- Pricing
- Booking creation
- Persistence
- Notifications

These concerns evolve independently.

For example:

| Concern | Reason to Change |
|----------|-----------------|
| Validation | New business rules |
| Pricing | New pricing policies |
| Notifications | New communication requirements |
| Persistence | Different storage mechanism |
| Booking creation | Changes to booking data |

Because these concerns change for different reasons, they represent different responsibilities.

This is the core SRP problem.

---

# Cohesion and GRASP

This lesson connects closely to two GRASP principles:

## High Cohesion

High cohesion means that code inside a unit belongs together conceptually.

A cohesive unit focuses on a related set of behaviors.

For example:

- Pricing logic belongs with pricing concerns.
- Notification logic belongs with notification concerns.
- Availability logic belongs with availability concerns.

The more unrelated concerns a unit contains, the lower its cohesion becomes.

Low cohesion makes code harder to understand and harder to modify safely.

---

## Information Expert

Information Expert suggests assigning responsibility to the part of the system that has the knowledge needed to perform the work.

Rather than placing all behavior into a single function, we try to locate behavior near the information it depends on.

Although our booking system is still fairly procedural at this stage, this principle becomes increasingly important as the system evolves into a richer domain model.

---

# Responsibility Blur

One of the biggest threats to Clarity is responsibility blur.

Responsibility blur occurs when multiple concerns become mixed together inside a single unit.

Several common smells help identify this problem.

---

## Flag Arguments

The original booking function contained flags such as:

```python
use_discount=False
send_confirmation=True
```

These flags alter internal behavior.

This introduces a form of coupling called **control coupling**.

The caller now influences multiple responsibilities inside the function.

As more flags appear, the function gradually becomes responsible for more and more concerns.

This weakens both Clarity and Resilience.

---

## Mixed Business Logic and Persistence

The original function calculated pricing:

```python
total_price = room["price"] * nights
```

and then immediately persisted data:

```python
bookings.append(booking)
```

These are separate concerns.

Pricing changes because business policies change.

Persistence changes because storage requirements change.

Combining them creates multiple change vectors inside the same unit.

---

## Hidden Side Effects

The booking process also modified room availability:

```python
room["available"] = False
```

The change itself is legitimate.

The issue is that side effects become difficult to spot when many responsibilities are combined together.

As responsibilities spread, side effects become harder to reason about.

This reduces:

- Clarity
- Resilience

---

# Refactoring Toward Cohesion

The goal is not to create more functions.

The goal is to create clearer responsibility boundaries.

---

## Extracting Pricing Logic

Pricing rules change independently from booking creation.

We extracted pricing into its own function:

```python
def calculate_price(room, nights, use_discount):
    total = room["price"] * nights

    if use_discount and nights >= 3:
        total *= 0.9

    return total
```

Benefits:

- Pricing logic lives in one place.
- Pricing rules become easier to find.
- Future pricing changes remain isolated.

This improves:

- Clarity
- Resilience

---

## Extracting Notification Logic

Notification behavior also changes independently.

We moved it into its own function:

```python
def send_booking_confirmation(guest_email, room_number):
    print(
        f"Sending confirmation email to {guest_email} for room {room_number}"
    )
```

Benefits:

- Booking logic focuses on booking.
- Notification logic focuses on communication.
- Future notification changes become isolated.

Again, this improves:

- Clarity
- Resilience

---

# Patterns Should Emerge Naturally

An important observation from this refactoring is that we did not start by introducing a pattern.

Instead:

1. We identified design pressure.
2. We separated responsibilities.
3. A possible structure naturally emerged.

For example, pricing behavior could eventually evolve into a strategy-like structure.

The lesson is not:

> Use the Strategy Pattern.

The lesson is:

> Separate responsibilities first and let patterns emerge when they solve real problems.

---

# Guarding Against Over-Refactoring

Many developers overcorrect when applying SRP.

They start splitting every operation into tiny helper functions.

For example:

```python
validate_room_exists()
validate_room_available()
validate_nights()
calculate_base_price()
calculate_discount()
persist_booking()
```

Technically these may be single-purpose functions.

But excessive decomposition introduces a different problem.

The flow of the operation becomes difficult to follow.

The reader must constantly jump between functions to understand a simple process.

---

# The CARDS Test

Before introducing an abstraction, ask:

> Which CARD does this improve?

An abstraction should improve at least one of:

- Clarity
- Alignment
- Resilience
- Domain Integrity
- Separation

If it improves none of them, it is probably unnecessary.

Remember:

Abstraction is not free.

Every additional abstraction introduces complexity.

---

# KISS Still Matters

SRP and KISS are not in conflict.

In fact, they complement each other.

Good design is not about maximizing the number of abstractions.

Good design is about making intent obvious and change safe.

Sometimes the simplest solution is the best solution.

---

# AI Design Filter

AI tools frequently generate refactorings that appear clean but fail structurally.

A typical AI-generated SRP refactor may create many tiny functions while leaving responsibility boundaries unchanged.

When reviewing AI-generated code, ask:

- Did responsibilities become clearer?
- Are change vectors better isolated?
- Is the code easier to reason about?
- Did cohesion improve?

If the answer is no, the refactor likely improved appearance rather than design.

AI can help produce code.

Design judgment remains your responsibility.

---

# Key Takeaways

- SRP is about reasons to change, not code size.
- Responsibilities should align with change vectors.
- High cohesion improves understandability and maintainability.
- Control coupling often appears through flag arguments.
- Mixed concerns reduce Clarity and Resilience.
- Patterns should emerge from design pressure.
- Over-refactoring can be just as harmful as under-refactoring.
- Every abstraction should improve at least one CARD.
- AI-generated refactors should be evaluated structurally, not cosmetically.

---

# Bridge to the Next Lesson

In this lesson, we focused on separating responsibilities so that changes remain localized and understandable.

The next step is to look at how responsibilities interact with each other through dependencies.

Even if responsibilities are clear, a system can still become difficult to evolve when dependencies point in the wrong direction.

In the next lesson, we will begin exploring coupling and dependency relationships, and how they affect the long-term stability of a design.