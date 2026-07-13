# Exercise 1 — Keep Concurrency Out of the Sensor Domain

An environmental monitoring system receives temperature readings from remote sensors through an MQTT broker. The MQTT client is asynchronous because it waits for incoming network messages.

The current implementation allows this asynchronous behavior to leak into the application layer. The main use case depends directly on the async MQTT client and an async repository, even though its primary responsibility is simply to determine whether a sensor reading is anomalous and store the result.

Your goal is to refactor the application so that the business logic no longer depends on asynchronous infrastructure.

## Your task

Refactor the code so that:

- The application use case becomes synchronous.
- The use case no longer depends on the MQTT client.
- The repository port becomes synchronous.
- The async database implementation remains asynchronous.
- A synchronous adapter bridges the application and the async database.
- The orchestration code is responsible for receiving sensor readings before invoking the use case.

Do **not** change the business behavior of the application.

The system should still:

- receive two sensor readings,
- mark readings with temperatures below **−20°C** or above **50°C** as anomalous,
- store the processed readings,
- print the stored readings at the end.

Focus on improving the architecture rather than changing the functionality.