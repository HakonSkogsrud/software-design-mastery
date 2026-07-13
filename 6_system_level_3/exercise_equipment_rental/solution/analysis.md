> Don't read any further until you tried coming up with a solution yourself!

# Solution & Analysis

## Overview

This exercise introduced one of the most important architectural ideas in modern application design: **keeping your application core independent from frameworks and infrastructure**.

The original implementation worked correctly, but the FastAPI endpoints had become responsible for almost everything:

- executing business logic
- interacting with SQLite
- sending notifications
- translating errors into HTTP responses

The refactored solution separates these concerns into distinct layers with clear dependency direction.

---

# Step 1 — Introduce a Domain Model

The first step was extracting an `Equipment` class.

Instead of passing around database rows or request objects, the application now works with a proper domain object.

```python
@dataclass(frozen=True)
class Equipment:
    ...
```

The domain model represents the concepts of the application—not the structure of a database or an HTTP request.

One small improvement is the `is_rented` property, which communicates intent more clearly than repeatedly checking whether `renter_email` is `None`.

---

# Step 2 — Move Business Logic into Use Cases

Originally, the endpoints implemented the workflows themselves.

For example, renting equipment involved:

- querying SQLite
- checking whether the equipment exists
- validating rental status
- updating the database
- sending a notification

All inside a single endpoint.

The solution extracts these workflows into application use cases.

```python
def rent_equipment(...):
    ...
```

This creates a clear separation between:

- **application logic**
- **HTTP handling**

The FastAPI layer no longer owns the business rules.

---

# Step 3 — Define the Ports

The application needs two external capabilities:

- storing equipment
- sending notifications

Rather than depending directly on SQLite or `print()`, the application defines two Protocols:

```python
class EquipmentRepository(Protocol):
    ...
```

and

```python
class RentalNotifier(Protocol):
    ...
```

These are called **ports**.

Notice an important detail:

The interfaces describe **what the application needs**, not **how the infrastructure works**.

Good examples:

- `add()`
- `get()`
- `update()`

Poor examples would have been:

- `execute_sql()`
- `save_to_sqlite()`
- `insert_row()`

The application should express its own language, not the database's.

---

# Step 4 — Introduce Adapters

The SQLite repository now implements the repository port.

Its responsibilities include:

- executing SQL
- opening database connections
- mapping rows to domain objects
- mapping domain objects back to SQL values

These responsibilities belong together because they are all infrastructure concerns.

Likewise, the console notifier becomes an adapter for the notification port.

If the application later needs to send emails or Slack messages, only this adapter changes.

The application core remains untouched.

---

# Step 5 — Keep FastAPI Thin

Perhaps the biggest improvement is the API layer.

Each endpoint now performs only four tasks:

1. Parse the incoming request.
2. Construct domain objects or primitive values.
3. Call a use case.
4. Translate application errors into HTTP responses.

Notice what disappeared from the endpoints:

- SQL
- business rules
- notification logic

The framework now acts purely as a delivery mechanism.

This is the essence of the Ports & Adapters architecture.

---

# Step 6 — Application Errors

The original implementation raised `HTTPException` directly from the business logic.

That tightly couples the application to FastAPI.

Instead, the solution introduces application-specific exceptions such as:

- `EquipmentAlreadyExistsError`
- `EquipmentNotFoundError`
- `EquipmentAlreadyRentedError`

These describe business situations rather than HTTP responses.

The API adapter decides how those situations should be presented to an HTTP client.

For example:

- `EquipmentNotFoundError` → HTTP 404
- `EquipmentAlreadyRentedError` → HTTP 409

A CLI adapter could instead print a friendly message.

The application itself never needs to know.

---

# Dependency Direction

The most important architectural change is the dependency direction.

Originally the structure looked roughly like this:

```text
FastAPI
   │
SQLite
   │
Business Logic
```

The framework effectively became the center of the application.

After the refactoring, the structure becomes:

```text
FastAPI Adapter
       │
       ▼
Application Use Cases
       │
       ▼
Repository Port
       ▲
       │
SQLite Adapter
```

The same idea applies to notifications.

The application defines the interfaces.

Infrastructure implements them.

This keeps the core stable while allowing infrastructure to evolve independently.

---

# Testing Benefits

The new design is significantly easier to test.

Previously, testing a use case required:

- FastAPI
- SQLite
- database setup

Now the application depends only on ports.

A test can provide:

- an in-memory repository
- a fake notifier

without changing any application logic.

This leads to:

- faster tests
- simpler tests
- fewer infrastructure dependencies

---

# CARDS Connections

This exercise reinforces several parts of the CARDS framework.

## Alignment

Dependencies point inward toward the application core.

The core no longer depends on FastAPI or SQLite.

---

## Separation

Business logic, HTTP handling, storage, and notifications each have clearly defined responsibilities.

---

## Resilience

Infrastructure can change independently from business logic.

Adding PostgreSQL, email notifications, or a CLI requires new adapters rather than changes to the application core.

---

# Possible Improvements

The solution intentionally keeps the architecture lightweight for teaching purposes.

In a larger application, you might also consider:

- grouping use cases into modules
- introducing additional repository methods for efficiency
- adding transaction management
- creating separate DTOs for API responses
- using dependency injection to construct adapters

These improvements build on the same architectural foundation without changing the dependency direction.

---

# Key Takeaways

The main lesson is not about Protocols or repositories.

It is about **ownership**.

The application should own:

- business rules
- workflows
- interfaces describing what it needs

Infrastructure should own:

- HTTP
- databases
- notifications
- external services

A useful mental model is:

> The application tells the outside world what it needs.

> The outside world adapts to the application.

That simple inversion of dependency direction makes applications easier to test, easier to maintain, and much more resilient to change.