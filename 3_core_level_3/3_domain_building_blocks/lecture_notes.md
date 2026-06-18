# Lecture Notes — Modeling Domain Building Blocks

## Overview

In the previous lesson, we started improving the booking system by replacing a few raw primitives with explicit domain concepts like `EmailAddress` and `StayNights`.

This lesson builds on that step.

The goal here is not just to add more classes. The goal is to make better modeling decisions by asking:

- Which concepts are **value objects**?
- Which concepts are **entities**?
- Which concepts do we **not need to model at all**?

This helps the code better reflect the business domain, which improves both **clarity** and **domain integrity**.

---

## Primitive Obsession

A common design problem is **primitive obsession**.

This happens when meaningful domain concepts are represented everywhere as raw:

- `str`
- `int`
- `Decimal`
- `bool`

That may look simple at first, but it hides meaning.

For example:

- an email address is not just any string
- the number of nights is not just any integer
- a price is not just any decimal

When we leave meaningful concepts as primitives, rules tend to spread out into services, helper functions, and conditionals.

Instead, we can introduce explicit domain types where they give us clearer intent and better protection.

---

## Entity vs Value Object

This lesson introduces two important ideas from domain modeling:

- **Value Object**
- **Entity**

These terms are commonly used in domain-driven design.

### Value Object

A **value object** is defined by what it contains.

If two instances have the same contents, they mean the same thing.

Examples from this script:

- `EmailAddress`
- `StayNights`
- `Money`

These are meaningful values. We care about whether they are valid, not about tracking one specific instance over time.

Value objects are often:

- immutable
- validated when created
- interchangeable when their values are the same

### Entity

An **entity** is defined by identity over time.

Its attributes may change, but it is still the same thing.

Examples from this script:

- `Room`
- `Booking`

We care about a specific room and a specific booking as things the system tracks over time.

Entities are often:

- stored and retrieved by identity
- changed over time
- part of the long-lived state of the system

---

## Practical Questions to Tell Them Apart

When deciding whether something is an entity or a value object, these questions help.

### Questions that suggest an entity

- Does the system care about this as the **same thing over time**?
- Does it have a **lifecycle**?
- Would we **store and retrieve** it as its own thing?

### Questions that suggest a value object

- If two instances contain the same data, are they **interchangeable**?
- Is this mainly a **meaningful value** or measurement?
- Would it be safer if it were **immutable**?

These are not rigid rules. They are practical modeling heuristics.

---

## The Code

## Type Aliases

```python
type BookingId = str
type GuestName = str
type RoomNumber = int
```

These aliases improve readability.

They do **not** create new runtime types, but they make intent clearer.

For example:

- `BookingId` tells us a string is being used as an identifier
- `RoomNumber` tells us an integer is being used as a room reference

This is lighter than creating a full class.

That is sometimes exactly the right choice.

---

## BookingStatus

```python
class BookingStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
```

`BookingStatus` is a small domain concept represented as an enum.

This is more meaningful than raw status strings spread throughout the code.

It gives us:

- a fixed set of valid states
- clearer intent
- fewer typos and invalid values

Even though it is simple, it still improves the model.

---

## EmailAddress

```python
@dataclass(frozen=True, slots=True)
class EmailAddress:
    value: str

    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise ValueError("Guest email must be valid")
```

`EmailAddress` is a value object.

### Why it is a value object

Because it is defined by its value. Two `EmailAddress("alice@example.com")` objects mean the same thing.

### Why `frozen=True`

This makes the object immutable.

That is a good fit for value objects because once an email address is validated, we usually want it to stay trustworthy.

### Why `slots=True`

This reduces instance overhead and prevents arbitrary new attributes from being added.

That is not the main lesson here, but it is a good fit for small domain objects.

### Validation in `__post_init__`

The object validates itself when created.

This is important because it keeps the rule close to the data.

Instead of checking email validity all over the system, the object enforces it once.

---

## StayNights

```python
@dataclass(frozen=True, slots=True)
class StayNights:
    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValueError("Nights must be at least 1")
```

`StayNights` is another value object.

### Why it is useful

A plain `int` does not tell us much.

`StayNights` tells us:

- what the number means
- what rule applies to it

### Invariant

The number of nights must be at least 1.

