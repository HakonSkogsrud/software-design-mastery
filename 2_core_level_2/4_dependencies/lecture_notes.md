# Lecture Notes - Dependency Direction and Stable Boundaries

## Overview

In this lesson, we take the structure from the previous lesson and make one important architectural improvement: we make the repository boundary explicit.

The previous lesson already introduced composition. `BookingService` no longer created everything itself. Instead, it worked with collaborators such as a repository, pricing service, booking policy, availability service, and notification service.

That was a strong step forward. But one question remained:

> What exactly is the booking use case allowed to depend on?

This lesson answers that question by introducing a clear dependency rule:

> Dependencies should point toward stable code.

To make that concrete, we introduce a `BookingRepository` protocol and make `BookingService` depend on that stable contract instead of relying on an implicit repository shape.

Along the way, this lesson also clarifies three related terms:

- dependency injection
- inversion of control
- dependency inversion

The goal is not to add abstraction everywhere. The goal is to make one volatile boundary explicit and keep concrete details at the edge of the system.

---

## The state of the system before this lesson

At this point in the booking system, the code already has a much better structure than the original messy script.

We now have:

- domain objects such as `Room`, `Booking`, and `BookingRequest`
- a repository
- services for availability, pricing, notifications, and booking policy
- a `BookingService` that orchestrates the booking flow
- a `main()` function that wires everything together

This is important context, because this lesson does **not** introduce composition for the first time. That already happened.

Instead, this lesson improves the direction of dependencies.

---

## The main design idea

The core idea of this lesson is:

> Stable code should not depend directly on volatile implementation details.

In this booking system:

### Stable code
Stable code is the code that expresses the business model and use-case behavior:

- `Booking`
- `Room`
- `BookingRequest`
- the booking flow in `BookingService`
- pricing logic
- booking status policy

### Volatile code
Volatile code is more likely to change because of technical or external reasons:

- repository implementations
- database technology
- frameworks
- delivery mechanisms
- external SDKs

The repository is a good example of a volatile dependency.

Today we have `InMemoryBookingRepository`. Later, that could become a SQL-backed implementation. The booking use case should not have to change just because storage changes.

That is the design pressure this lesson addresses.

---

## Dependency injection

Before introducing the protocol, the lesson pauses to explain a term students have already started using: **dependency injection**.

A dependency is simply something a class needs in order to do its job.

For example, `BookingService` needs access to a repository. It cannot do its work without one.

### Without dependency injection

If a class creates its own dependency internally, it controls too much:

```python
class BookingService:
    def __init__(self):
        self.repository = InMemoryBookingRepository(...)
```

Here, `BookingService` decides exactly which repository to use.

### With dependency injection

With dependency injection, the dependency is passed in from the outside:

```python
class BookingService:
    def __init__(self, repository):
        self.repository = repository
```

This is better because the class no longer decides how that dependency is created.

It only uses it.

That is the first design improvement.

---

## Inversion of control

Dependency injection is closely related to **inversion of control**.

Normally, a class controls how its dependencies are created and wired together.

With inversion of control, that responsibility moves outward.

So instead of `BookingService` deciding which repository to construct, something outside it—here, `main()`—decides which repository to pass in.

That means:

- the core does less setup work
- the wiring is moved outward
- the class focuses more clearly on its actual job

Inversion of control is the broader idea.

Dependency injection is one way to apply it.

---

## Dependency inversion

This lesson then introduces the more important architectural concept: **dependency inversion**.

The easiest way to remember the difference is this:

- **Dependency injection** is about how a dependency is provided
- **Dependency inversion** is about what the core depends on

In this lesson:

- dependency injection means the repository is passed into `BookingService`
- dependency inversion means `BookingService` depends on a stable contract instead of a concrete repository class

That is the deeper design move.

---

## The repository boundary is still implicit

Before the refactoring in this lesson, `BookingService` already accepted a repository from the outside.

That was good.

But the code still relied on an implicit assumption:

> Whatever object we pass in as `repository` should have the methods the service expects.

That works in Python, but the architectural boundary is still not clearly expressed.

The stable side—the use case—has not explicitly stated what repository behavior it needs.

So the next step is to define that contract.

---

## The `BookingRepository` protocol

The main refactoring in this lesson is the introduction of a `Protocol`:

```python
class BookingRepository(Protocol):
    def get_room(self, room_number: int) -> Room | None:
        ...

    def save_booking(self, booking: Booking) -> None:
        ...

    def active_booking_exists_for_room(self, room_number: int) -> bool:
        ...

    def list_bookings(self) -> list[Booking]:
        ...
```

This protocol defines the repository behavior the use case depends on.

That is the key architectural improvement.

`BookingService` does not need:

- an in-memory repository
- a SQL repository
- a Postgres repository

It needs repository **behavior**.

By defining that behavior in a protocol, the stable side now owns the contract.

