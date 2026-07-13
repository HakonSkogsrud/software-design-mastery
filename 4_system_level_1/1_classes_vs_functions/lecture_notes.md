# Lecture Notes - When to Use a Class vs When to Use a Function

## Overview

In this lesson, you'll learn how to choose between two of Python's most fundamental building blocks: **functions** and **classes**. Rather than following object-oriented or functional programming dogma, the goal is to select the simplest abstraction that matches the problem you're solving.

We'll explore:

- Why stateless behavior is often best expressed as functions
- When classes provide genuine value by owning state
- How unnecessary classes increase complexity
- When functions become awkward due to shared context
- How closures and partial application provide a lightweight alternative
- Practical heuristics for deciding which abstraction to use

Throughout the lesson, we'll use a personal finance application that evolves from generating reports to tracking budgets and converting currencies.

---

# Functions First

A good default is to start with a function.

Example:

```python
def calculate_total_spending(
    transactions: list[Transaction],
) -> Decimal:
    ...
```

This function has several desirable properties:

- Stateless
- Deterministic
- No hidden side effects
- Easy to test
- Easy to reuse

All of its behavior is determined by its inputs, making it straightforward to understand.

### Design Insight

If behavior depends **only on its inputs**, a function is usually the best choice.

This supports the CARDS principle of **Clarity** because all information needed to understand the behavior is explicit.

---

# Functions Model Transformations

Many operations in the finance application simply transform data.

Examples include:

- Filtering transactions by month
- Calculating totals
- Grouping spending by category
- Generating reports

Each operation:

- accepts input
- performs one transformation
- returns a result

There is:

- no identity
- no lifecycle
- no mutable state

These are ideal candidates for functions.

---

# Avoid Unnecessary Classes

A common anti-pattern is wrapping stateless behavior inside a class.

Example:

```python
class SpendingCalculator:
    def calculate_total(...):
        ...
```

Ask yourself:

- Does this object own state?
- Does it have an identity?
- Does it protect invariants?
- Does it have a meaningful lifecycle?

If the answer is "no," then the class is probably unnecessary.

Using a class here simply increases cognitive overhead without providing structural value.

### Design Insight

Don't introduce complexity in anticipation of future requirements.

Add structure only when the problem demands it.

---

# Classes Are Not Just Namespaces

Another common pattern is creating utility containers such as:

```python
class FinanceUtils:
    ...
```

or a large:

```text
utils.py
```

These organize code by convenience rather than by meaningful concepts.

Good abstractions represent things like:

- ownership
- policies
- domain concepts
- responsibilities
- architectural boundaries

Not arbitrary collections of helper methods.

This supports **Alignment** by encouraging dependencies to point toward meaningful concepts.

---

# Functions Compose Naturally

One advantage of functions is that they compose well.

Example workflow:

```text
Load transactions
        ↓
Filter by month
        ↓
Generate report
        ↓
Print report
```

Each step:

- performs one task
- is independently testable
- can be reused elsewhere

This pipeline style improves:

- readability
- composability
- local reasoning

It also reinforces **Separation** within CARDS.

---

# Small Functions Encourage Reuse

The lesson demonstrates extracting even small pieces of behavior into focused functions.

Instead of embedding every calculation inside one larger function, individual behaviors can become independently reusable.

This is not about creating many tiny functions for their own sake.

The goal is making useful behaviors available for future composition.

---

# When Classes Become Useful

The finance application evolves.

Instead of generating reports once, it now tracks spending over time.

A `BudgetTracker` object is introduced.

Responsibilities include:

- storing running totals
- adding transactions
- checking category totals
- enforcing spending limits

Unlike the earlier examples, this object owns **mutable state**.

This is where a class provides genuine value.

### Classes Become Appropriate When They:

- own data that changes over time
- coordinate related behavior
- manage lifecycle
- protect invariants

This is much more than simply grouping methods together.

---

# Encapsulation Protects Invariants

Imagine external code modifying the internal totals directly.

