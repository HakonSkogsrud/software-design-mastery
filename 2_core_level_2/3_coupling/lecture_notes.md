# Lecture Notes - Choosing Coupling Intentionally

## Overview

In this lesson, we move beyond the simplistic idea of “reducing coupling” and learn how to **choose coupling intentionally**.

Coupling is unavoidable in any useful system. Services need to collaborate, data needs to flow through the application, and different parts of the system depend on each other. The goal is not to eliminate those dependencies, but to shape them so that changes remain local and responsibilities remain clear.

The two main CARDS forces in this lesson are:

- **Resilience** — small changes stay small.
- **Alignment** — dependencies match responsibilities.

Using the hotel booking system, we examine two common coupling problems:

1. **Global coupling** caused by shared module-level state.
2. **Stamp coupling** caused by passing broad objects where only a small subset of data is actually needed.

---

## Coupling Is Inevitable

Every software system contains dependencies.

Examples from the booking system:

- `BookingService` depends on pricing behavior.
- `BookingService` depends on notification behavior.
- `PricingService` depends on room information.
- `NotificationService` depends on booking information.

These dependencies are normal and necessary.

The important question is not:

> Is this coupled?

Instead ask:

> What kind of coupling is this, and what kind of change will it create later?

The goal is not to eliminate dependencies. The goal is to shape them so that responsibilities remain clear and changes remain local.

---

## Coupling Types Recap

Before we discuss specific refactorings, it is useful to revisit the most common forms of coupling.

### Global Coupling

Multiple parts of the system depend on shared state.

Example:

```python
rooms = {...}
bookings = []
```

Several services can access and modify these structures directly.

**Impact:** Weakens **Resilience** because changes to storage tend to ripple through the application.

---

### Control Coupling

One part of the system controls another part’s behavior using flags.

Example:

```python
if request.send_confirmation:
    ...
```

**Impact:** Weakens **Clarity** because behavior becomes harder to reason about as more flags are introduced.

---

### Stamp Coupling

A component receives a large object even though it only needs a small part of it.

Example:

```python
pricing.calculate_for_booking(room, booking_request)
```

**Impact:** Weakens **Alignment** because the dependency surface becomes larger than necessary.

---

### Content Coupling

One component reaches into the internal details of another.

**Impact:** Weakens **Separation** because it creates strong dependencies on implementation details.

---

### Data Coupling

A component receives only the data it actually needs.

Example:

```python
pricing.calculate_total_price(
    room=room,
    nights=request.nights,
    use_discount=request.use_discount,
)
```

**Impact:** Often strengthens **Alignment** and **Resilience**.

---

### Message Coupling

Components collaborate through focused methods and interfaces.

Example:

```python
repository.save_booking(booking)
```

**Impact:** Usually desirable because responsibilities remain explicit.

---

## Fixing Global Coupling

The booking system still contained shared module-level state:

```python
rooms = {...}
bookings = []
```

Multiple services depended on this state directly.

This creates a coupling between business logic and storage details.

### Introducing a Repository

Instead of accessing global state directly:

```python
room = rooms[request.room_number]
bookings.append(booking)
```

we introduce a repository:

```python
room = repository.get_room(request.room_number)
repository.save_booking(booking)
```

The repository becomes the owner of storage concerns.

Example:

```python
class InMemoryBookingRepository:
    def get_room(self, room_number):
        ...

    def save_booking(self, booking):
        ...
```

### Why This Helps

The dependency still exists. `BookingService` still needs access to rooms and bookings.

However, the dependency now has a better shape.

Before:

```text
BookingService
    ↓
Global State
```

After:

```text
BookingService
    ↓
Repository
```

The storage responsibility is now isolated.

This improves:

- **Resilience** — storage changes become more localized.
- **Separation** — business logic no longer talks directly to shared module-level state.

The important lesson is that we did not remove coupling. We changed it into a healthier form.

---

## Introducing Stamp Coupling

Next, the booking system gains new pricing rules.

The request object grows:

```python
@dataclass
class BookingRequest:
    guest_name: str
    guest_email: str
    room_number: int
    nights: int
    use_discount: bool = False
    send_confirmation: bool = True
    preferred_channel: str = "email"
    is_corporate: bool = False
    requires_invoice: bool = False
```

