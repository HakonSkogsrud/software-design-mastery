# Lecture Notes - Designing Around Reasons to Change

## Overview

In Level 1, we focused on improving software structure locally. We introduced domain objects, separated responsibilities inside functions, and made the booking flow easier to understand.

In this lesson, we take the next step.

The challenge is no longer a messy function. Instead, the challenge is what happens when the system grows and new requirements arrive.

A common mistake is to add new behavior directly into the nearest function that seems relevant. This often works at first, but over time the same business rule starts appearing in multiple places, making the system harder to change safely.

The key idea of this lesson is:

> A responsibility should be separated when it has its own reason to change.

We will see how a new approval rule creates pressure across multiple use cases and how identifying that rule as a separate responsibility leads to a cleaner design.

---

## A New Requirement

Our booking system currently creates bookings and supports room upgrades.

Now the hotel introduces a new rule:

> Suite bookings should start as `PENDING` instead of `CONFIRMED`.

At first glance, this looks like a small change.

The obvious implementation is to modify `book_room()`:

```python
status = BookingStatus.CONFIRMED

if room.room_type == "suite":
    status = BookingStatus.PENDING
```

This is a reasonable first step.

The problem appears when the system evolves further.

---

## The Preview Booking Feature

The business now asks for a new feature:

> Allow guests to preview a booking before actually creating it.

The preview should show:

- the total price
- the initial booking status

To implement this, we add a `preview_booking()` function.

That function also needs to determine whether the booking starts as `CONFIRMED` or `PENDING`.

A common implementation looks like this:

```python
status = BookingStatus.CONFIRMED

if room.room_type == "suite":
    status = BookingStatus.PENDING
```

Now the approval rule exists in two places.

---

## Why Duplication Is Not the Real Problem

It is tempting to say:

> The problem is duplication.

But duplication is only the symptom.

The real issue is that we have discovered a new business decision:

> What should the initial status of a booking be?

That decision is conceptually different from:

- validating a booking
- calculating a price
- storing a booking
- sending confirmations

It changes for different reasons.

That is what makes it a separate responsibility.

---

## Responsibility and Change Vectors

Throughout this course, we define responsibility in terms of change.

A responsibility exists when a piece of logic changes for its own reasons.

The approval rule is a good example:

- approval rules may change
- pricing rules may change
- validation rules may change

These changes are unrelated.

Because approval rules evolve independently, they deserve their own home in the design.

---

## Broken Consistency

The approval rule now exists in:

- `book_room()`
- `preview_booking()`

But we also have `upgrade_room()`.

Suppose the business clarifies the requirement:

> Any booking involving a suite should require approval.

That means:

- creating a suite booking → `PENDING`
- previewing a suite booking → `PENDING`
- upgrading into a suite → `PENDING`

However, the existing upgrade flow knows nothing about this rule.

As a result, a booking can be upgraded into a suite while remaining `CONFIRMED`.

This is an important design signal.

When a rule starts affecting multiple use cases, it is often no longer a detail of any one use case.

It is a separate concept.

---

## Extracting the Approval Decision

Instead of embedding the approval rule inside individual flows, we separate it:

```python
def initial_booking_status(room):
    if room.room_type == "suite":
        return BookingStatus.PENDING

    return BookingStatus.CONFIRMED
```

Now both `book_room()` and `preview_booking()` use the same function:

```python
status = initial_booking_status(room)
```

This is not about creating tiny functions.

The function exists because the approval decision has its own reason to change.

---

## CARDS Perspective

### Clarity

The approval decision now has a name.

Instead of being buried inside multiple use cases, it is visible as its own concept.

```python
initial_booking_status(room)
```

The code communicates intent more clearly.

### Resilience

If approval rules change, there is only one place to update.

Changes stay localized instead of spreading across multiple flows.

### Separation

Booking creation and approval policy are now distinct concerns.

The booking flow coordinates work.

The approval function decides status.

Each responsibility has a clearer role.

---

## What About `upgrade_room()`?

Once approval logic is separated, another design question appears:

> Should `upgrade_room()` also use the same approval rule?

In our example, the answer is probably yes.

If moving into a suite requires approval, then upgrading into a suite should also result in a `PENDING` booking.

The important point is that this becomes much easier to see once the rule has its own home.

---

## Should the Logic Move Into `change_room()`?

A natural question is whether the approval logic belongs inside the `Booking` entity.

For example:

```python
booking.change_room(...)
```

Could that method automatically recalculate status?

### Arguments for Moving It Inside

If every room change must always re-evaluate booking status, putting the logic closer to the state change can be safer.

This reduces the risk that a caller forgets to apply the rule.

### Arguments for Keeping It Separate

The `change_room()` method currently has a simple responsibility:

```text
change the room
change the price
```

It does not know about:

- approval workflows
- room policies
- business rules

Keeping approval logic separate preserves that simplicity.

The approval decision remains an explicit policy instead of becoming hidden inside a state mutation.

### The Trade-Off

Move the logic into the entity when:

- status recalculation is a true domain invariant
- every room change must always enforce it

Keep it separate when:

- approval is a distinct business policy
- different workflows may apply it differently
- you want the decision to remain explicit

For this lesson, keeping the rule separate is the simpler and clearer design.

---

## AI Guardrail

AI coding tools often make the initial change correctly:

```python
if room.room_type == "suite":
    status = BookingStatus.PENDING
```

The problem is what happens next.

When new use cases are added, AI tools frequently:

- duplicate the rule
- copy it into another function
- miss a third place that should also use it

When reviewing AI-generated code, ask:

> Is this logic specific to this flow, or is it a business decision that multiple flows depend on?

If multiple flows depend on it, that logic probably deserves its own home.

---

## Key Takeaways

- New requirements often reveal hidden responsibilities.
- Duplication is frequently a symptom of a deeper design issue.
- The important question is not:

  > Can this code be reused?

- The important question is:

  > Does this logic have its own reason to change?

- In this lesson, the approval rule became a separate responsibility because:
  - multiple use cases depended on it
  - it evolved independently from booking creation
  - it introduced consistency problems when duplicated

- Separating the approval decision improved:
  - **Clarity**
  - **Resilience**
  - **Separation**

---

## Bridge to the Next Lesson

In this lesson, we separated a responsibility because it had its own reason to change.

But once responsibilities become distinct, a new question appears:

> How should we combine behavior when requirements become more varied?

One common response is inheritance.

Unfortunately, inheritance often creates new forms of coupling and rigidity.

In the next lesson, we'll explore why composition is usually a safer way to extend behavior and how it helps systems evolve without becoming tangled.