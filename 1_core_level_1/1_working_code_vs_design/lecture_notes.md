# Lecture Notes - Why “Working Code” Is Not Good Design

## Overview

In this lesson, we introduce a fundamental idea that will guide the rest of the program:

> Correctness is not the same as good design.

Many systems start with code that works perfectly. The real challenge begins when requirements change.

By the end of this lesson, you should understand:

- Why working code is only the starting point
- What change amplification is
- Why maintainability is about safe change
- The five CARDS design forces
- Why software design matters even more in the age of AI-assisted development

---

# The Illusion of “It Works”

When developers are learning to program, success is often measured by a simple question:

> Does the code work?

If the program produces the correct result, the task feels complete.

Real software is different.

Requirements change.
Features are added.
Business rules evolve.

A system that works today may become difficult to modify tomorrow.

The real question becomes:

> How easy is it to change the system safely?

That question is the starting point of software design.

---

# Example: A Booking Function

The lesson introduced a simplified booking function from our hotel booking system.

The function:

- validates input
- checks room availability
- calculates pricing
- creates a booking
- updates room state
- sends notifications

Everything works correctly.

At first glance, the code appears reasonable.

However, working code can still contain structural weaknesses.

---

# Small Requirement, Bigger Change

A new business rule was introduced:

> Bookings of 3 nights or more get a 10% discount, but only for double rooms or suites. Confirmation messages should mention the discount when one was applied.

This sounds like a small change.

Yet implementing it required modifications in multiple places:

## Pricing Logic

The discount calculation became more complex.

The pricing logic now depends on:

- room type
- booking duration
- discount eligibility

---

## Booking Data

A new field was added:

```python
"discount_amount": discount_amount
```

The structure of the booking itself changed.

---

## Notification Behavior

Confirmation messages now depend on whether a discount was applied.

The notification logic had to change as well.

---

# Change Amplification

This is an example of **change amplification**.

## Definition

> Change amplification occurs when a small requirement change causes a large code change.

A single business rule affected:

- pricing
- stored booking data
- notification behavior

The problem is not that the code became incorrect.

The problem is that a small change did not stay local.

---

# Resilience

This introduces the first CARDS force.

## 🂽 Resilience

Resilience asks:

> When something changes, how much of the system must change with it?

### Strong Resilience

Small changes remain local.

You modify one part of the system and everything else remains untouched.

### Weak Resilience

Changes spread through multiple functions, modules, or services.

Future development becomes slower and riskier.

---

# Introducing CARDS

CARDS is the framework used throughout this program.

These are not rules.

They are design forces that help us reason about software structure.

---

## 🂡 Clarity

Can a developer quickly understand what a piece of code is responsible for?

Questions to ask:

- Does this function do one thing?
- Is its purpose obvious?
- Does the implementation match the name?

Good design makes code easier to understand.

---

## 🂱 Alignment

Do dependencies point in the right direction?

Questions to ask:

- Does important business logic depend on unstable details?
- Are core decisions protected from infrastructure concerns?

Good design keeps important parts of the system independent from volatile details.

---

## 🂽 Resilience

Does change stay local?

Questions to ask:

- How many places must change when requirements change?
- Do changes spread through the system?

Good design makes future changes safer.

---

## 🂾 Domain Integrity

Can the system represent impossible states?

Questions to ask:

- Can invalid bookings exist?
- Can the system enter states that should never happen?

Good design prevents invalid states from being created.

---

## 🂿 Separation

Are responsibilities isolated?

Questions to ask:

- Is pricing mixed with notifications?
- Is validation mixed with persistence?
- Are unrelated concerns tangled together?

Good design keeps concerns separate and composable.

---

# CARDS and Trade-Offs

Design decisions are rarely perfect.

Improving one force may create pressure on another.

## Example: Extracting Pricing Logic

Moving pricing calculations into a separate function improves:

- Clarity
- Separation

However, if pricing rules continue to grow, the pricing function itself may become difficult to maintain.

New design decisions will eventually be needed.

---

## Example: Room Availability

Using a simple availability flag:

```python
room["available"] = False
```

is very easy to understand.

This improves:

- Clarity

However, it does not model real-world booking dates very well.

A more realistic model would improve:

- Domain Integrity

but would also increase complexity.

---

Because of trade-offs:

> There is rarely a perfect design.

Throughout this program, every refactoring will strengthen one or more CARDS while helping us understand the trade-offs between them.

---

# AI Amplifies Weak Design

Modern software is no longer edited only by humans.

It is increasingly edited by:

- Copilot
- Claude
- Cursor
- ChatGPT
- other AI coding assistants

These tools are extremely useful.

However, they operate locally.

They see a small portion of the codebase and generate changes within that context.

Systems behave globally.

A local change can have system-wide consequences.

---

## Weak Resilience + AI

If a design is fragile:

- AI may duplicate logic
- AI may introduce inconsistent behavior
- AI may unintentionally spread changes

The result is more change amplification.

---

## Weak Alignment + AI

If dependency directions are already unclear:

- AI suggestions can slowly erode architecture
- Business logic can drift toward infrastructure concerns
- Architectural boundaries become less obvious over time

---

## Using CARDS as a Filter

Before accepting an AI-generated change, ask:

- Does this improve Clarity?
- Does it preserve Alignment?
- Does it strengthen Resilience?
- Does it protect Domain Integrity?
- Does it improve Separation?

CARDS helps evaluate code, regardless of whether it was written by a human or by AI.

---

# Key Takeaways

## Working Code Is Not Enough

Correctness is necessary, but it is not the goal of software design.

---

## Maintainability Means Ease of Safe Change

A maintainable system allows developers to modify behavior without fear.

---

## Change Amplification Is a Warning Sign

When small requirements cause widespread code changes, resilience is weak.

---

## CARDS Provides a Design Lens

CARDS gives us five forces for evaluating software structure:

- 🂡 Clarity
- 🂱 Alignment
- 🂽 Resilience
- 🂾 Domain Integrity
- 🂿 Separation

---

## AI Makes Design More Important

AI can generate code quickly.

Good design ensures those changes remain safe and aligned with the system.

---

# Bridge to the Next Lesson

Now that we have a vocabulary for discussing software design, the next step is learning how to recognize structural problems before they become expensive.

In the next lesson, we will start examining code through the lens of CARDS and learn how to spot early warning signs of weak design.