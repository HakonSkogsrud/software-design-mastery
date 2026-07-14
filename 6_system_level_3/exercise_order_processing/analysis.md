> Don't read any further until you tried coming up with a solution yourself!

# Solution & Analysis

The original `place_order()` use case gradually became responsible for coordinating many unrelated workflows. Every new requirement meant opening the same function and adding another call.

```text
place_order()
    ├── reserve inventory
    ├── save order
    ├── send email
    ├── update loyalty points
    ├── record analytics
    └── send webhook
```

None of these operations were wrong individually. The problem was that the use case became the central coordinator for the entire application.

# Keeping the Core Workflow Small

The solution reduces `place_order()` to its essential responsibilities:

1. Reserve inventory.
2. Save the order.
3. Publish an `OrderPlaced` event.

Note that inventory reservation remains a direct function call. This is intentional.

An order should not be stored if inventory cannot be reserved. Reserving inventory is therefore part of the core business transaction, not a side effect that can happen later.

In contrast, sending emails or recording analytics are reactions to a successful order. They are good candidates for event handlers because they don't define whether placing the order succeeds.

This illustrates an important design principle: events should be used for independent reactions, not for the core business workflow itself.

# Events Describe Business Facts

The exercise introduces an `OrderPlaced` event.

This is an example of a **domain event**.

Notice that the event describes something that has already happened.

Good:

- `OrderPlaced`

Poor:

- `SendConfirmationEmail`
- `KafkaOrderMessage`
- `WebhookPayload`

Domain events should express business meaning, not infrastructure or implementation details.

Keeping the language focused on the domain improves **Alignment** because the business model remains independent from technology choices.

# Event Handlers Own Their Own Responsibilities

Instead of one large orchestration function, each concern now lives in its own handler.

For example:

- confirmation emails
- loyalty points
- analytics
- partner webhooks

Each handler has a single responsibility and can evolve independently.

Adding another reaction often requires only:

1. writing a new handler,
2. subscribing it to the event bus.

The original use case remains unchanged.

This is the Open/Closed Principle in practice: extending behavior without modifying existing application logic.

# A Simple Event Bus Is Enough

The in-memory event bus demonstrates the architectural idea without introducing unnecessary complexity.

At this point, there is no:

- message broker,
- queue,
- asynchronous processing,
- distributed system.

Those are implementation details that can be introduced later if the system requires them.

The important lesson is that **the application now communicates through events instead of direct coordination**.

# Why the Event Bus Is Configured Separately

Note that handlers are registered during application startup instead of inside the use case. This keeps responsibilities separated.

The use case does not know which handlers exist, how many there are, or whether any exist at all. It simply publishes an event.

This improves **Separation** because business logic remains independent from application wiring.

# Trade-offs

Event-based architecture is not free.

Compared to the original solution, we've traded one kind of complexity for another.

### Benefits

- Lower coupling between workflows.
- Easier to add new functionality.
- Better separation of responsibilities.
- Natural extension point for integrations.

### Costs

- Control flow becomes less obvious.
- Debugging can be harder.
- More moving parts.
- Coordination shifts from direct function calls to event subscriptions.

A good software designer understands both sides of this trade-off.

# Key Takeaways

This exercise demonstrates that event-driven architecture is primarily about **reducing coupling between workflows**.

Instead of building larger orchestration functions, the application publishes business events and allows independent parts of the system to react.

The result is a system that is easier to extend and maintain as requirements evolve.

Most importantly, the use case once again focuses on its primary responsibility: placing an order. Everything else becomes an independent reaction to that completed business action.