# Lecture Notes — Protecting the Domain Core

## Overview

In the previous lessons, we strengthened the domain model by introducing better domain concepts and stronger types.

We created value objects such as:

- `EmailAddress`
- `StayNights`
- `Money`

These help prevent invalid values from entering the system.

However, there is another problem we still need to solve.

A model can contain valid data and still be easy to misuse.

In this lesson, we focus on protecting the domain core by making important business rules harder to bypass.

The goal is not to make misuse impossible. Python does not provide strict encapsulation like some other languages.

Instead, the goal is to make the correct path obvious and the incorrect path awkward.

---

# The Problem

Consider a booking model like this:

```python
@dataclass
class Booking:
    booking_id: BookingId
    guest_name: GuestName
    guest_email: EmailAddress
    room_number: RoomNumber
    nights: StayNights
    total_price: Money
    status: BookingStatus = BookingStatus.PENDING
```

This model is already much better than one built entirely from primitive types.

However, important state can still be modified directly:

```python
booking.status = BookingStatus.CONFIRMED
booking.total_price = Money(Decimal("0.00"))
```

Similarly, callers can create objects in arbitrary states:

```python
booking = Booking(
    booking_id="BKG-123",
    guest_name="Alice",
    guest_email=EmailAddress("alice@example.com"),
    room_number=101,
    nights=StayNights(3),
    total_price=Money(Decimal("0.00")),
    status=BookingStatus.CONFIRMED,
)
```

The model is structurally sound, but it does not actively guide correct usage.

---

# Validation vs Protection

It is useful to distinguish between two different concerns.

## Validation

Validation ensures that values are correct.

Examples:

- An email address contains an `@`.
- The number of nights is greater than zero.
- A monetary value is non-negative.

We addressed these concerns in previous lessons.

## Protection

Protection ensures that important business rules remain intact over time.

Examples:

- A booking should always start in a valid state.
- State transitions should follow business rules.
- Important values should not be modified arbitrarily.

This lesson focuses on protection.

---

# Controlling Object Creation

One of the easiest ways to bypass a model is through direct construction.

If callers create objects directly, they also decide how those objects start their lifecycle.

Instead, we can provide an intention-revealing constructor:

```python
@dataclass
class Booking:
    ...

    @classmethod
    def create(
        cls,
        booking_id: BookingId,
        guest_name: GuestName,
        guest_email: EmailAddress,
        room_number: RoomNumber,
        nights: StayNights,
        total_price: Money,
    ) -> Self:
        return cls(
            booking_id=booking_id,
            guest_name=guest_name,
            guest_email=guest_email,
            room_number=room_number,
            nights=nights,
            _total_price=total_price,
            _status=BookingStatus.PENDING,
        )
```

Now the domain model decides that every new booking starts in the `PENDING` state.

Callers provide business inputs rather than implementation details.

This has several benefits:

- Creation logic is centralized.
- The initial state is consistent.
- Future changes become easier.

---

# Explicit State Transitions

Another problem is direct mutation.

Consider code like this:

```python
booking.status = BookingStatus.CONFIRMED
```

Nothing prevents callers from changing state in arbitrary ways.

Instead, we can expose explicit behavior:

```python
booking.confirm()
booking.cancel()
```

These methods represent business actions rather than implementation details.

For example:

```python
def confirm(self) -> None:
    if self._status is not BookingStatus.PENDING:
        raise ValueError("Only pending bookings can be confirmed")

    self._status = BookingStatus.CONFIRMED
```

This ensures that state changes follow business rules.

The rules live inside the model instead of being scattered throughout the codebase.

---

# Encapsulation Through Intent

Python does not enforce true private fields.

However, we can still communicate intent.

Fields such as:

```python
_status: BookingStatus
_total_price: Money
```

are marked as internal implementation details.

The leading underscore signals that these values should not be modified directly.

This is not a technical restriction.

It is a design convention.

Good Python code respects that convention.

---

# Read-Only Access

Other parts of the application still need to inspect state.

Properties provide a clean solution.

For example:

```python
@property
def status(self) -> BookingStatus:
    return self._status
```

and

```python
@property
def total_price(self) -> Money:
    return self._total_price
```

These properties expose information without exposing mutation.

As a result:

```python
print(booking.status)
print(booking.total_price)
```

is encouraged, while:

```python
booking._status = BookingStatus.CONFIRMED
```

clearly looks suspicious.

---

# Protecting Business Rules

The wildlife tracking mission exercise demonstrates another common pattern.

Consider this requirement:

> A tracker can only be changed before the mission starts.

Without protection, any caller could write:

```python
mission.tracker_id = "TRK-99"
```

at any time.

Instead, we can expose a dedicated method:

```python
def assign_tracker(self, tracker_id: str) -> None:
    ...
```

This method validates both:

- whether the mission is still in the correct state
- whether the new tracker id is valid

The business rule now lives inside the domain model itself.

Callers no longer need to remember the rule.

---

# Keeping Rules in One Place

Notice how lifecycle rules are concentrated inside the model.

The mission decides:

- when it can start
- when it can complete
- when it can be cancelled
- when a tracker can be reassigned

This is important because business rules change over time.

When rules are centralized:

- changes become easier
- bugs become less likely
- the model becomes easier to understand

Instead of searching through services and helper functions, we know exactly where to look.

---

# Protection in Python

A common misconception is that protection means preventing every possible misuse.

That is unrealistic in Python.

Someone can still write:

```python
mission._status = MissionStatus.COMPLETED
```

Python will allow it.

The goal is different.

We want correct usage to feel natural and incorrect usage to look suspicious.

Well-designed APIs guide developers toward the intended behavior.

This is often more valuable than strict technical enforcement.

---

# AI-Assisted Development

This becomes especially important when using AI coding tools.

AI systems often generate the shortest path to a result.

That path may bypass domain rules.

When reviewing AI-generated code, ask questions like:

- Is the model's public API being used?
- Are lifecycle methods being respected?
- Are internal fields being modified directly?

For example:

```python
booking.confirm()
```

is preferable to:

```python
booking._status = BookingStatus.CONFIRMED
```

even if both technically work.

---

# Key Takeaways

A strong domain model is not only about valid data.

It is also about protecting important business rules.

In this lesson we improved the model by:

- Controlling construction with `create()`
- Making state transitions explicit
- Using internal fields for protected state
- Exposing read-only properties
- Centralizing lifecycle rules inside the domain model

The result is a model that is easier to use correctly and harder to misuse accidentally.

This strengthens:

- **Domain Integrity** by protecting important rules
- **Clarity** by making intended usage explicit
- **Resilience** by keeping changes localized

These ideas form the foundation of a protected domain core.