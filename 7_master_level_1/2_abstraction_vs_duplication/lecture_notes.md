# Lecture Notes - Abstraction vs Duplication

# Overview

In this lesson, we explored one of the most common and misunderstood software design trade-offs: **Abstraction vs Duplication**.

Many developers are taught that duplication should always be removed. In practice, however, abstraction is not free. Every abstraction introduces a dependency, and every dependency introduces coupling.

The goal of software design is therefore **not to eliminate duplication**, but to make future changes easier and less risky.

By the end of this lesson, you should understand how to recognize stable abstractions, when duplication is the better choice, and how this trade-off appears both within code and across entire systems.

---

# Abstraction Is a Trade-Off

A common interpretation of the DRY principle is:

> Duplication is bad.

A more useful way to think about the trade-off is:

- **Duplication adds repeated code.**
- **Abstraction adds dependency.**

Neither is inherently better. The important question is whether the dependency introduced by an abstraction is worth its long-term cost.

---

# Duplicate Code vs Duplicate Knowledge

Not all duplication is equal.

Consider two pieces of pricing logic that both apply a discount for high-value transactions.

Both implement the same business rule:

- transactions above €10,000 receive a discount

Extracting this into a shared function such as `apply_high_value_discount()` makes sense because the abstraction represents a **shared business concept**, not merely similar-looking code.

A useful guideline is:

> Abstract shared knowledge, not shared syntax.

---

# Stable Concepts Make Good Abstractions

Good abstractions usually represent concepts that exist within the business domain.

Examples include:

- Money
- Exchange Rate
- Transaction Fee
- High-Value Discount

These concepts tend to remain stable over time.

By contrast, generic utilities such as:

- `process_transaction()`
- `generate_document()`

often combine multiple unrelated responsibilities simply because their implementations happen to look similar.

As requirements evolve, these abstractions typically accumulate parameters and special cases, making them harder to understand and maintain.

---

# Clarity Matters

Introducing an abstraction should improve the design—not simply reduce the number of lines of code.

Ask yourself:

- Does this abstraction reveal a meaningful business concept?
- Or does it hide important differences behind a generic interface?

A small abstraction that makes the domain clearer is often worthwhile.

A generic abstraction that obscures intent usually is not.

This directly supports the **Clarity** principle of CARDS.

---

# A Practical View of YAGNI

YAGNI ("You Aren't Gonna Need It") is often interpreted too strictly.

Instead of asking:

> Could this change someday?

Ask:

- How likely is this code to change?
- How expensive is it to prepare?
- Does the abstraction improve clarity or add complexity?

Preparing for likely future change is sensible.

Building elaborate abstractions for imagined requirements is not.

---

# AI and Duplication

Modern AI coding tools have changed the economics of software development.

Because generating code is inexpensive, AI often favors duplication over abstraction.

In many situations, this is actually the safer choice.

Rather than asking an AI assistant to "remove duplication," consider whether the duplicated code truly represents the same business knowledge.

Similarity alone is not enough to justify a shared abstraction.

---

# The Same Trade-Off Exists at the System Level

Abstraction versus duplication is not limited to functions and classes.

It also appears when designing larger systems.

Imagine two applications:

- Trading System
- Accounting System

Both define their own `Money` type.

One option is to extract a shared `finance_core` package containing:

- Money
- Currency
- Exchange Rate
- Tax Rules

This removes duplication, but it also introduces a shared dependency.

Before creating such a package, consider questions like:

- Who owns it?
- Can the applications evolve independently?
- Will changes require coordination between teams?

At the architectural level, abstractions often create organizational dependencies in addition to technical ones.

---

# Shared Abstractions Tend to Grow

One subtle but important observation is that shared abstractions naturally attract additional responsibilities.

Each new consumer often requests one additional feature.

Over time, the abstraction becomes increasingly difficult to evolve because it represents the combined requirements of many different users.

Duplicated code often remains small.

Shared abstractions frequently become larger and more complex.

This is one reason why internal platforms and shared libraries sometimes become bottlenecks.

---

# Strategic Duplication

Duplication is not always accidental.

Sometimes it is a deliberate design decision.

Duplicating a small amount of code can allow different applications or teams to evolve independently without introducing shared ownership or release coordination.

A useful way to think about the trade-off is:

- **Shared code optimizes for consistency and efficiency.**
- **Duplicated code optimizes for independence.**

Neither approach is universally correct.

The right choice depends on how the software is expected to evolve.

---

# Decision Framework

When you encounter duplication, ask yourself the following questions:

### Does this represent a real business concept?

Abstract stable domain concepts—not merely similar implementations.

### Will this abstraction remain stable while its consumers evolve?

If every new payment type requires modifying your shared `finance_core` package, the abstraction has become a bottleneck rather than a simplification.

### What dependency am I introducing?

Every abstraction creates a dependency.

At the code level, this may be a shared function or module.

At the system level, it may be a shared package, service, or team.

### What am I actually buying?

An abstraction should provide tangible value, such as:

- improved clarity
- consistent business rules
- easier maintenance

Reducing the number of lines of code is rarely sufficient justification on its own.

---

# Key Takeaways

- Abstraction is not a goal—it is a trade-off.
- Every abstraction introduces a dependency.
- Good abstractions represent stable business concepts.
- Similar-looking code is not enough to justify sharing.
- Duplicated code is often cheaper than the wrong abstraction.
- Shared code improves consistency.
- Duplication often preserves independence.
- Design for ease of future change rather than minimal code.

---

# Bridge to the Next Lesson

Once you've decided that an abstraction is worthwhile, another important question appears:

**How flexible should it be?**

Should every aspect of its behavior be configurable, or should it provide one clear, opinionated way of working?

In the next lesson, we'll explore this trade-off through **Configuration vs Convention**, and see why exposing too many configuration options can make an abstraction just as difficult to use as the duplication it replaced.