That is dependency inversion in practice.

---

## Why `Protocol` is a good fit here

Python’s `Protocol` type is useful in this case because we care about behavior, not inheritance hierarchies.

The lesson does not introduce a base repository class with shared implementation. It simply states the required interface.

That keeps the abstraction lightweight.

This is consistent with an important theme in the course:

> Introduce abstraction where it helps. Do not abstract everything.

The repository is a good candidate because it is volatile.

Other collaborators in this lesson are left alone to keep the example focused.

---

## `BookingService` after the refactoring

After introducing the protocol, `BookingService` changes only slightly:

```python
class BookingService:
    def __init__(
        self,
        repository: BookingRepository,
        availability_service,
        pricing_service,
        booking_policy,
        notification_service,
    ):
        self.repository = repository
        self.availability_service = availability_service
        self.pricing_service = pricing_service
        self.booking_policy = booking_policy
        self.notification_service = notification_service
```

This is important.

The booking flow itself does not change.

That is a sign of a good refactoring: the behavior stays the same, but the design becomes clearer.

Now the dependency is explicit.

`BookingService` is saying:

> I depend on repository behavior defined by `BookingRepository`.

This improves:

- **Alignment** — dependencies point toward a stable contract
- **Separation** — storage concerns stay more clearly outside the use case
- **Clarity** — the constructor better communicates the boundary

---

## Domain objects in the script

The lesson continues to use the same domain model from the previous lesson. These classes are important because they represent the stable core of the system.

### `BookingStatus`

`BookingStatus` is a `StrEnum` with three states:

- `PENDING`
- `CONFIRMED`
- `CANCELLED`

This makes booking state explicit and avoids passing around raw strings with hidden meaning.

---

### `Room`

`Room` is a dataclass with:

- `number`
- `room_type`
- `price`
- `available`

It also contains simple behavior:

- `is_available()`
- `mark_unavailable()`
- `mark_available()`

This keeps room-related behavior close to the room itself.

---

### `Booking`

`Booking` stores the result of a booking operation:

- guest name
- guest email
- room number
- number of nights
- total price
- status

It also includes behavior:

- `is_confirmed()`
- `cancel()`
- `change_room(...)`

This helps keep booking behavior attached to the `Booking` model instead of scattering it elsewhere.

---

### `BookingRequest`

`BookingRequest` represents the input to the booking flow.

It includes:

- guest information
- room number
- number of nights
- discount options
- confirmation preferences
- corporate flags
- invoice flags

This keeps the input to the use case explicit and structured.

---

## The repository implementation

The script keeps the existing `InMemoryBookingRepository`.

It now acts as a concrete implementation of the `BookingRepository` protocol.

It stores:

- rooms in a dictionary
- bookings in a list

It provides the four required methods:

- `get_room(...)`
- `save_booking(...)`
- `active_booking_exists_for_room(...)`
- `list_bookings()`

### `get_room`
Looks up a room by number.

### `save_booking`
Adds a booking to the in-memory list.

### `active_booking_exists_for_room`
Checks whether a room already has an active booking. A cancelled booking does not count as active.

### `list_bookings`
Returns a copy of the bookings list for display.

This implementation remains simple, which is a good thing. The lesson is about dependency direction, not database complexity.

---

## Supporting services

The script also keeps the supporting services from the previous lesson.

### `Logger`
A small utility class with a single `log(...)` method.

Used by other services to show what they are doing.

### `RetryPolicy`
A simple class returning a retry count.

Used by the notification service.

---

### `AvailabilityService`

`AvailabilityService` checks whether a booking can proceed.

It validates:

- room exists
- room is available
- nights is greater than zero

This keeps availability-related decisions out of `BookingService`.

---

### `PricingService`

`PricingService` calculates the final booking price.

It starts with:

- `room.price * nights`

Then adjusts for:

- discount for longer stays
- corporate pricing
- invoice surcharge for non-corporate bookings

It also logs its activity.

This is a good example of stable business logic. It belongs in the core and does not need inversion in this lesson.

---

### `BookingPolicy`

`BookingPolicy` decides the initial booking status.

In this version:

- suites start as `PENDING`
- everything else starts as `CONFIRMED`

This is a useful example of how policy logic can be separated from orchestration.

It also logs what it is doing.

---

### `NotificationService`

`NotificationService` is responsible for sending confirmations.

It uses:

- `Logger`
- `RetryPolicy`

Its method `send_booking_confirmation(...)` logs the retry policy and prints the confirmation message.

This service remains concrete in this lesson. Again, that is deliberate. The lesson stays focused by showing dependency inversion only for the repository boundary.

---

## The booking flow in `BookingService`

The core orchestration still lives in `BookingService.book_room(...)`.

This method coordinates the booking process step by step.

### 1. Start the flow

It prints:

```python
print("[BookingService] Starting booking flow")
```

