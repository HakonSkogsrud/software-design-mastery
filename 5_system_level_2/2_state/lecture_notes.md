# Lecture Notes - State Ownership

# Overview

In this lesson, we explored one of the most important ideas in software design: **state ownership**.

As applications grow, more parts of the system want to read and update the same information. Without clear ownership, state becomes duplicated, inconsistent, and increasingly difficult to reason about.

The key takeaway is simple:

> **Every piece of mutable state should have a clear owner.**

Along the way, we distinguished between **actual state** and **derived state**, discussed why **DRY applies to data as well as code**, and looked at how concepts like **projections**, **event sourcing**, and **CQRS** build on the same fundamental idea.

---

# From Cross-Cutting Concerns to State Ownership

In the previous lesson, we looked at ownership of cross-cutting concerns such as logging.

This lesson applies the same design question to data:

- Who owns the transaction history?
- Who owns account balances?
- Who owns spending summaries?
- Who is responsible for keeping them consistent?

Ownership is just as important for state as it is for behavior.

---

# The Temptation of Snapshots

As our finance platform grows, we naturally want to display information such as:

- current balance
- spending by category
- transaction count
- dashboard statistics

A common solution is to introduce a snapshot that stores these values directly.

At first, this seems efficient:

- reports become faster
- dashboards are simple to build
- notifications have easy access to summary information

Unfortunately, this also introduces a new problem.

---

# Duplicated Truth

The transaction history already contains:

- transaction amounts
- categories
- dates
- currencies

If we also store balances and totals separately, the same knowledge now exists in multiple places.

This is the real problem.

Many people think DRY only means avoiding duplicated code.

A more useful interpretation is:

> **Don't duplicate knowledge.**

If one fact is represented in multiple places, every update must keep those representations synchronized.

If one update path forgets, the system becomes inconsistent.

---

# A Realistic Failure

Imagine a second import path is added.

It successfully stores new transactions.

However, it forgets to update the dashboard snapshot.

Now:

- transactions are correct
- reports are incorrect
- dashboards show stale information
- notifications may trigger incorrectly

Nothing crashes.

The system simply becomes wrong.

These bugs are difficult because they often appear long after the code that caused them was written.

---

# Actual State vs Derived State

A useful distinction is between **actual state** and **derived state**.

## Actual state

Actual state represents facts that the system owns.

In our finance platform, examples include:

- imported transactions

These are the source of truth.

## Derived state

Derived state is calculated from the facts.

Examples include:

- account balance
- spending by category
- monthly totals
- budget usage
- reports

Whenever possible:

> **Store the facts. Derive the views.**

This reduces synchronization problems because there is only one authoritative representation of the data.

---

# Introducing a Transaction Store

Once we decide that transactions are the source of truth, they need a clear owner.

A transaction store becomes responsible for maintaining the transaction history.

Reports, analytics, and dashboards no longer own financial facts.

Instead, they derive information from the transaction store.

This improves:

- **Clarity** by making the source of truth obvious.
- **Resilience** by reducing duplicated state.
- **Separation** because reporting no longer mutates import state.

---

# When Derived State Should Be Stored

Recomputing everything is not always practical.

Large systems may contain:

- millions of transactions
- dashboards that refresh frequently
- expensive analytics
- continuous budget calculations

In these situations, storing derived state can improve performance.

Examples include:

- cached balances
- spending summaries
- dashboard projections
- reporting views

However, stored derived state introduces a new responsibility.

Someone must keep it synchronized.

---

# Projections

A useful way to think about stored derived state is as a **projection**.

A projection is **not** the source of truth.

Instead, it is a derived representation built from the transaction history.

Examples include:

- dashboards
- reporting summaries
- budget views
- analytics

One major advantage of projections is that they can be rebuilt from the underlying facts whenever necessary.

If a projection becomes corrupted, rebuilding it should restore consistency.

---

# Ownership

Ownership means that exactly one component is responsible for mutating a piece of shared state.