That rule is now protected directly by the type.

This is a good example of how value objects help fight primitive obsession.

---

## Money

```python
@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Money cannot be negative")

    def __add__(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)

    def __mul__(self, multiplier: int) -> "Money":
        return Money(self.amount * multiplier)
```

`Money` is also a value object.

### Why use Money instead of raw Decimal

A price is not just a number. It is a meaningful domain value.

By introducing `Money`, the code becomes clearer and safer.

### Validation

Negative money values are rejected at creation time.

### Behavior

`Money` supports:

- addition with another `Money`
- multiplication by an integer

This is useful because it lets us express domain logic directly in terms of domain concepts.

For example:

- room price times number of nights
- total revenue plus booking price

This is better than repeatedly manipulating raw decimals throughout the system.

---

## Room

```python
@dataclass
class Room:
    number: RoomNumber
    room_type: str
    price_per_night: Money
```

`Room` is an entity.

### Why `Room` is an entity

Because a room is something the system tracks over time.

Room 101 is still Room 101 even if:

- its price changes
- its room type changes
- the hotel updates some related information later

Identity matters here.

### Current design choice

`room_type` is still a `str`.

That is acceptable for now.

The script intentionally keeps this simple and points out that not every concept needs a heavier abstraction immediately.

A future version might introduce a `RoomType` enum or value object, but this lesson does not require it yet.

---

## Booking

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

    def __post_init__(self) -> None:
        if not self.guest_name.strip():
            raise ValueError("Guest name cannot be empty")
```

`Booking` is also an entity.

### Why `Booking` is an entity

Because a booking is something the system tracks over time.

It has:

- an identity: `booking_id`
- a state: `status`
- persistence in the repository

Even though this script does not add behavior like `confirm()` or `cancel()`, the structure already suggests that a booking is something long-lived and important to the business.

### Current design choice

`Booking` stores `room_number`, not a full `Room` object.

That is intentional.

This lesson is focused on distinguishing entities from value objects, not yet on designing stronger aggregate relationships.

---

## RoomRepository

```python
class RoomRepository:
    def __init__(self) -> None:
        self._rooms: dict[RoomNumber, Room] = {
            101: Room(
                number=101,
                room_type="single",
                price_per_night=Money(Decimal("100.00")),
            ),
            102: Room(
                number=102,
                room_type="double",
                price_per_night=Money(Decimal("140.00")),
            ),
            201: Room(
                number=201,
                room_type="suite",
                price_per_night=Money(Decimal("220.00")),
            ),
        }

    def get(self, room_number: RoomNumber) -> Room | None:
        return self._rooms.get(room_number)

    def all(self) -> list[Room]:
        return list(self._rooms.values())
```

This repository stores and retrieves `Room` entities.

### Purpose

It provides access to rooms without spreading storage details across the rest of the code.

### Why it matters here

Even in this simple in-memory form, it reinforces the idea that `Room` is a tracked object in the system.

### Initial room data

The repository starts with three rooms:

- 101 — single — 100.00
- 102 — double — 140.00
- 201 — suite — 220.00

Notice that prices are stored as `Money`, not raw `Decimal`.

---

## BookingRepository

```python
class BookingRepository:
    def __init__(self) -> None:
        self._bookings: list[Booking] = []

    def save(self, booking: Booking) -> None:
        self._bookings.append(booking)

    def all(self) -> list[Booking]:
        return self._bookings
```

This repository stores `Booking` entities.

### Purpose

It is a simple in-memory collection for this stage of the course.

### Why it matters

Like `RoomRepository`, it reinforces the idea that a booking is a tracked business object.

---

## PricingPolicy

```python
class PricingPolicy:
    def calculate_total_price(self, room: Room, nights: StayNights) -> Money:
        return room.price_per_night * nights.value
```

This class calculates booking price.

### Inputs

- a `Room`
- `StayNights`

### Output

- `Money`

### Why this is a good fit

The method works with domain concepts, not low-level primitive values.

That gives us clearer code:

- `room.price_per_night`
- `nights.value`

And it returns a meaningful result type: `Money`.

---

## BookingService

```python
class BookingService:
    def __init__(
        self,
        booking_repository: BookingRepository,
        room_repository: RoomRepository,
        pricing_policy: PricingPolicy,
    ) -> None:
        self._booking_repository = booking_repository
        self._room_repository = room_repository
        self._pricing_policy = pricing_policy