This makes the execution flow easier to follow in the demo.

### 2. Get the room from the repository

```python
room = self.repository.get_room(booking_request.room_number)
```

This is one place where the repository boundary matters directly.

`BookingService` does not care how rooms are stored. It only asks the repository for the room.

### 3. Validate booking availability

```python
if not self.availability_service.can_book(room, booking_request.nights):
    return None
```

This delegates validation to `AvailabilityService`.

### 4. Check for existing active bookings

```python
if self.repository.active_booking_exists_for_room(room.number):
    print("Room already has an active booking")
    return None
```

This is another place where repository behavior is used through the stable contract.

### 5. Calculate total price

```python
total_price = self.pricing_service.calculate_total_price(...)
```

Pricing logic stays in the pricing service.

### 6. Create the booking

A new `Booking` is created using the request data and the policy result:

```python
status=self.booking_policy.initial_status(room)
```

This keeps booking-status rules out of the service itself.

### 7. Save the booking

```python
self.repository.save_booking(booking)
```

Again, `BookingService` depends only on repository behavior.

### 8. Mark the room unavailable

```python
room.mark_unavailable()
```

The room updates its own state.

### 9. Send confirmation if appropriate

If the request asks for confirmation and the booking is confirmed, the service sends a notification:

```python
if booking_request.send_confirmation and booking.is_confirmed():
    self.notification_service.send_booking_confirmation(
        booking,
        booking_request.preferred_channel,
    )
```

That avoids sending confirmations for pending bookings such as suites.

### 10. Return the booking

If all goes well, the method returns the `Booking` object.

---

## Why the booking flow is mostly unchanged

One of the most important teaching points in this lesson is that the main use-case logic does not need a rewrite.

That is exactly what we want.

The lesson is not about changing business behavior. It is about clarifying the dependency boundary.

This is a good example of a structural refactoring:

- same behavior
- clearer dependency direction
- more explicit contract
- no unnecessary redesign

---

## `main()` as the composition boundary

The script ends with a `main()` function that creates and wires all concrete objects:

- logger
- retry policy
- repository
- availability service
- pricing service
- booking policy
- notification service
- booking service

This is where the concrete choices come together.

Robert Martin sometimes refers to this kind of place as the **dirty place**.

That is not a criticism. It simply means this is where concrete details are allowed to meet.

`main()` is allowed to know:

- which repository implementation we use
- which logger we use
- which retry policy we use

The application core should not need to know those choices.

That is the split this lesson is reinforcing:

- `BookingService` knows what behavior it needs
- `main()` knows which concrete objects are used today

---

## The demo scenarios

The script includes three scenarios to show the system behavior.

### Scenario 1 — Standard booking

Alice books room 101 for 2 nights.

Expected result:

- room exists
- room is available
- booking is valid
- pricing is calculated
- status is `CONFIRMED`
- confirmation is sent

---

### Scenario 2 — Corporate booking

Bob books room 102 as a corporate booking.

This demonstrates:

- corporate pricing adjustment
- invoice behavior
- normal confirmation flow

---

### Scenario 3 — Suite booking starts as pending

Charlie books room 201, which is a suite.

This demonstrates policy behavior:

- suites start as `PENDING`
- confirmation is not sent because the booking is not confirmed

This is a good example of business policy affecting the flow without making `BookingService` carry all the rule logic itself.

---

## What this lesson improves in CARDS terms

### Alignment
This is the main focus of the lesson.

`BookingService` now depends on `BookingRepository`, a stable contract, rather than on an implicit or concrete repository shape.

### Separation
Repository implementation details remain outside the booking use case.

### Clarity
The constructor communicates the boundary more explicitly.

### Resilience
The system becomes easier to evolve because a future repository implementation can be added without changing the use case.

---

## What this lesson does not do

This lesson is deliberately narrow.

It does **not**:

- abstract every dependency
- introduce a full architecture framework
- add database complexity
- redesign the entire system

That restraint matters.

Good design is not about abstracting everything in sight. It is about introducing structure where it solves a real problem.

Here, the real problem is repository volatility.

So that is the one boundary the lesson makes explicit.

---

## Practical takeaway

After this lesson, students should be able to recognize the difference between these three ideas:

### Dependency injection
Pass the dependency in from the outside.

### Inversion of control
Move responsibility for wiring concrete dependencies outward.

### Dependency inversion
Make the stable side depend on a stable contract instead of a concrete implementation.

They should also be able to apply a simple test:

> Can I change the repository implementation without editing `BookingService`?

If the answer is yes, the dependency direction is doing its job.

---

## Bridge to the next lesson

In this lesson, we improved dependency direction by making one boundary explicit.

That gives us a cleaner architectural shape:

- the core defines what it needs
- the edge provides the implementation
- `main()` patches the concrete pieces together

In the next lesson, we build on that by shifting the focus more directly toward protecting the domain core itself.