```python
tracker.monthly_totals["Food"] = Decimal("-999999")
```

The object can no longer guarantee that its state is valid.

Encapsulation is not about hiding implementation details.

It is about ensuring the object remains internally consistent.

This strengthens **Resilience**, because changes remain localized inside the class.

---

# When Functions Become Awkward

Later, the system introduces multiple currencies.

The conversion function looks like:

```python
convert_currency(
    amount,
    source_currency,
    rates,
    target_currency,
)
```

Soon every call repeats the same configuration:

- exchange rates
- target currency

Repeated shared context is often a design signal.

Symptoms include:

- repeated parameters
- duplicated configuration
- growing parameter lists

This doesn't necessarily justify introducing a class.

But it does indicate that another abstraction may help.

---

# A Lightweight Alternative: Partial Application

Python offers an elegant middle ground.

Using `functools.partial`, shared configuration can be captured once.

Instead of repeatedly writing:

```python
convert_currency(
    amount,
    source_currency,
    rates,
    "EUR",
)
```

we create:

```python
eur_converter = partial(
    convert_currency,
    rates=rates,
    target_currency="EUR",
)
```

Calls become much simpler:

```python
eur_converter(amount, "USD")
```

The important insight is **not** learning `partial`.

The important insight is recognizing that **shared configuration does not automatically require a class**.

---

# Another Alternative: Closures

Closures provide another lightweight option.

A factory function can return a configured conversion function.

The returned function "remembers" the exchange rates and target currency.

Again:

- no mutable state
- no lifecycle
- no unnecessary object

Closures and partial application are valuable tools in modern Python because they allow behavior and configuration to stay together without introducing additional classes.

---

# When a Class Finally Makes Sense

Requirements continue to evolve.

The currency converter now needs:

- cached exchange rates
- automatic refresh
- retry logic
- external API communication

Now the object has:

- internal state
- dependencies
- lifecycle
- responsibilities that persist over time

A `CurrencyConverter` class now becomes a natural abstraction.

The class has earned its complexity.

---

# Decision Framework

## Prefer Functions When

- Behavior is stateless
- Logic performs a transformation
- Inputs and outputs are explicit
- Composition is important
- Behavior should remain lightweight

---

## Prefer Classes When

- State persists over time
- Lifecycle matters
- Internal invariants must be protected
- Related dependencies belong together
- Behavior depends on evolving internal data

---

# Common Mistakes

## Everything Is a Class

Symptoms include:

- unnecessary boilerplate
- wrapper classes
- artificial object hierarchies

---

## Functions Only

This can lead to:

- long parameter lists
- duplicated configuration
- unclear ownership
- scattered state

---

## Premature Abstraction

Designing for hypothetical future requirements often creates rigid software.

Instead:

- solve today's problem well
- allow the design to evolve naturally
- introduce complexity only when structural pressure appears

---

# AI Guardrail

AI coding assistants frequently generate unnecessary classes.

For example, asking an AI to "add filtering logic" may produce:

```python
class TransactionFilteringManager:
    ...
```

Before accepting generated code, ask:

- What state does this object own?
- What lifecycle does it manage?
- Which invariant does it protect?

If the answer is "none," a function is probably the better choice.

AI is excellent at generating code.

It still relies on you to make sound structural decisions.

---

# Key Takeaways

- Functions excel at transforming data.
- Classes excel at managing evolving state.
- Avoid introducing state unless the problem requires it.
- Shared configuration is often a design signal, but not necessarily a reason to create a class.
- Closures and partial application provide lightweight alternatives.
- Good design is incremental.
- Choose the simplest abstraction that matches the problem.

---

# Bridge to the Next Lesson

In this lesson, we focused on choosing the right abstraction for behavior and state.

In the next lesson, we'll take the next step by looking at **behavior injection**. Rather than hardcoding decisions inside classes, you'll learn how functions themselves can become configurable pieces of behavior, allowing systems to evolve safely without introducing unnecessary inheritance or class hierarchies.