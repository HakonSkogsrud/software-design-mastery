> Don't read any further until you tried coming up with a solution yourself!

# Solution & Analysis

## Overview

The original implementation works, but it mixes two different concerns inside the same use case:

1. Coordinating asynchronous infrastructure
2. Processing a sensor reading according to business rules

The refactoring separates these responsibilities.

The MQTT client and database implementation remain asynchronous because they perform I/O. The `process_reading` use case becomes synchronous because its responsibility is to apply business behavior to a reading and store the result through a synchronous application port.

The core design principle is:

> Async execution belongs at the system boundary. Business logic should not become async merely because infrastructure is async.

---

## The problem in the original design

The original use case looks roughly like this:

```python
async def process_next_reading(
    sensor_client: AsyncSensorClient,
    repository: AsyncReadingRepository,
) -> None:
    reading = await sensor_client.receive_reading()

    if reading.temperature < -20 or reading.temperature > 50:
        reading.mark_as_anomalous()

    await repository.save(reading)
```

At first, this may seem reasonable. The sensor client and repository are asynchronous, so the function awaits both operations.

The problem is not that the anomaly rule itself is asynchronous. It is not.

The problem is that the use case combines:

- receiving a reading from MQTT
- evaluating a business rule
- modifying the domain object
- storing the result
- coordinating asynchronous execution

Because these concerns are combined, the use case becomes shaped by the infrastructure.

Any caller of `process_next_reading` must now:

- run inside an event loop
- provide an async MQTT client
- provide an async repository
- understand the asynchronous execution model

The application operation is therefore difficult to reuse independently of the infrastructure.

---

## Why `process_reading` no longer receives the sensor client

The refactored use case receives a `SensorReading` instead of a sensor client:

```python
def process_reading(
    reading: SensorReading,
    repository: ReadingRepository,
) -> None:
    ...
```

This is an important design change.

The responsibility of `process_reading` is to **process a reading**. It should not also be responsible for obtaining that reading.

Receiving data from an MQTT client is an infrastructure operation. Processing the received data is an application operation.

These are separate steps:

1. Infrastructure receives a reading.
2. The application processes the reading.
3. Infrastructure stores the result.

By passing the reading directly into the use case, the use case no longer knows:

- that MQTT is being used
- that receiving data requires `await`
- whether the reading came from a network connection
- whether the caller is a CLI, API endpoint, background worker, or test

The use case now operates on a domain concept rather than an infrastructure service.

That makes its interface more precise:

> `process_reading` processes a reading.

The old name, `process_next_reading`, implied orchestration. It had to find the next reading before it could process it. The new function receives everything it needs to perform its actual business responsibility.

---

## Moving orchestration to the edge

The asynchronous work moves to the entry point:

```python
reading = asyncio.run(sensor_client.receive_reading())
process_reading(reading, repository)
```

This entry point coordinates the workflow:

1. Receive a reading asynchronously.
2. Pass the resulting domain object into the synchronous use case.
3. Let the use case apply the business rule and save the reading.

The entry point is allowed to know about async execution because it sits at the edge of the application.

This creates a clear distinction:

- **Orchestration** decides when and how operations run.
- **Application logic** decides what should happen to a reading.

The orchestration code owns the event loop. The use case does not.

---

## Introducing a synchronous repository port

The original repository port was asynchronous:

```python
class AsyncReadingRepository(Protocol):
    async def save(self, reading: SensorReading) -> None: ...
```

That design describes the mechanics of a particular adapter.

The improved application port is synchronous:

```python
class ReadingRepository(Protocol):
    def save(self, reading: SensorReading) -> None: ...
```

This port describes what the use case needs:

> The use case needs somewhere to save a reading.

It does not prescribe whether the underlying implementation uses:

- an in-memory list
- a file
- a synchronous database driver
- an asynchronous database driver
- an external storage service

That is an infrastructure decision.

The port belongs to the application, so it should be shaped around the needs of the application rather than around one particular adapter.

---

## Adapting async infrastructure

The asynchronous database implementation remains asynchronous:

```python
class AsyncReadingDatabase:
    async def save(self, reading: SensorReading) -> None:
        ...
```

A synchronous repository adapter exposes the interface expected by the application:

```python
class SyncReadingRepository:
    def save(self, reading: SensorReading) -> None:
        asyncio.run(self._database.save(reading))
```

The adapter translates between two execution models:

- the synchronous interface expected by the application
- the asynchronous interface provided by the infrastructure

This preserves the dependency direction:

> The infrastructure adapts to the application.  
> The application does not adapt to the infrastructure.

This is the central Ports & Adapters improvement in the solution.

### A practical limitation

Calling `asyncio.run()` is suitable for illustrating the boundary, but it has an important limitation: it cannot be called while another event loop is already running.