A tempting implementation is:

```python
pricing.calculate_for_booking(room, booking_request)
```

At first glance, this seems convenient.

Only one parameter needs to be passed. The method signature remains stable even as new request fields are added.

However, convenience is often where coupling problems begin.

---

## Why Stamp Coupling Is Problematic

Pricing does not care about most of the request.

Relevant to pricing:

- `nights`
- `use_discount`
- `is_corporate`
- `requires_invoice`

Irrelevant to pricing:

- `guest_name`
- `guest_email`
- `send_confirmation`
- `preferred_channel`

Yet pricing now depends on all of them indirectly.

The dependency surface has become larger than the responsibility. This is stamp coupling.

The code still works, but the structure has become weaker. If the request object keeps growing, pricing becomes increasingly coupled to changes that have nothing to do with pricing.

This weakens:

- **Alignment** — the dependency does not match the responsibility.
- **Resilience** — unrelated changes can start affecting pricing.

---

## Objects vs Values

One common misconception is:

> Always pass primitives.

That is not the lesson.

Passing objects is often the right thing to do.

For example:

```python
pricing.calculate_total_price(room=room, ...)
```

Passing `Room` makes sense because pricing genuinely depends on room characteristics. The object belongs to the pricing domain.

### Rule of Thumb

Pass objects when:

- the object itself belongs to the receiver’s responsibility
- the receiver works with the object conceptually

Pass values when:

- only a small slice of information is needed
- the object would merely act as a convenience container

This distinction is important.

The goal is not to minimize parameters at all costs. The goal is to make dependencies reflect responsibilities.

---

## Moving from Stamp Coupling to Data Coupling

### Before

```python
pricing.calculate_for_booking(
    room,
    booking_request,
)
```

Pricing depends on the entire request.

### After

```python
pricing.calculate_total_price(
    room=room,
    nights=request.nights,
    use_discount=request.use_discount,
    is_corporate=request.is_corporate,
    requires_invoice=request.requires_invoice,
)
```

Pricing now depends only on the information relevant to pricing.

### Benefits

#### Improved Alignment

Dependencies now reflect the actual responsibility of the service. Pricing depends on pricing inputs, nothing more.

#### Improved Resilience

Unrelated changes to `BookingRequest` are less likely to affect pricing. The pricing service becomes more stable as the request object evolves.

#### More Intentional Coupling

We keep the `Room` object because it is meaningful to pricing. We stop passing the entire request because most of it is irrelevant.

This is a good example of intentional coupling.

---

## A Note on Control Coupling

The booking flow still contains:

```python
if request.send_confirmation:
    ...
```

This is a form of control coupling.

That does not automatically make it wrong. However, it should trigger a design review.

Today:

```python
send_confirmation
```

Tomorrow:

```python
send_sms_backup
silent_mode
high_priority
```

Flags often accumulate over time.

The lesson is not:

> Never use flags.

The lesson is:

> When flags appear, ask whether multiple workflows are being hidden behind one API.

A single flag may be acceptable. A growing collection of flags is often a sign that responsibilities need to be revisited.

---

## Key Takeaways

Coupling is unavoidable. The goal is not elimination. The goal is intentional design.

### Global Coupling

Problem:

```python
rooms = {...}
bookings = []
```

Solution:

```python
repository.get_room(...)
repository.save_booking(...)
```

The dependency remains, but it becomes more explicit and localized.

### Stamp Coupling

Problem:

```python
pricing.calculate_for_booking(room, request)
```

Solution:

```python
pricing.calculate_total_price(
    room=room,
    nights=...,
    ...
)
```

The dependency now reflects the actual needs of pricing.

### Practical Guideline

> Pass objects when the object belongs to the responsibility.  
> Pass values when only a slice is needed.

This helps move from stamp coupling toward data coupling, which is usually a healthier baseline.

---

## Bridge to the Next Lesson

In this lesson, we focused on the **shape** of dependencies.

We learned how to reduce unnecessary coupling and make dependencies more deliberate.

But there is another important question:

> Once two parts of the system depend on each other, which direction should that dependency point?

In the next lesson, we will look at dependency direction and learn how stable boundaries emerge from choosing the right dependency flow.