```

This service coordinates booking creation.

It depends on:

- `BookingRepository`
- `RoomRepository`
- `PricingPolicy`

### `create_booking`

```python
def create_booking(
    self,
    booking_id: BookingId,
    guest_name: GuestName,
    guest_email: str,
    room_number: RoomNumber,
    nights: int,
) -> Booking:
```

The method starts with input values, some of which are still primitives.

Inside the method:

1. it retrieves the room
2. validates the email by creating `EmailAddress`
3. validates the number of nights by creating `StayNights`
4. calculates price using `PricingPolicy`
5. creates a `Booking`
6. saves the booking

### Why this is useful

This shows a common pattern:

- external input starts simple
- the service turns it into domain concepts
- the domain model stays clearer and safer

### Important detail

If the room does not exist, the service raises:

```python
raise ValueError("Room does not exist")
```

This is a simple guard against invalid booking requests.

---

## total_revenue

```python
def total_revenue(bookings: Iterable[Booking]) -> Money:
    total = Money(Decimal("0.00"))
    for booking in bookings:
        if booking.status is not BookingStatus.CANCELLED:
            total = total + booking.total_price
    return total
```

This function calculates revenue from a collection of bookings.

### Why `Iterable[Booking]`

This keeps the function flexible.

It can work with:

- a list
- another iterable source
- repository results

### Why return `Money`

Returning `Money` keeps the result in domain terms.

That is more expressive than returning a raw decimal.

### Cancellation check

Cancelled bookings are excluded from revenue.

Even though this lesson is not focused on booking lifecycle behavior, the status still affects reporting logic.

---

## main

```python
def main() -> None:
    booking_repository = BookingRepository()
    room_repository = RoomRepository()
    pricing_policy = PricingPolicy()

    booking_service = BookingService(
        booking_repository=booking_repository,
        room_repository=room_repository,
        pricing_policy=pricing_policy,
    )

    booking = booking_service.create_booking(
        booking_id="BKG-001",
        guest_name="Alice Johnson",
        guest_email="alice@example.com",
        room_number=101,
        nights=3,
    )

    print("Created:", booking)
    print("Rooms:", room_repository.all())
    print("All bookings:", booking_repository.all())
    print("Total revenue:", total_revenue(booking_repository.all()).amount)
```

The `main` function wires everything together.

### What it does

- creates repositories and pricing policy
- creates the service
- creates one booking
- prints:
  - the created booking
  - all rooms
  - all bookings
  - total revenue

### Why this is useful in a teaching context

It gives a small runnable example of the whole model working together.

---

## What This Lesson Is Really Teaching

This lesson is not mainly about dataclasses, enums, or repositories.

It is teaching a modeling habit:

- do not leave meaningful concepts as loose primitives when the domain clearly has rules
- but also do not model everything

That balance matters.

### Concepts we model here

- `EmailAddress` — value object
- `StayNights` — value object
- `Money` — value object
- `Room` — entity
- `Booking` — entity

### Concepts we do **not** model

Not every concept in the real world of a hotel belongs in this booking model.

Examples:

- `HotelClerk`
- `RoomService`
- the piano in the lobby

These may exist in the business world, but they are not important to this slice of the booking domain.

This is where **YAGNI** applies:

> You Aren’t Gonna Need It.

Keep the model focused.

---

## Design Takeaways

### 1. Not every concept should be a primitive
Wrapping a primitive can make the model clearer and safer when the value has business meaning.

### 2. Not every concept needs a full abstraction immediately
Some concepts can stay simple until the model really needs more structure.

### 3. Value objects and entities serve different purposes
- value objects represent meaningful values
- entities represent things the system tracks over time

### 4. Good domain modeling is selective
The goal is not “more classes.”
The goal is a clearer and more trustworthy model.

---

## Recap

By the end of this lesson:

- `EmailAddress`, `StayNights`, and `Money` are modeled as value objects
- `Room` and `Booking` are modeled as entities
- repositories store those entities
- the service turns raw input into domain concepts
- pricing and revenue calculations now use `Money`

This gives us a stronger foundation for later lessons, where the model will need more protection and clearer boundaries.