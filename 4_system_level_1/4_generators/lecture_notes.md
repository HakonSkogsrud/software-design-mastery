# Lecture Notes - Designing Streaming Workflows with Generators

## Overview

In the previous lesson, we introduced an abstract base class that unified the workflow for importing transactions from different file formats. The import process became easier to understand because the common workflow lived in one place while the subclasses handled the format-specific details.

In this lesson, we improve that design further.

The shared workflow still has one limitation: every importer loads all transactions into memory before the rest of the application can process them. As transaction histories grow, that becomes increasingly inefficient.

Rather than treating generators as simply another Python language feature, we'll use them as a software design tool. They allow us to process data incrementally, reduce coupling between components, and naturally build pipeline-style workflows.

By the end of this lesson, you should understand:

- why eager loading becomes a design problem
- how generators enable streaming workflows
- why interfaces should usually expose `Iterable`
- how streaming improves composability
- when streaming is—and isn't—the right design choice

---

# The Hidden Cost of Loading Everything

Our abstract base class defines a shared workflow:

1. Read rows from a file.
2. Parse those rows into `Transaction` objects.
3. Return all transactions.

This is a clean design, but it still processes data eagerly.

For a CSV importer, that means:

- reading every row into memory
- parsing every row into another collection
- only then returning the complete result

This works perfectly well for small files.

However, as users import years of transaction history, several problems begin to appear:

- higher memory usage
- longer delays before processing can begin
- unnecessary intermediate collections

The application has to wait until the entire import finishes before it can do anything useful.

---

# Streaming Instead of Loading Everything

Instead of returning all transactions at once, we can produce them one by one.

The workflow changes from:

> Read everything → Parse everything → Return everything

to:

> Read one row → Parse one transaction → Yield one transaction

The overall structure stays exactly the same.

Only the way data moves through the system changes.

This is the essence of a streaming workflow.

---

# How Generators Help

A generator function uses `yield` instead of `return`.

Each time a value is yielded:

- the caller receives one transaction
- the function pauses
- execution resumes when the next transaction is requested

This means processing can begin immediately instead of waiting for the full dataset.

Streaming provides several benefits:

- lower memory usage
- earlier processing
- better composability
- improved scalability for large datasets

---

# Designing the Interface

Although the implementation uses a generator internally, the public interface should usually expose an `Iterable`.

For example:

```python
def import_transactions(self) -> Iterable[Transaction]:
```

instead of:

```python
def import_transactions(self) -> Generator[Transaction, None, None]:
```

Why?

Because callers only need to iterate over transactions.

They do **not** rely on generator-specific methods such as:

- `send()`
- `throw()`
- `close()`

This follows one of the recurring ideas in software design:

> Depend on the capability you need, not on implementation details.

Using `Iterable` keeps the interface flexible while allowing the implementation to use generators internally.

---

# Simplifying the Abstract Base Class

The streaming version of the abstract base class actually becomes simpler.

Instead of:

- reading every row
- creating another list of parsed transactions

the workflow simply:

- iterates over rows
- parses each row
- yields each transaction

The previous helper method that converted a list of rows into a list of transactions is no longer necessary.

The loop itself expresses the workflow clearly.

---

# Updating the Importers

## CSV Importer

The CSV importer now processes the file incrementally.

Instead of returning `list(reader)`, it yields rows directly from the CSV reader.

This removes the intermediate collection entirely.

Only one row needs to exist in memory at a time.

---

## JSON Importer

The JSON importer is slightly different.

Using Python's built-in `json` module still loads the JSON document into memory before iterating over it.

That is perfectly acceptable.

The important point is that the importer still exposes the same iterable interface to the rest of the application.

Some implementations stream internally.

Others may not.

Consumers don't need to know the difference.

---

# Updating the Synchronization Workflow

Previously, the synchronizer expected a list.

That allowed it to call `len()` immediately.

Once the importer returns an `Iterable`, that assumption disappears.

Instead, the synchronizer processes transactions as they arrive while counting them during iteration.

Processing can now begin immediately without waiting for the complete import.

---

# Pipeline-Style Workflows

Once every stage accepts and returns an `Iterable`, small processing stages become easy to compose.

Examples include:

- filtering transactions
- validating transactions
- enriching transactions
- writing transactions to storage

Each stage:

- consumes an iterable
- performs one focused transformation
- produces another iterable

This naturally creates a lightweight processing pipeline.

Each component remains small, focused, and reusable.

---

# CARDS Connections

## Alignment

Consumers depend on `Iterable` instead of concrete collection types.

Dependencies point toward the smallest useful abstraction.

---

## Separation

Each component has a clear responsibility.

- Importers load data.
- Filters transform data.
- Synchronizers coordinate the workflow.
- Storage components persist data.

These responsibilities remain independent and easy to compose.

---

## Resilience

Streaming allows the application to handle larger datasets without redesigning the overall workflow.

As data grows, the same structure continues to work.

---

# Common Mistakes

## Converting Everything Back to a List

Avoid immediately doing this:

```python
transactions = list(importer.import_transactions())
```

Sometimes this is necessary—for example when sorting or iterating multiple times—but doing it by default removes the benefits of streaming.

Ask yourself:

> Do I actually need the entire collection at once?

---

## Streaming Everything

Not every workflow benefits from generators.

If the dataset is small and already in memory, a list is often simpler.

Streaming should solve an actual design problem, not become the default for every piece of code.

---

## Mixing Side Effects into Pipelines

Generator pipelines are easiest to understand when they behave like predictable transformations.

Avoid hiding unrelated work such as:

- database writes
- notifications
- excessive logging

inside transformation stages.

Keep side effects at clear boundaries.

---

# AI Guardrail

AI coding assistants frequently generate eager list-based solutions because they are simple and usually correct.

When reviewing AI-generated code, don't stop at correctness.

Also ask:

> Does this workflow really need the entire dataset in memory?

If not, consider whether a streaming workflow would produce a more scalable design.

---

# Key Takeaways

- Lists store complete collections.
- Generators produce values over time.
- Streaming allows processing to begin immediately.
- Interfaces should usually expose `Iterable`, not `Generator`.
- Streaming workflows naturally support composable pipelines.
- Good software design responds to the pressures your system is under rather than applying advanced language features everywhere.

---

# Bridge to the Next Lesson

Streaming improves **how data flows** through an application.

As systems continue to grow, another challenge appears.

Even when data is processed efficiently, components can still become tightly coupled through shared state, shared configuration, and shared infrastructure.

In the next lesson, we'll explore how hidden dependencies create global coupling—and how to structure applications so that small changes stay small.