# Types as a Design Tool

## Overview

Type annotations are often introduced as a tooling feature. They help with autocomplete, static analysis, and catching mistakes earlier.

But from a design perspective, their most important role is this:

> Types make intent visible.

A well-designed system should communicate its structure through its interfaces. When you read a function signature, you should be able to understand what kind of data it expects, what kind of data it returns, and how it is meant to be used.

You should not always need to read the full implementation to understand the contract.

## Starting Point

In this lesson, we start from a simplified booking system with rooms, bookings, repositories, and a pricing policy.

The code already has some structure, but many function signatures are still implicit:

```python
class BookingService:
    def __init__(self, booking_repository, room_repository, pricing_policy):
        self._booking_repository = booking_repository
        self._room_repository = room_repository
        self._pricing_policy = pricing_policy

    def create_booking(
        self,
        guest_name,
        guest_email,
        room_number,
        nights,
    ):
        ...
```

This works, but the interface does not tell us enough.

What is `guest_name`? What is `room_number`? What does `create_booking` return? What does `room_repository.get()` return?

Types help answer those questions directly at the boundary.

## Types Communicate Intent

Compare this untyped signature:

```python
def create_booking(
    self,
    guest_name,
    guest_email,
    room_number,
    nights,
):
    ...
```

with this typed version:

```python
def create_booking(
    self,
    guest_name: str,
    guest_email: str,
    room_number: int,
    nights: int,
) -> Booking:
    ...
```

Now we immediately know that:

- `guest_name` is text
- `guest_email` is text
- `room_number` is an integer
- `nights` is an integer
- the method returns a `Booking`

This makes the code easier to understand without reading the full method body.

Return types also communicate intent:

```python
def save(self, booking: Booking) -> None:
    ...
```

The `-> None` tells us that this method performs an action. It changes state, but it does not return meaningful domain data.

## Types as Contracts

Types are not just comments or documentation. They form contracts between parts of the system.

Consider this pricing method:

```python
def calculate_total_price(self, room, nights):
    ...
```

The method may work, but the interface is vague. We do not know what `room` is supposed to be, what `nights` should be, or what the method returns.

A stronger version is:

```python
def calculate_total_price(
    self,
    room: Room,
    nights: int,
) -> Decimal:
    ...
```

Now the contract is explicit. The method expects a `Room`, an integer number of nights, and returns a `Decimal`.

The same applies to repositories:

```python
def get(self, room_number: int) -> Room | None:
    ...
```

This tells us that a room lookup may succeed or fail. The caller must handle both possibilities.

## Types Force Better Modeling

One of the most important design benefits of types is that they force us to think about the shape of the data.

For example:

```python
def save(self, booking: Booking) -> None:
    ...
```

This annotation reflects a design decision. The repository stores `Booking` objects, not dictionaries, request payloads, or arbitrary data.

Similarly:

```python
def get(self, room_number: int) -> Room | None:
    ...
```

forces us to be clear about what a room lookup means. It returns either a `Room` or nothing.

Types often reveal where the design is still unclear. That is useful feedback.

## Type Aliases

Sometimes a type is technically correct, but not very expressive.

```python
guest_name: str
guest_email: str
room_number: int
```

These annotations are valid, but they do not fully communicate the role these values play in the domain.

Type aliases let us give names to important concepts:

```python
type GuestName = str
type GuestEmail = str
type RoomNumber = int
```

Now the model can become more expressive:

```python
@dataclass
class Booking:
    guest_name: GuestName
    guest_email: GuestEmail
    room_number: RoomNumber
    nights: int
    total_price: Decimal
    status: BookingStatus = BookingStatus.PENDING
```

This does not create a new runtime type. It also does not enforce invariants yet. But it does make the domain language clearer.

## Aliases for Complex Types

Aliases are also useful when types become long or hard to read.

Instead of repeating this:

```python
dict[str, Decimal]
```

we can introduce a name:

```python
type PriceBreakdown = dict[str, Decimal]
```

Instead of repeating this:

```python
tuple[date, date]
```

we can write:

```python
type DateRange = tuple[date, date]
```

This keeps signatures readable and gives names to important concepts.

## Different Parts Need Different Concepts

A booking stores a room number:

```python
room_number: RoomNumber
```

But the pricing policy works with a full room object:

```python
def calculate_total_price(
    self,
    room: Room,
    nights: int,
) -> Decimal:
    ...
```

That is fine.

The booking only needs to remember which room was booked. The pricing policy needs access to room data, such as `price_per_night`.

The important question is:

> Which concept does this part of the system actually need?

Types help make that distinction visible.

## General Input Types

For input parameters, prefer the most general type that matches what the function actually needs.

For example:

```python
def total_revenue(bookings: list[Booking]) -> Decimal:
    ...
```

If the function only loops over the bookings, requiring a `list` is more specific than necessary.

A better version is:

```python
from collections.abc import Iterable

def total_revenue(bookings: Iterable[Booking]) -> Decimal:
    ...
```

Now the function accepts lists, tuples, sets, generators, or any other iterable.

The function only needs iteration, so the type should reflect that.

> Accept the most general input type that satisfies the requirements.

This reduces unnecessary coupling.

## Specific Return Types

Return types follow the opposite rule.

Return the most specific type that truthfully describes the result.

For example:

```python
def all(self) -> Iterable[Booking]:
    ...
```

This works, but it hides useful information.

If the method returns a list, say so:

```python
def all(self) -> list[Booking]:
    ...
```

Now callers know exactly what they receive.

Another common example is this:

```python
def create_booking(...) -> Booking | None:
    ...
```

Sometimes that is appropriate. But often it spreads uncertainty throughout the codebase.

If invalid input should be exceptional, a stronger contract is usually better:

```python
def create_booking(...) -> Booking:
    ...
```

Then invalid situations can be handled explicitly with exceptions.

## Modern Collection Types

Older Python code often uses types from `typing`:

```python
from typing import List, Dict

bookings: List[Booking]
rooms: Dict[int, Room]
```

Modern Python prefers built-in generic types:

```python
bookings: list[Booking]
rooms: dict[int, Room]
```

For abstract collection types, prefer importing from `collections.abc`:

```python
from collections.abc import Iterable, Mapping
```

This is especially useful for argument types where you want to depend on behavior rather than a concrete container.

## AI Coding Tools and Types

AI-generated code often weakens type quality in predictable ways.

### Overly Broad Types

```python
def handle(data: Any) -> Any:
    ...
```

This communicates almost nothing.

### Unnecessary Optional Results

```python
def create_booking(...) -> Booking | None:
    ...
```

Every caller now has to handle an additional case.

### Unnecessary Optional Inputs

```python
def create_booking(
    guest_name: str | None = None,
):
    ...
```

Optionality should exist only when the design actually requires it.

### Outdated Syntax

AI often generates older syntax:

```python
from typing import List, Dict
```

Modern Python usually prefers:

```python
list[Booking]
dict[int, Room]
```

When AI generates type annotations, do not only ask whether the code runs. Ask whether the types express the design clearly.

## Key Takeaways

Types are a design tool.

Good type annotations:

- communicate intent
- clarify contracts
- expose domain concepts
- encourage better modeling decisions
- reduce ambiguity at boundaries

The key guidelines are:

- Use types to make interfaces clearer.
- Use aliases when names add meaning.
- Accept inputs as generally as possible.
- Return outputs as specifically as possible.
- Treat types as part of the design, not as an afterthought.

In the next lesson, we move beyond expressing intent with types and start enforcing important rules directly through invariants.