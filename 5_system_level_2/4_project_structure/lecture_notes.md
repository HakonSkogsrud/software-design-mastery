# Lecture Notes - Organizing Code into Modules and Folders

## Overview

As software grows, organizing code becomes a design problem rather than a housekeeping task. A good project structure makes it easier to understand the system, find the right place for new code, and keep changes localized. A poor structure does the opposite: responsibilities become blurred, coupling increases, and the codebase becomes harder to navigate.

In this lesson, you learned:

- Why project structure matters as applications grow
- How folders and modules communicate architectural boundaries
- Why to organize code by responsibility rather than technical type
- How module boundaries influence coupling
- When protocols can reduce coupling between parts of the system
- Common structural mistakes to avoid

---

# Why Structure Matters

When an application is small, a handful of files is often enough.

As our finance platform grows, however, it gains many new responsibilities:

- Transaction imports
- Spending reports
- Budget tracking
- Notifications
- Integrations

Without a clear structure:

- Files become larger.
- Responsibilities become mixed.
- Developers struggle to find where new code belongs.
- Understanding the system becomes increasingly difficult.

Project organization is therefore part of the software design.

---

# AI Amplifies Existing Structure

Modern AI coding assistants generate code based on the structure they see.

If the project has weak boundaries, AI may:

- Place new functionality in arbitrary modules
- Import unrelated parts of the system
- Increase coupling without realizing it

A well-organized codebase provides structural guardrails for both humans and AI.

Good architecture makes the correct location for new code the obvious one.

---

# Structure Reflects Architecture

Folders are more than containers for files.

They communicate:

- Ownership
- Responsibilities
- System boundaries
- Dependency direction

A good structure helps answer questions such as:

- Where should this new feature go?
- Which module owns this behavior?
- What should this module depend on?
- What should remain independent?

This directly supports the CARDS framework:

- **Clarity** — responsibilities are easier to understand.
- **Alignment** — dependencies point in sensible directions.
- **Separation** — concerns remain isolated.

---

# A Simple Project Structure

A practical starting point is:

```text
finance_app/
    src/
    tests/
    scripts/
    docs/
```

Each directory has a clear purpose.

### `src`

Contains the application code.

### `tests`

Contains automated tests that mirror the application structure.

### `scripts`

Contains operational tasks such as imports, migrations, or maintenance jobs.

### `docs`

Contains documentation, architecture notes, and design decisions.

The goal is simply to separate different kinds of work.

---

# Organizing Application Code

A common beginner approach is grouping code by technical type:

```text
models/
services/
repositories/
utils/
```

Although this looks organized, these folders do not represent business responsibilities.

Instead, related functionality becomes scattered across the project.

A better approach is grouping by responsibility:

```text
transactions/
reports/
budgets/
notifications/
infrastructure/
```

Now the project structure reflects the domain instead of the implementation.

Developers naturally think in features and workflows. The codebase should support that mental model.

---

# Organizing Code into Modules

Folders define the larger boundaries.

Modules define the structure inside those boundaries.

For example:

```text
transactions/
    models.py
    filters.py
    sample_data.py

reports/
    models.py
    spending.py
    presentation.py
```

The objective is **not** to create many tiny files.

Instead, place code together when it changes for the same reasons.

Examples:

- Transaction models belong together.
- Transaction filtering belongs together.
- Report calculations belong together.
- Report presentation belongs together.

Each module should have a clear responsibility.

---

# Watch Import Direction

One useful way to evaluate a design is by looking at imports.

For example:

```text
reports → transactions
```

This makes sense because reports depend on transaction data.

The reverse dependency:

```text
transactions → reports
```

would usually indicate a design problem.

Lower-level modules should generally not depend on higher-level application workflows.

Circular imports often signal that responsibilities have become mixed.

Simple dependency directions usually lead to simpler systems.

---

# Using Protocols to Reduce Coupling

Sometimes a module needs behavior without caring about the implementation.

For example, report generation needs transactions, but it should not care whether those transactions come from:

- CSV files
- Databases
- APIs
- Test fixtures

Instead of depending on a concrete importer, the code can depend on a small protocol describing the required capability.

This reduces coupling because high-level workflows depend on abstractions rather than implementations.

Introduce protocols only when they genuinely simplify dependencies.

---

# Avoid Dumping Grounds

Files such as:

- `utils.py`
- `helpers.py`
- `common.py`
- `misc.py`

often begin with good intentions.

Over time they become containers for unrelated functionality.

Eventually:

- Many modules depend on them.
- Responsibilities become unclear.
- Coupling quietly accumulates.

If you are unsure where something belongs, treat that uncertainty as design feedback.

Perhaps:

- the responsibility is unclear,
- the module is too broad,
- or a new module should exist.

---

# Naming Modules and Folders

Choose names that describe responsibilities.

Good examples:

- `transaction_imports`
- `budget_tracking`
- `report_generation`

Avoid vague names such as:

- `processing`
- `shared`
- `misc`
- `stuff`

Consistency is more important than perfection.

Developers should be able to predict where functionality belongs.

---

# Tests Should Mirror the Structure

Tests should follow the same organization as the application.

Example:

```text
src/
    reports/
        spending.py

tests/
    reports/
        test_spending.py
```

This makes navigation easier and reinforces ownership.

Tests are part of the architecture because they evolve alongside the production code.

---

# Scripts and Operational Code

Operational tasks are different from application logic.

Examples include:

- Importing historical data
- Running migrations
- Rebuilding caches
- One-off export jobs

These belong in a dedicated `scripts/` directory.

The dependency rule is simple:

- Scripts may call application code.
- Application code should not depend on scripts.

This keeps dependency direction clean and supports **Alignment**.

---

# Common Structural Mistakes

## Organizing Around Frameworks

Structures such as:

```text
controllers/
models/
views/
```

reflect implementation technology rather than the business domain.

Related functionality becomes scattered across multiple folders.

---

## Giant Modules

Files such as:

```text
finance_service.py
```

that contain reporting, imports, budgeting, notifications, and synchronization quickly become difficult to understand and maintain.

Large modules usually indicate missing boundaries.

---

## Overengineering Too Early

Avoid introducing many architectural layers before the system actually needs them.

Structure should evolve together with system complexity.

---

## Ignoring Boundaries

If every module depends on every other module, the system develops:

- Tangled imports
- Hidden coupling
- Fragile change propagation

Good boundaries prevent this from happening.

---

# Key Takeaways

- Folder structure communicates architecture.
- Organize code by responsibility rather than technical type.
- Modules should group code that changes together.
- Keep dependency directions simple.
- Use protocols when they reduce coupling.
- Avoid dumping-ground modules.
- Mirror the application structure in your tests.
- Keep operational scripts outside the application core.
- Good organization improves **Clarity**, **Alignment**, and **Separation**.

---

# Bridge to the Next Lesson

A well-organized codebase gives each part of the system a clear responsibility. The next challenge is protecting those responsibilities from infrastructure concerns such as databases, APIs, and external services.

In the next lesson, we'll explore **Ports & Adapters**, a design approach that keeps the application focused on business logic while allowing infrastructure to evolve independently.