# Lecture Notes - Protocols and Abstract Base Classes

# Overview

In this lesson, we looked at two ways of introducing abstractions in Python:

- **Protocols**, which describe the capabilities that a consumer expects.
- **Abstract Base Classes (ABCs)**, which define a family of related implementations that share behavior.

The key idea is that these solve **different design problems**.

Use a **Protocol** when you want to reduce coupling between components. Use an **ABC** when multiple implementations genuinely share workflow or implementation.

Just as importantly, we saw that many parts of a system don't need either. Often, a concrete class—or even a simple function—is the best design.

---

# Why interfaces matter

As our finance platform grows, it needs to import transactions from multiple sources:

- CSV files
- Bank APIs
- Budgeting applications

The reporting and synchronization logic should work with all of these without caring about their implementation details.

The challenge is deciding how these components should agree on behavior.

Good abstractions make adding new integrations straightforward while keeping the rest of the system unchanged.

This primarily strengthens:

- **Alignment** — dependencies point toward behavior instead of concrete implementations.
- **Separation** — infrastructure stays isolated from application logic.
- **Resilience** — adding new integrations requires fewer changes.

---

# Start with concrete implementations

A common mistake is introducing interfaces before there is any variation.

Instead, begin with a concrete implementation.

Our first importer is simply a `CsvTransactionImporter`.

Because it owns:

- configuration (the file path),
- the import workflow,
- parsing logic,
- and metadata about the source,

a class is justified.

If all we had were a single operation with no related state, a function would likely be the better choice.

Abstractions should emerge from design pressure, not anticipation.

---

# When a Protocol becomes useful

As more transaction sources are added, the synchronization code starts depending on concrete importer classes.

This creates unnecessary coupling.

The synchronization logic does not actually care whether transactions come from:

- a CSV file,
- a bank API,
- or somewhere else.

It only needs something that can:

- import transactions,
- identify its source,
- and report whether incremental synchronization is supported.

A **Protocol** captures exactly those capabilities.

The important observation is that implementations do **not** inherit from the protocol.

Instead, Python uses **structural typing**.

If an object provides the required behavior, it satisfies the protocol automatically.

---

# Protocols belong to the consumer

One of the most important ideas from this lesson is where a protocol should live.

A protocol should be designed from the perspective of the code that **uses** the dependency.

For example, the synchronization logic requires:

- `import_transactions()`
- `supports_incremental_sync()`
- `source_name()`

Those methods belong in the protocol.

CSV-specific implementation details, such as reading rows from a file, do **not** belong there.

The protocol should describe the public capability—not how one implementation happens to work internally.

This improves both **Alignment** and **Separation**.

---

# Testing becomes easier

Protocols make test doubles extremely lightweight.

Instead of inheriting from a base class or configuring a mocking framework, a simple object that implements the required methods is enough.

For example, a `FakeImporter` can provide predictable transaction data for tests while satisfying the same protocol as the real importers.

This keeps tests simple and avoids unnecessary infrastructure.

---

# When a Protocol is not enough

Protocols describe capabilities.

Sometimes that is exactly what we need.

But sometimes multiple implementations also share significant behavior.

In the lesson, we stayed with the importer example.

We introduced multiple **file-based importers**:

- a CSV importer
- a budgeting application JSON importer

Although the file formats differ, they both follow the same overall process:

1. Read raw data from a file.
2. Convert each raw record into a `Transaction`.
3. Return the resulting list.

When multiple implementations repeat this workflow, an abstract base class becomes useful.

---

# Using an Abstract Base Class

The `FileTransactionImporter` abstract base class provides the common import workflow.

It handles the parts that every file importer performs:

- coordinating the import process,
- parsing all records,
- providing default behavior where appropriate.

Each subclass only implements the parts that genuinely differ:

- how the file is read,
- how a single raw record is converted into a `Transaction`,
- the name of the source.

This is a classic example of the **Template Method** pattern:

The base class defines the overall algorithm while subclasses customize specific steps.

Inheritance now provides real value because it eliminates duplicated workflow while keeping format-specific behavior separate.

---

# Protocols vs Abstract Base Classes

These two abstractions serve different purposes.

## Use a Protocol when:

- consumers define the required behavior;
- implementations are unrelated;
- flexibility is important;
- there is little or no shared implementation.

Examples include:

- transaction importers,
- repositories,
- notification senders,
- adapters.

Protocols answer the question:

> **"What capabilities does this object provide?"**

---

## Use an Abstract Base Class when:

- implementations form a real family;
- they share workflow or implementation;
- the base class provides meaningful behavior.

Examples include:

- file-based transaction importers,
- parsers,
- framework extension points.

ABCs answer the question:

> **"What workflow do all members of this family share?"**

---

# When neither is necessary

Not every piece of code needs an abstraction.

Simple calculations often work best as functions.

For example, a function that calculates total spending:

- has no shared state,
- does not represent a reusable component,
- has no meaningful hierarchy.

Turning it into a protocol or an abstract base class would only add unnecessary complexity.

Choosing **not** to abstract is often the best design decision.

---

# Common mistakes

## Abstracting too early

Do not create an interface simply because you have one implementation.

Wait until genuine variation appears.

---

## Designing protocols from implementations

A protocol should expose only the behavior consumers need.

Implementation-specific methods should remain private to concrete classes.

---

## Using an ABC when a Protocol is enough

If implementations do not share workflow or implementation, inheritance only increases coupling.

A protocol is often the simpler and more flexible choice.

---

## Forcing unrelated classes into one hierarchy

Only classes that genuinely belong together should inherit from the same abstract base class.

For example:

- CSV and JSON file importers share a workflow.
- A bank API importer does not.

Placing them all under one base class creates a misleading hierarchy.

---

# AI and abstractions

AI coding assistants frequently generate abstract base classes because inheritance is a common pattern in training data.

Before accepting generated abstractions, ask yourself:

- Does this base class actually share behavior?
- Is there a common workflow?
- Or do consumers simply need a capability?

If the answer is "capability," a protocol is usually the better fit.

AI can generate syntactically correct abstractions.

It is still your responsibility to decide whether those abstractions improve the design.

---

# Key takeaways

- Start with concrete implementations.
- Let abstractions emerge from design pressure.
- Use **Protocols** to describe capabilities required by consumers.
- Use **Abstract Base Classes** to share workflow and implementation.
- Keep protocols focused on public behavior.
- Keep inheritance hierarchies honest.
- Many problems still only require a function or a concrete class.

Choose the least restrictive abstraction that protects the design.

---

# Bridge to the next lesson

So far, every importer has returned a complete list of transactions.

That works well for small datasets.

As the amount of data grows, loading everything into memory becomes inefficient.

In the next lesson, we'll explore **generators** and streaming workflows. You'll learn how to process transactions one at a time as they flow through the system, and how that changes the abstractions we build around them.