In a production application, alternatives may include:

- using a synchronous database driver
- running synchronous application work in a worker thread
- moving persistence into an async orchestration layer
- introducing a dedicated bridge between sync and async execution

The exact mechanism depends on the runtime environment. The architectural lesson remains the same: the infrastructure mechanism should not casually define the application interface.

---

## Keeping the domain behavior with the model

The `SensorReading` model now owns the transition to an anomalous state:

```python
@dataclass
class SensorReading:
    ...
    is_anomalous: bool = False

    def mark_as_anomalous(self) -> None:
        self.is_anomalous = True
```

This is clearer than a standalone helper because marking a reading as anomalous is behavior performed on that reading.

The use case decides **when** the state transition should happen:

```python
if (
    reading.temperature < MIN_TEMPERATURE
    or reading.temperature > MAX_TEMPERATURE
):
    reading.mark_as_anomalous()
```

The model controls **how** its state changes.

This creates a useful division of responsibility:

- the use case applies the larger business workflow
- the domain object owns its own state transition

For this exercise, the object is mutable to keep the example focused. An immutable model could return a new instance instead, but that would introduce another design topic without improving the concurrency lesson.

---

## The responsibility of the use case

The final use case has three focused responsibilities:

1. Determine whether the temperature is outside the allowed range.
2. Mark the reading as anomalous when necessary.
3. Save the processed reading through the repository port.

```python
def process_reading(
    reading: SensorReading,
    repository: ReadingRepository,
) -> None:
    if (
        reading.temperature < MIN_TEMPERATURE
        or reading.temperature > MAX_TEMPERATURE
    ):
        reading.mark_as_anomalous()

    repository.save(reading)
```

It does not:

- receive MQTT messages
- manage an event loop
- await database operations
- know which database implementation is used
- coordinate multiple infrastructure systems

This makes the function easier to read and test.

---

## Testing becomes simpler

The original async use case required async test infrastructure.

A test had to provide:

- an async sensor client
- an async repository
- an event loop
- potentially simulated I/O behavior

The refactored use case only requires:

- a `SensorReading`
- a simple repository test double

A test can call the function directly:

```python
repository = FakeReadingRepository()
reading = SensorReading(
    sensor_id="sensor-001",
    temperature=58.0,
    humidity=32.0,
    recorded_at=datetime.now(),
)

process_reading(reading, repository)

assert reading.is_anomalous
assert repository.saved_readings == [reading]
```

The test focuses on the business behavior rather than on asynchronous plumbing.

Tests for the MQTT adapter and async database can still be asynchronous, but those are adapter tests. The core application tests remain straightforward.

---

## What remains asynchronous

The solution does not remove async from the system.

Async remains appropriate for:

- receiving messages from the MQTT client
- communicating with the database implementation
- coordinating infrastructure operations

The important improvement is that async no longer spreads into the use case.

The system now has:

- async infrastructure at the edges
- a synchronous application port
- synchronous business logic in the center

---

## CARDS analysis

### Clarity

`process_reading` now describes exactly what it does.

It accepts a reading, applies the anomaly rule, and saves the result. MQTT and event-loop details no longer obscure the business workflow.

### Alignment

The repository port is defined around the needs of the application.

The infrastructure adapter conforms to that port instead of forcing the application to adopt its asynchronous API.

### Resilience

Changing the MQTT library or database driver has less impact on the use case.

Infrastructure changes remain closer to the adapters.

### Domain Integrity

The `SensorReading` model owns the operation that moves it into the anomalous state.

The use case decides when that valid domain transition is required.

### Separation

Receiving data, processing it, and adapting persistence are now distinct responsibilities.

Concurrency remains outside the business logic.

---

## Trade-offs

The refactoring introduces another adapter and a boundary between synchronous and asynchronous execution.

That is additional code.

The benefit is not fewer lines. The benefit is controlling where infrastructure decisions are allowed to spread.

For a tiny script, the original version may be acceptable. As the system grows, the separated design becomes more valuable because:

- use cases remain easier to call
- tests remain simpler
- new entry points can reuse the same behavior
- infrastructure changes remain localized

The boundary is valuable when the application logic is expected to outlive the current infrastructure choices.

---

## Key takeaways

- Receiving a sensor reading and processing a sensor reading are different responsibilities.
- The use case now receives a domain object because obtaining that object belongs to infrastructure orchestration.
- Async remains in the MQTT client and database implementation.
- The application depends on a synchronous repository port.
- The infrastructure adapter bridges the synchronous application interface and async database implementation.
- Domain behavior remains synchronous, focused, and easy to test.
- Ports should describe application needs rather than adapter mechanics.
- The infrastructure should adapt to the core, not the other way around.