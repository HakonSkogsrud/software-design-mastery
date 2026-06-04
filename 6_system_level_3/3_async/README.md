# Concurrency Lesson Examples v2

This bundle contains two runnable examples for the lesson **Concurrency and Keeping It Out of the Domain**.

## 1. bad_async_leak/main.py

Shows the design problem:

- application use cases depend directly on a concrete async database repository
- the core becomes async because infrastructure leaked inward
- pure calculation functions remain synchronous, because making them async would be artificial
- the pain is that callers such as CLI code now need event-loop plumbing because of an infrastructure choice

Run:

```bash
python bad_async_leak/main.py
```

## 2. good_ports_adapters/main.py

Shows two better integration styles:

1. **Async orchestration at the edge**
   - async bank client fetches transactions
   - async repository writes to the database
   - report generation still uses synchronous domain calculations after data is loaded

2. **Boundary adapter from async infrastructure to a synchronous application port**
   - the infrastructure repository still uses async database operations
   - the application core still depends on a synchronous `TransactionRepository` port
   - a boundary adapter bridges the two for synchronous entry points such as CLI or worker code

Run:

```bash
python good_ports_adapters/main.py
```

## Teaching point

Async infrastructure is fine. The design problem is when async infrastructure dictates the shape of the domain and application core.
