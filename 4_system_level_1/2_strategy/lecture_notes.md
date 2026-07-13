# Lecture Notes - Eliminating Conditional Explosion with Strategy

## Overview

In this lesson, you learned how growing conditional logic can slowly make otherwise straightforward code difficult to extend and maintain.

A few `if` statements are not inherently a problem. The real issue appears when one function becomes responsible for every variation in behavior. Each new feature requires editing that same function, making changes increasingly risky.

The solution is to identify the **variation axis** and move that behavior behind a stable boundary using the **Strategy pattern**. In Python, this can be implemented with either functions or objects. Both approaches separate *what changes* from *what stays the same*, making the system easier to extend.

This lesson primarily strengthens the **Resilience** and **Clarity** aspects of the CARDS framework.

---

# The Problem: Conditional Explosion

Software often evolves gradually.

A report generator might initially support only one reporting mode:

- all transactions

Soon, new requirements arrive:

- exclude refunds
- only large purchases
- transactions above a configurable threshold
- reports for a specific category

The easiest implementation is usually to add another branch:

```text
if ...
elif ...
elif ...
```

Over time, a single function accumulates more and more decisions.

This creates several problems:

- every new feature requires modifying existing code
- every modification risks breaking existing behavior
- the function becomes responsible for multiple concerns
- understanding the function becomes increasingly difficult

The issue is not the existence of conditionals.

The issue is that **all variation has become centralized in one place.**

---

# Identifying the Variation Axis

Instead of asking:

> "How many report types do we support?"

Ask:

> **"What is actually changing?"**

In this example, the reporting algorithm stays the same.

The changing part is **which transactions should be included**.

That filtering rule is the true variation axis.

Once you recognize this, the design becomes much simpler.

---

# Strategy Pattern

The Strategy pattern separates:

- stable behavior
- changing behavior

Instead of encoding every variation inside one function, the varying behavior is supplied from the outside.

Rather than this:

```text
generate_report(..., report_type="large_purchases")
```

we move toward:

```text
generate_report(..., strategy)
```

The report generator no longer decides *how* transactions should be selected.

It simply asks the supplied strategy.

This has an important consequence:

Adding a new reporting rule no longer requires modifying the report generator.

Instead, you create another strategy.

Changes become **additive instead of invasive**.

---

# Functional Strategy

Python makes Strategy particularly lightweight.

A strategy can simply be a function:

```python
Callable[[Transaction], bool]
```

Each function answers one question:

> Should this transaction be included?

Examples include:

- include everything
- exclude refunds
- large purchases only

The report generator simply applies whichever function it receives.

This is often the most Pythonic implementation because it is:

- concise
- explicit
- easy to test
- easy to compose

Use the functional approach when the behavior is:

- small
- stateless
- easy to express as a single function

---

# Class-Based Strategy

Sometimes a function is no longer enough.

A strategy may need:

- configuration
- internal state
- multiple methods
- additional responsibilities

In these situations, representing the strategy as an object can improve readability.

Instead of a function, each strategy becomes a small class with an `include()` method.

For example:

- `ExcludeRefunds`
- `LargePurchasesOnly`
- `CategoryOnly`

The report generator still depends only on the behavior, not on the concrete implementation.

The overall design remains exactly the same.

---

# Using Protocol

Instead of forcing inheritance, we define the expected interface using a `Protocol`.

```python
class TransactionFilter(Protocol):
    def include(self, transaction: Transaction) -> bool:
        ...
```

Any object that implements this method automatically satisfies the protocol.

No explicit inheritance is required.

This allows us to program against behavior rather than implementation.

This style is often more flexible than requiring every strategy to inherit from a common base class.

---

# Benefits of Strategy

Using Strategy provides several important design improvements.

## Resilience

The report generator becomes stable.

Adding a new reporting rule no longer requires modifying existing logic.

Small changes stay small.

---

## Clarity

Each reporting rule has its own name.

Instead of hiding behavior inside a long conditional chain, every variation has a dedicated place.

The intent becomes much easier to understand.

---

## Open/Closed Principle

The report generator is:

- open for extension
- closed for modification

New behavior is added by creating new strategies instead of editing stable code.

---

# Choosing Between Functions and Classes

There is no universal winner.

### Prefer functions when:

- the behavior is simple
- no state is required
- readability remains high

### Prefer classes when:

- behavior needs configuration
- state is stored
- the strategy becomes more complex
- the boundary should be more explicit

Both approaches implement exactly the same design idea.

---

# Avoid Over-Abstraction

Not every conditional deserves a strategy.

If there is only one implementation—or the variation is unlikely to grow—a simple conditional may be easier to understand.

Remember the principles:

- **KISS** — Keep It Simple, Stupid
- **YAGNI** — You Aren't Gonna Need It

Create strategies because variation actually exists, not because a pattern is available.

---

# AI Guardrail

AI coding tools frequently solve new requirements by adding another branch.

Typical warning signs include:

- growing `if` / `elif` chains
- mode parameters
- string-based switches
- multiple Boolean flags

When reviewing AI-generated code, ask:

- What is actually changing?
- Can that behavior become a strategy?
- Would adding the next feature require editing this function again?

If the answer is yes, the variation probably deserves its own boundary.

---

# Key Takeaways

- Conditionals are not inherently bad.
- Conditional explosion happens when one function accumulates too many variations.
- Identify the variation axis before choosing a design.
- Strategy injects behavior instead of encoding it in conditionals.
- Python supports Strategy naturally with both functions and objects.
- `Protocol` allows objects to satisfy an interface without inheritance.
- The result is code that is easier to extend while remaining easier to understand.

---

# Bridge to the Next Lesson

In this lesson, we used a `Protocol` to define the boundary between the report generator and its strategies.

But Python also offers another way to define interfaces: **Abstract Base Classes (ABCs)**.

Both approaches allow code to depend on abstractions rather than concrete implementations, but they make different trade-offs.

In the next lesson, we'll compare **Protocols and ABCs**, discuss when each is the better choice, and explore how structural typing can help you design more flexible Python applications.