That owner is responsible for:

- updating the state
- enforcing consistency
- protecting invariants
- deciding what can be modified

Other components may read the state.

Ideally, they should not modify it directly.

This greatly reduces hidden coupling.

---

# Rust and Ownership

Rust enforces ownership through the language itself.

Its ownership and borrowing rules prevent many forms of shared mutable state from compiling.

Python gives us much more freedom.

That freedom also means more responsibility.

In Python, ownership is primarily expressed through design:

- encapsulation
- immutable data where practical
- controlled mutation
- clear APIs
- avoiding multiple writable paths

The language does not enforce these decisions for us.

---

# AI and State Ownership

AI-generated code often introduces additional state because it appears convenient.

Examples include:

- cached totals
- counters
- module-level dictionaries
- mutable summaries

These additions may improve local performance but also increase architectural complexity.

When reviewing AI-generated code, ask questions such as:

- Is this actual state or derived state?
- Is this duplicating knowledge?
- Can it be derived instead?
- Who owns updating it?
- How is it kept consistent?

Thinking in terms of ownership helps identify structural problems early.

---

# Event Sourcing

Event sourcing pushes this idea even further.

Instead of storing only the current state, it stores a history of events.

Current state is derived by replaying those events.

In our finance platform:

- transactions behave like events
- balances are derived
- reports are derived
- budget status is derived

This reinforces an important architectural principle:

> **Facts first. Views second.**

If necessary, the current view can always be rebuilt from the recorded facts.

A similar idea appears in blockchain systems, where an append-only history of transactions forms the basis for deriving the current state.

Although blockchain and event sourcing solve different problems, they both emphasize preserving historical facts.

---

# CQRS

The same thinking also appears in **CQRS (Command Query Responsibility Segregation)**.

CQRS separates:

- the model used to write data
- the model used to read data

In our finance platform:

- transactions form the write model
- reports and dashboards use projections built from those transactions

You do not need CQRS to benefit from these ideas, but it demonstrates how state ownership scales into larger architectures.

---

# Concurrency

Ownership becomes even more important when multiple operations execute simultaneously.

If several synchronization jobs update the same projection concurrently, problems such as:

- lost updates
- inconsistent totals
- stale summaries

become much more likely.

Clear ownership does not eliminate concurrency challenges.

However, it provides a single place where synchronization and coordination can be managed.

---

# Practical Guidelines

Prefer:

- storing facts rather than summaries
- deriving views whenever practical
- one owner for mutable shared state
- rebuilding derived state from the source of truth when needed

Be careful with:

- duplicated writable state
- global mutable data
- multiple sources of truth
- caches without clear ownership
- exposing mutable internal structures

A useful question to ask during design is:

> **If this value is wrong, where should I go to fix it?**

If the answer is "several places," the ownership is probably unclear.

---

# CARDS Connections

## Clarity

The source of truth is easy to identify.

## Alignment

Responsibilities point to the components that own them.

## Resilience

Changes remain localized because mutable state has one owner.

## Domain Integrity

Financial facts remain internally consistent.

## Separation

Importing, storing, projecting, and reporting remain separate concerns.

---

# Key Takeaways

- Shared mutable state becomes dangerous when it duplicates knowledge.
- DRY applies to knowledge, not just code.
- Transactions are the source of truth.
- Balances, reports, and summaries are derived state.
- Derived state may be stored for performance, but it needs a clear owner.
- Projections should be rebuildable from the underlying facts.
- Event sourcing and CQRS build on the same fundamental distinction between facts and views.
- Python does not enforce ownership, so good design must.

---

# Bridge to the Next Lesson

So far, we've focused on keeping state consistent.

But what happens when something goes wrong halfway through updating that state?

If an import fails after storing transactions but before updating a projection, how do we prevent inconsistencies?

In the next lesson, we'll explore **error handling**, and how errors should move through the system without corrupting the state we've worked so carefully to protect.