# Lecture Notes — Designing Invariants That Enforce Themselves

## Overview

In the previous lesson, we used type annotations and type aliases to make intent clearer. That improved **Clarity**. We could see what values functions expected, what they returned, and what kind of data was moving through the system.

But there is an important limit to that improvement:

Type annotations can describe intent, but they do not guarantee validity.

That is the focus of this lesson.

This lesson is mainly about **Domain Integrity** in the CARDS framework, and it also strengthens **Clarity**. A model becomes easier to understand once it becomes easier to trust.

---

## From clearer types to stronger guarantees

Type aliases like these are useful:

```python
type GuestName = str
type GuestEmail = str
type RoomNumber = int
```

These aliases improve readability. They tell us what role a value is supposed to play.

But they do not change runtime behavior.

- `GuestEmail` is still just a string
- `RoomNumber` is still just an integer

That means aliases help us communicate intent, but they do not enforce the rules of the domain.

This is the key transition from the previous lesson into this one:

- the previous lesson improved the **communication** of the code
- this lesson improves the **integrity** of the model

---

## A typed model can still be weak

The starting point for the lesson already looks better than an untyped script:

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

This is clearer than a dictionary. It is typed. It is easier to read.

But the key question is not whether the model looks structured.

The real question is:

**What does this model allow?**

At this point, it still allows too much.

- `guest_email: GuestEmail` still allows any string
- `room_number: RoomNumber` is still just an integer
- `nights: int` still allows `0` or negative values
- `guest_name` can still be empty
- `total_price` can still be negative

So even though the code is cleaner, invalid state is still representable.

That is the core smell in this lesson.

---

## Why scattered validation is a problem

Because the model is weak, the service starts compensating:

```python
def create_booking(
    self,
    guest_name: GuestName,
    guest_email: GuestEmail,
    room_number: RoomNumber,
    nights: int,
) -> Booking:
    room = self._room_repository.get(room_number)

    if room is None:
        raise ValueError("Room does not exist")

    if nights <= 0:
        raise ValueError("Nights must be at least 1")
```

This may look reasonable at first, but it reveals a design problem:

The service is protecting rules that really belong closer to the model.

Worse, the service is not the only way to create a booking. Because the `Booking` dataclass still accepts raw primitives, invalid objects can still be created directly:

```python
broken = Booking(
    guest_name="",
    guest_email="not-an-email",
    room_number=101,
    nights=0,
    total_price=Decimal("-100.00"),
    status=BookingStatus.PENDING,
)
```

That object should never exist.

But it can.

Once that happens, every other part of the system has to treat the model with suspicion and add more checks.

That is the deeper issue here:

**If invalid state is representable, the rest of the system becomes defensive.**

---

## What an invariant is

The key concept in this lesson is the invariant.

An invariant is a rule that must always hold whenever an object exists.

Not sometimes.  
Not only when created through one service.  
Always.

In this booking example, some obvious invariants are:

- nights must be at least 1
- guest email must be valid
- guest name cannot be empty
- total price cannot be negative

These are not optional preferences. They help define what a valid booking actually is.

That leads to an important distinction:

- input at the system boundary can be invalid
- domain objects should not be

Once data enters the domain model, we want stronger guarantees.

---

## Why primitives are often too weak

The root problem is that primitives such as `str` and `int` can represent both valid and invalid domain values.

A plain string can be:
- a valid email address
- an empty guest name
- complete nonsense

A plain integer can be:
- a valid number of nights
- zero
- negative

Type aliases do not solve this, because they do not add constraints.

That is why this lesson introduces a stronger design move:

Replace weak aliases and dangerous primitives with domain concepts that carry both meaning and rules.

---

## Replacing dangerous primitives with domain concepts

### `EmailAddress`

```python
@dataclass(frozen=True, slots=True)
class EmailAddress:
    value: str

    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise ValueError("Guest email must be valid")
```

Previously, `GuestEmail` was just an alias for `str`.

Now the rule lives inside the type itself.

This means:
- `EmailAddress("alice@example.com")` is valid
- `EmailAddress("not-an-email")` fails immediately

This is a small but important shift. The email is no longer just data. It is a domain concept with its own invariant.

### `StayNights`

```python
@dataclass(frozen=True, slots=True)
class StayNights:
    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValueError("Nights must be at least 1")
```

Previously, nights were stored as a plain integer. That made invalid values easy to represent.

Now the rule is attached to the type:
- `StayNights(3)` is valid
- `StayNights(0)` fails immediately

This gives us stronger guarantees without having to remember to re-check the value elsewhere.

### Why this matters

This is the main structural move in the lesson:

We stop representing important domain concepts as weak primitives, and we start giving them structure.

That is how the model begins to protect itself.

