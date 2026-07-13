# Lecture Notes - Error Handling

# Overview

In this lesson, we explored error handling from a software design perspective. Rather than treating errors as something to deal with after writing the main logic, we looked at how failures influence the structure of a system.

Using the personal finance platform as our running example, we covered:

- Why failures are an architectural concern
- The fail-fast principle
- The dangers of silent failures
- Using exceptions effectively in Python
- Designing custom exception hierarchies
- Attaching structured data to exceptions
- Translating low-level failures into domain-level failures
- Result-style error handling and monadic approaches
- Choosing between exceptions and explicit return values

---

# Error Handling Shapes Architecture

Our finance platform imports transactions from multiple sources:

- CSV files
- Bank APIs
- Budgeting applications

Each of these integrations can fail in different ways:

- Malformed input
- Missing fields
- Invalid values
- Unsupported currencies
- Network failures
- Unavailable services

The important question is not whether failures happen—they always do.

The real design question is:

> **How should failures move through the system?**

Without a clear strategy, systems gradually accumulate:

- swallowed exceptions
- ambiguous `None` values
- invalid state
- low-level implementation details leaking into higher layers

Error handling therefore influences the overall architecture of the application.

---

# The Fail-Fast Principle

The core idea behind fail fast is simple:

> **Detect invalid assumptions as early as possible.**

Examples include:

- invalid transaction amounts
- malformed dates
- unsupported currencies
- missing required fields

Detecting these problems early prevents invalid state from spreading further through the system.

Fail fast **does not** mean crashing recklessly.

Instead, it means making problems visible immediately, close to where they occur.

Benefits include:

- easier debugging
- simpler reasoning
- improved domain integrity
- smaller impact of failures

---

# Silent Failures

One of the most dangerous forms of error handling is hiding failures.

Examples include:

- swallowing exceptions
- skipping invalid rows silently
- replacing invalid values with defaults
- returning empty results without explanation

Although the application appears to continue running, its data may no longer be trustworthy.

Silent failures can lead to:

- incorrect reports
- inaccurate budgets
- difficult debugging
- reduced confidence in the system

A visible failure is often preferable to incorrect results that nobody notices.

### AI Consideration

AI coding tools frequently generate broad exception handlers because they eliminate visible errors.

However, code that hides failures is usually less maintainable than code that reports them clearly.

---

# Exceptions in Python

Python is an exception-oriented language.

Most libraries and frameworks communicate failures by raising exceptions.

Exceptions work particularly well when:

- an operation cannot continue
- assumptions have been violated
- infrastructure has failed
- continuing would produce incorrect results

One of their biggest advantages is that they keep the success path clean while allowing failures to propagate automatically.

---

# Custom Exception Hierarchies

Generic exceptions such as:

- `ValueError`
- `KeyError`
- `RuntimeError`

describe technical problems rather than business problems.

Instead, systems benefit from domain-specific exceptions.

Example hierarchy:

- `FinanceError`
- `TransactionImportError`
- `InvalidTransactionError`
- `UnsupportedCurrencyError`
- `BankApiError`

These exceptions communicate the language of the finance platform instead of implementation details.

Benefits include:

- clearer intent
- cleaner architectural boundaries
- better separation between infrastructure and domain logic
- easier selective handling

---

# Exceptions Can Carry Data

Custom exceptions are useful for more than simply giving failures better names.

They can also carry structured information about the failure.

Examples include:

- source file
- line number
- invalid field
- invalid value
- transaction ID

Instead of forcing every layer to interpret a text message, higher-level components can inspect the exception directly.

For example, an application can log:

- which CSV file failed
- which row failed
- which value caused the problem

This also makes testing easier because tests can verify the structured data instead of parsing exception messages.

A useful rule:

> **The exception message is for people. The exception data is for the system.**

---

# Translating Failures at Boundaries

Different layers of the application have different responsibilities.

A CSV importer may encounter low-level failures such as:

- invalid decimal values
- malformed dates
- missing dictionary keys

Those implementation details should not leak into the rest of the application.

Instead, the importer translates them into domain-oriented exceptions such as:

- `InvalidTransactionError`
- `TransactionImportError`

Higher-level components only need to know that importing failed.

They do not need to understand how CSV parsing works.

A useful guideline is:

> **Raise failures close to the source. Handle them close to the boundary.**

This keeps responsibilities clearly separated.

---

# Result Types and Monadic Error Handling

Exceptions are not the only approach to error handling.

Some programming languages use explicit result types.

Examples include:

- `Result[Transaction, Error]`
- `Transaction | None`

Rather than throwing exceptions, functions return an object describing either:

- success
- failure

This makes possible failures visible in the function signature.

Advantages include:

- explicit control flow
- callers must consider failure
- useful for validation and parsing

Disadvantages include:

- more manual propagation
- additional boilerplate
- can reduce readability when overused

---

# Exceptions vs Explicit Return Values

In practice, Python often combines both approaches.

## Use exceptions when:

- assumptions have been violated
- infrastructure has failed
- the workflow cannot continue
- failures are unexpected

Examples:

- unreadable CSV files
- unavailable bank APIs
- invalid transaction data

## Use explicit return values when:

- absence is expected
- optional values are normal
- callers should decide what to do next

Example:

A budget lookup returning `Budget | None` is often clearer than raising an exception when no budget exists.

Different failure modes deserve different handling strategies.

---

# Key Takeaways

- Error handling is part of software design.
- Fail fast to prevent invalid state from spreading.
- Silent failures reduce trust in a system.
- Custom exception hierarchies improve communication between components.
- Exceptions can carry structured context in addition to error messages.
- Translate low-level implementation failures into domain-level failures.
- Result-style error handling provides an explicit alternative to exceptions.
- Choose the error handling strategy that best matches the type of failure.

The overall goal is simple:

> **Failures should either be handled intentionally or propagated clearly.**

---

# Bridge to the Next Lesson

As our finance platform grows, we've accumulated more than just business logic. We now have importers, synchronizers, domain models, exception types, and clear application boundaries.

The next challenge is no longer *what* the responsibilities are, but *where* they belong. In the next lesson, we'll look at how to organize modules and folders so these responsibilities remain easy to navigate as the system continues to evolve.