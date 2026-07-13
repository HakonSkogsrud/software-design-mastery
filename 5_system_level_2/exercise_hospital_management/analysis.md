> Don't read any further until you tried coming up with a solution yourself!

# Solution & Analysis

## Overview

This exercise focuses on one of the most important software design skills: organizing a growing codebase so that it remains understandable and maintainable over time.

There is no single "correct" folder structure. Instead, the goal is to create a structure that communicates responsibilities clearly, minimizes unnecessary coupling, and makes future changes easier.

When evaluating your solution, ask yourself these questions:

- Can I easily predict where new functionality belongs?
- Are related concepts grouped together?
- Are dependencies pointing in a sensible direction?
- Does the structure reflect the business domain rather than implementation details?

---

# Problem 1 — Organizing by Technical Type

The original project was organized like this:

```text
models/
services/
repositories/
```

This is a very common starting point, but it becomes problematic as applications grow.

Consider adding a new feature such as appointment reminders.

Where should the code go?

- `models/`
- `services/`
- `repositories/`

The answer is usually "all of them."

A single feature becomes scattered across multiple directories.

As a result:

- Developers constantly jump between folders.
- Understanding a workflow requires opening many files.
- Related code becomes physically separated.

The structure reflects *how* the code is implemented instead of *what* the software actually does.

---

# A Better Organization

A stronger design groups code by responsibility.

For example:

```text
src/
    patients/
    appointments/
    billing/
    laboratory/
    notifications/
    infrastructure/
```

Now each directory owns a particular part of the business domain.

Inside `appointments`, for example, you might have:

```text
appointments/
    models.py
    scheduling.py
    reminders.py
```

Everything related to appointments lives together.

When adding appointment functionality, developers immediately know where to start.

This improves **Clarity**.

---

# Problem 2 — Weak Ownership

In the original structure, ownership is unclear.

Who owns appointment scheduling?

- `appointment.py`
- `appointment_service.py`
- `appointment_repository.py`

Ownership is spread across several folders.

Responsibility-based organization gives each area a clear home.

For example:

```text
appointments/
```

becomes the natural owner of everything related to appointments.

This improves discoverability and reduces hesitation during development.

---

# Problem 3 — Growing Coupling

Another issue is coupling.

In many projects like this, service classes begin importing one another.

For example:

```text
billing_service
    ↓
appointment_service
    ↓
notification_service
    ↓
patient_service
```

Eventually these dependencies start pointing in multiple directions.

The system becomes difficult to understand because no module has a clearly defined boundary.

A good solution reduces these cross-feature dependencies.

If appointments need patient information, importing a patient model is reasonable.

However, appointment scheduling should not depend on billing logic.

Keeping dependency directions simple supports **Alignment**.

---

# Problem 4 — Dumping Grounds

The original project contained:

```text
utils.py
helpers.py
```

These files often begin with a single helper function.

Over time they accumulate unrelated responsibilities.

Eventually they become some of the most heavily imported modules in the project.

This creates hidden coupling because many unrelated parts of the system now depend on the same file.

Instead, helper functions should usually live close to the responsibility they support.

For example:

```text
appointments/
    formatting.py
```

or

```text
laboratory/
    parsing.py
```

Keeping supporting logic close to the feature that owns it makes dependencies easier to understand.

---

# Splitting Large Modules

One of the assignment tasks was identifying a module that should be split.

Many answers are possible.

For example:

```text
notification_service.py
```

might currently contain:

- email notifications
- SMS notifications
- push notifications
- appointment reminders
- billing reminders

These responsibilities change independently.

Splitting them into focused modules makes future changes smaller.

For example:

```text
notifications/
    email.py
    sms.py
    push.py
```

or perhaps:

```text
notifications/
    appointment_notifications.py
    billing_notifications.py
```

Exactly how you split the module depends on which responsibilities tend to change together.

A useful guideline is:

> Code that changes together should usually live together.

---

# Naming Matters

Strong module names communicate responsibility.

For example:

Good:

```text
appointments/
billing/
patients/
```

Less helpful:

```text
processing/
common/
shared/
```

Specific names reduce cognitive load because developers can predict where functionality belongs.

Consistency is generally more important than finding the perfect name.

---

# CARDS Analysis

## Clarity

Responsibility-based folders communicate intent.

Developers spend less time searching for functionality.

---

## Alignment

Dependencies become easier to reason about.

Instead of services importing one another arbitrarily, each responsibility owns its own behavior.

Dependency directions become more consistent.

---

## Separation

Different business capabilities become isolated.

Appointments, billing, and laboratory code evolve more independently.

Changes stay smaller because fewer unrelated modules are involved.

---

# There Is No Perfect Structure

One important lesson from this exercise is that project organization is not about finding a universally correct folder layout.

Different teams may choose slightly different structures.

What matters is whether the structure helps developers answer questions such as:

- Where should this feature go?
- Which module owns this responsibility?
- What is allowed to depend on what?

If those answers are clear, the structure is doing its job.

---

# Key Takeaways

- Organize projects around business responsibilities rather than technical implementation details.
- Related code should live together because it usually changes together.
- Keep dependency directions simple and consistent.
- Avoid generic dumping-ground modules such as `utils.py` and `helpers.py`.
- Give each module a clear owner and a single reason to exist.
- A well-organized codebase improves discoverability, reduces coupling, and makes future changes easier.