---

## Moving invariants into the model

Once stronger domain types exist, `Booking` can depend on them instead of raw primitives.

```python
@dataclass
class Booking:
    guest_name: GuestName
    guest_email: EmailAddress
    room_number: RoomNumber
    nights: StayNights
    total_price: Decimal
    status: BookingStatus = BookingStatus.PENDING

    def __post_init__(self) -> None:
        if not self.guest_name.strip():
            raise ValueError("Guest name cannot be empty")

        if self.total_price < 0:
            raise ValueError("Total price cannot be negative")
```

This is an important change.

`Booking` is now harder to misuse because:
- email is already validated before it enters the booking
- nights are already validated before they enter the booking
- the booking itself rejects an empty guest name
- the booking itself rejects a negative total price

This does not make the model perfect, but it makes invalid bookings much harder to create.

That is the point of the lesson.

We are not trying to model everything at once. We are strengthening the parts of the model where invalid state is currently too easy to create.

---

## Services become simpler

Once the model carries more of the integrity, the service no longer needs to act as a validator for every field.

Instead, it becomes a place where boundary input is turned into domain concepts:

```python
room = self._room_repository.get(room_number)
if room is None:
    raise ValueError("Room does not exist")

validated_email = EmailAddress(guest_email)
validated_nights = StayNights(nights)

total_price = self._pricing_policy.calculate_total_price(
    room=room,
    nights=validated_nights.value,
)

booking = Booking(
    guest_name=guest_name,
    guest_email=validated_email,
    room_number=room.number,
    nights=validated_nights,
    total_price=total_price,
    status=BookingStatus.PENDING,
)
```

This is a healthier separation of responsibilities.

The service still has a job, but it is a different job now:

- look up the room
- coordinate the policy
- convert raw input into validated domain concepts
- create the booking

The service orchestrates.

The model protects its own validity.

That improves **Clarity** because responsibilities are sharper, and it improves **Domain Integrity** because fewer rules depend on callers remembering to do the right thing.

---

## Hard invariants vs soft policies

One of the most important distinctions in the lesson is that not every rule belongs inside the model.

Some rules define validity.  
Other rules are business policies that may change.

### Hard invariants

Hard invariants are rules that must never be broken. They define whether an object is valid at all.

In this example:
- nights must be at least 1
- guest email must be valid
- guest name cannot be empty
- total price cannot be negative

These belong inside the model or inside the small domain types the model depends on.

### Soft policies

Soft policies are different. They may change because the business changes its mind.

Examples include:
- pricing formulas
- discounts
- surcharges
- special offers

In this codebase, `PricingPolicy` stays outside the model:

```python
class PricingPolicy:
    def calculate_total_price(self, room: Room, nights: int) -> Decimal:
        return room.price_per_night * nights
```

That is a good design choice because pricing is not what makes a booking valid. It is a business rule that may evolve over time.

This is the rule of thumb:

- hard invariants go inside the model
- soft policies stay outside it

That keeps the model strong without making it rigid.

---

## AI guardrail

This lesson also includes an important warning about AI-generated code.

AI tools often weaken a model in a subtle way by “fixing” invalid data instead of rejecting it.

For example:

```python
nights = max(nights, 1)
```

This may look helpful, but it is actually dangerous.

Instead of rejecting invalid input, the code silently changes it. That hides the real problem and weakens the guarantees of the model.

A better rule is:

**Never silently normalize invalid domain data. Reject it early.**

If a value is invalid in the domain, the system should fail where that value enters the model.

---

## Final structure of the code

By the end of the lesson, the code has this overall shape:

- weak primitive aliases are replaced where they are too dangerous
- `EmailAddress` and `StayNights` enforce their own invariants
- `Booking` enforces its own remaining core rules
- `BookingService` becomes simpler and more focused
- `PricingPolicy` remains outside the model as a soft policy

This is a stronger design because the model becomes easier to trust.

---

## Key takeaways

- Type annotations and aliases improve readability, but they do not enforce validity.
- A domain model is weak if invalid state is still easy to represent.
- Invariants are rules that must always hold whenever an object exists.
- Dangerous primitives should often be replaced by explicit domain concepts.
- Services should orchestrate, not carry all validation logic.
- Hard invariants belong inside the model.
- Soft policies should stay outside it.

---

## Bridge to the next lesson

At this point, some concepts are starting to become more explicit:

- `EmailAddress`
- `StayNights`

And we already had `BookingStatus` as an earlier example of a stronger type.

These are more than just validation helpers. They are beginning to show the shape of the domain.

That leads naturally to the next question:

- which of these are value objects?
- which concepts carry identity?
- which concepts are really entities?

That is the focus of the next lesson, where the domain model starts to take clearer structural shape.