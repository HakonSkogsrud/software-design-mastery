# Lecture Notes - Principles as Force Balancing

## Overview

In previous lessons, we focused on identifying structural problems in software:

- Large functions
- Mixed responsibilities
- Hidden dependencies
- Growing complexity

In this lesson, we shift our focus slightly.

Many developers learn design principles such as KISS, DRY, YAGNI, and SOLID as rules to follow. Experienced designers eventually realize that these principles are better viewed as tools for balancing competing forces.

Using the CARDS framework, we can understand what these principles are actually protecting:

- **Clarity** — code communicates intent clearly
- **Alignment** — dependencies point in the right direction
- **Resilience** — small changes stay small
- **Domain Integrity** — invalid states are prevented by design
- **Separation** — concerns remain isolated and composable

The goal of software design is not to maximize a single force. The goal is to balance them.

---

## KISS: Simplicity Protects Clarity

KISS stands for:

> Keep It Simple, Stupid

The principle is often misunderstood as "write less code."

In reality, KISS is about reducing unnecessary complexity so that intent remains obvious.

Consider the booking system's `book_room()` function.

Initially, it handled:

- Validation
- Availability checks
- Pricing calculations
- Booking creation
- Notification logic

Even though the code worked, it became difficult to understand what the function was actually responsible for.

A small refactor extracted pricing logic into a separate function.

Benefits:

- The booking workflow becomes easier to read.
- Pricing rules become easier to locate.
- Each function has a clearer purpose.

This improves:

- **Clarity**
- **Resilience**

Notice that we did not introduce additional abstractions. We simply reduced complexity.

That is KISS in practice.

---

## DRY: Reducing Change Amplification

DRY stands for:

> Don't Repeat Yourself

The key idea is that duplicated knowledge creates maintenance risk.

In the booking system, pricing logic appeared in multiple places:

- Booking creation
- Room upgrades

If pricing rules change, every copy must be updated.

This weakens **Resilience** because a single business change can require modifications throughout the system.

Extracting pricing logic into a shared function solves this problem.

Benefits:

- Pricing rules live in one place.
- Changes become safer.
- The system becomes easier to evolve.

### The DRY Trade-Off

DRY is frequently over-applied.

Many developers interpret DRY as:

> Any duplication is bad.

This often leads to abstractions that are harder to understand than the duplicated code itself.

Examples include creating:

- Factories
- Managers
- Strategy hierarchies
- Policy engines

before the system actually needs them.

The goal is not to eliminate every repeated line.

The goal is to eliminate duplicated knowledge that would otherwise create maintenance problems.

This is where the tension between CARDS forces appears:

- DRY often strengthens **Resilience**
- Overusing DRY often weakens **Clarity**

Good design balances both.

---

## YAGNI: Avoid Designing for Imaginary Requirements

YAGNI stands for:

> You Aren't Gonna Need It

A common mistake is building flexibility for requirements that do not yet exist.

Imagine the booking system currently supports exactly one discount rule:

- Stay at least three nights
- Receive a 10% discount

A developer might decide to prepare for future growth by introducing:

- Pricing strategies
- Discount policies
- Rule engines

While these abstractions may eventually become useful, they provide little value today.

Instead, they:

- Increase complexity
- Introduce additional concepts
- Make the system harder to understand

This weakens:

- **Clarity**
- **Resilience**

Ironically, excessive flexibility often makes systems harder to change.

YAGNI reminds us to respond to actual design pressure, not hypothetical future requirements.

---

## Viewing SOLID Through CARDS

SOLID is often taught as a collection of independent principles.

A useful perspective is to view SOLID as reinforcing different CARDS forces.

| SOLID Principle | Primary CARDS Force |
|---------------|--------------------|
| SRP | Clarity |
| OCP | Resilience |
| LSP | Alignment |
| ISP | Clarity |
| DIP | Alignment |

For example:

### SRP (Single Responsibility Principle)

Separating pricing from booking logic improves:

- Clarity

### OCP (Open-Closed Principle)

Designing systems that can accept new behavior without modifying existing code improves:

- Resilience

### DIP (Dependency Inversion Principle)

Depending on abstractions rather than implementation details improves:

- Alignment

The important lesson is not memorizing SOLID definitions.

The important lesson is understanding which design force a principle is trying to strengthen.

---

## Principles Are Not Rules

The central idea of this lesson is simple:

Design principles are not rules.

They are tools.

Each principle helps strengthen one or more CARDS forces.

At the same time, every design decision introduces trade-offs.

Examples:

| Principle | Strengthens | Risk When Overused |
|------------|-------------|--------------------|
| KISS | Clarity | Under-design |
| DRY | Resilience | Loss of Clarity |
| YAGNI | Clarity, Resilience | Short-term thinking |
| SOLID | Depends on principle | Excessive abstraction |

Good software design requires balancing these forces intentionally.

There is rarely a perfect answer.

There are only trade-offs.

---

## AI and Design Principles

AI coding tools are very effective at producing working code.

However, they frequently optimize for local correctness rather than long-term structure.

Common AI-generated problems include:

- Duplicated business rules
- Additional flag arguments
- Large functions that keep growing
- Premature abstractions

The code may work perfectly while slowly weakening the design.

This is why architectural thinking remains important.

A clear design acts as a guardrail:

- For humans
- For AI tools
- For future changes

As AI accelerates code generation, understanding structural forces becomes even more valuable.

---

## Recap

In this lesson we learned that:

- KISS protects Clarity by reducing unnecessary complexity.
- DRY protects Resilience by reducing duplicated knowledge.
- YAGNI protects Clarity and Resilience by avoiding speculative design.
- SOLID principles can be understood through the CARDS framework.
- Every principle involves trade-offs.
- Good design is about balancing forces, not following rules.

The goal is not to memorize principles.

The goal is to understand what each principle is trying to protect and when applying it improves the design.

---

## Bridge to the Next Lesson

In this lesson, we explored trade-offs at the level of functions and small refactorings.

Next, we'll look at a deeper structural problem: coupling.

We'll examine how dependencies form between parts of a system, how hidden coupling creates change amplification, and how understanding dependency relationships helps us build software that remains stable as it grows.