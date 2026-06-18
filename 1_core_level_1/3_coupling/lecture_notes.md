# Lecture Notes - Hidden Dependencies and Coupling

## Overview

In this lesson, we introduced one of the most important structural forces in software design: **coupling**.

Coupling determines how strongly parts of a system depend on each other. Some coupling is unavoidable, but excessive or poorly placed coupling makes systems difficult to understand, modify, and evolve.

The goal of this lesson is not to memorize coupling terminology. Instead, coupling types serve as a diagnostic tool. When a small change requires edits in many places, coupling is often the underlying cause.

Within the CARDS framework, coupling primarily affects:

- **Resilience** — small changes should stay small
- **Alignment** — dependencies should point in the right direction

---

# Why Coupling Matters

A system can have clear code and still be difficult to maintain if its components are tightly connected.

When coupling increases:

- Changes spread further through the system
- Refactoring becomes riskier
- Internal implementation details leak outward
- Components become harder to reuse independently

A key responsibility of a designer is to identify unnecessary coupling and reduce it where practical.

---

# Common Coupling Types

The purpose of these categories is not classification for its own sake.

They help answer a practical question:

> Why is this code difficult to change?

## Global Coupling

Global coupling occurs when multiple parts of a system depend on shared global state.

Example:

```python
rooms = {...}
bookings = []
```

Functions can freely read and modify these structures.

Problems:

- Dependencies are hidden
- Changes become harder to track
- Replacing the storage mechanism affects many locations

### CARDS Impact

**Alignment** suffers because dependencies are implicit rather than explicit.

---

## Control Coupling

Control coupling occurs when callers influence internal behavior through flags or control parameters.

Example:

```python
book_room(
    guest_name,
    guest_email,
    room_number,
    nights,
    use_discount=True,
)
```

The caller must understand details of how the function behaves internally.

Problems:

- Behavior becomes harder to reason about
- New options often lead to additional flags
- Responsibilities become mixed together

### CARDS Impact

**Clarity** suffers because behavior becomes less obvious.

---

## Stamp Coupling

Stamp coupling occurs when large structures are passed around even though only a small portion is required.

Example:

```python
booking["guest_email"]
booking["room_number"]
booking["status"]
```

A function may only need one field but receives an entire booking structure.

Problems:

- Functions depend on data they don't actually need
- Structural changes have wider impact
- Dependencies become larger than necessary

### CARDS Impact

**Resilience** suffers because structural changes ripple through the system.

---

## Data Coupling

Data coupling is generally the healthiest baseline.

Functions receive only the information they require.

Example:

```python
def calculate_price(
    price_per_night: int,
    nights: int,
) -> int:
    return price_per_night * nights
```

Benefits:

- Smaller dependencies
- Easier testing
- Better reuse
- Reduced change amplification

### CARDS Impact

Supports **Resilience** by minimizing unnecessary dependencies.

---

## Message Coupling

Message coupling is often the weakest and most flexible form of coupling.

Instead of sharing internal structures, objects communicate through behavior.

Example:

```python
pricing_service.calculate_price(
    room_price,
    nights,
)
```

The caller knows what to ask for but not how it is implemented.

Benefits:

- Internal details remain hidden
- Implementations can evolve independently
- Responsibilities stay localized

### CARDS Impact

Supports both **Alignment** and **Resilience**.

---

# The Law of Demeter

The Law of Demeter helps reduce dependency leakage.

A common summary is:

> Talk only to your immediate collaborators.

Consider:

```python
booking.guest.email
```

The code now depends on:

- Booking
- Guest
- Email storage details

Internal structure has leaked outward.

A better approach is:

```python
booking.guest_email()
```

Or even:

```python
notification_service.send_confirmation(
    booking
)
```

The caller expresses intent without navigating object internals.

---

# Why Deep Navigation Is Dangerous

Deep navigation creates hidden structural dependencies.

Example:

```python
drone["hardware"]["battery"]["health"]
```

This code assumes:

- A drone contains hardware
- Hardware contains a battery
- Battery contains a health field

Any structural change may break the caller.

The deeper the navigation chain becomes, the more fragile the code usually is.

### CARDS Impact

Violates:

- **Clarity** — readers must understand internal structures
- **Alignment** — dependencies spread across object boundaries

---

# Composition Over Inheritance

Inheritance is often introduced as a reuse mechanism.

However, inheritance also creates strong coupling between parent and child classes.

Example:

```python
class DiscountBookingService(
    BookingService
):
    ...
```

The subclass depends on details of the parent implementation.

Problems:

- Base-class changes may break subclasses
- Behavior becomes harder to reason about
- Hidden assumptions accumulate over time

This is sometimes called **subclass fragility**.

---

## Prefer Composition

Instead of inheriting behavior, inject collaborators.

Example:

```python
class BookingService:
    def __init__(
        self,
        pricing_service,
    ):
        self.pricing_service = pricing_service
```

Usage:

```python
total_price = (
    self.pricing_service.calculate(
        room_price,
        nights,
    )
)
```

Benefits:

- Dependencies become explicit
- Components can evolve independently
- Reuse becomes more flexible

### CARDS Impact

Improves both **Alignment** and **Resilience**.

---

# Example: Encapsulating Drone Logic

Consider the original implementation:

```python
def schedule_battery_replacement(drone):
    if (
        drone["hardware"]["battery"]["health"] < 70
        and drone["hardware"]["battery"]["cycles"] > 500
        and drone["mission"]["status"] == "idle"
    ):
        ...
```

This function knows far too much about the drone's internal structure.

A better design introduces domain objects:

```python
drone.can_schedule_battery_replacement()
```

Now the scheduling function works with a meaningful concept rather than nested data.

Benefits:

- Reduced stamp coupling
- Reduced dependency leakage
- Improved readability
- Better separation of responsibilities

The scheduling function no longer cares how batteries or missions are represented internally.

---

# AI Risk: Coupling Amplification

AI tools are excellent at producing locally correct code.

However, they often increase coupling unintentionally.

Common examples:

Deep attribute navigation:

```python
booking.guest.account.profile.email
```

Large parameter lists:

```python
create_booking(
    guest_name,
    guest_email,
    guest_phone,
    guest_address,
    ...
)
```

Direct access to internal structures:

```python
rooms[room_number]["price"]
```

The generated code may work perfectly today while making future changes more expensive.

When reviewing AI-generated code, ask:

- Are internal structures leaking outward?
- Are dependencies explicit?
- Is behavior hidden behind meaningful abstractions?
- Are we introducing unnecessary coupling?

AI can generate code.

Designers must protect structure.

---

# Key Takeaways

- Coupling is one of the primary drivers of change amplification.
- Not all coupling is bad, but excessive coupling reduces flexibility.
- Global coupling hides dependencies.
- Control coupling mixes responsibilities.
- Stamp coupling exposes too much structure.
- Data coupling is usually a healthy baseline.
- Message coupling often provides the most flexibility.
- The Law of Demeter helps prevent dependency leakage.
- Composition usually creates more resilient designs than inheritance.
- AI tools frequently introduce coupling accidentally.

When evaluating code, ask:

> If this internal structure changes tomorrow, how many places will I need to modify?

The answer often reveals the real coupling in the system.

---

# Bridge to the Next Lesson

In this lesson we focused on identifying structural dependencies and understanding how coupling affects change.

In the next lesson, we'll build on these ideas by looking at how responsibilities should be distributed across a system. Reducing coupling is only part of the solution. We also need to decide where behavior belongs so that modules remain cohesive and changes stay localized.