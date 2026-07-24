# Lecture Notes - Configuration vs Convention

## Overview

In this lesson, we explored one of the most common design decisions in software engineering:

> **Should this be configurable, or should it simply be part of the application?**

Configuration provides flexibility, but every configuration option increases the complexity of a system. It introduces additional system states, operational overhead, and opportunities for mistakes.

The goal of this lesson is not to discourage configuration. Instead, it is to understand:

- what belongs in configuration,
- where configuration should live,
- what can go wrong,
- and when conventions are a better alternative.

Throughout the lesson, we use examples from a booking system together with a real-world production incident to illustrate these trade-offs.

---

# Configuration Is Part of Your Software Design

A production incident can originate entirely from configuration.

In the example from the lesson, a production backend unexpectedly connected to the staging database because the database connection string in an environment variable was incorrect.

The Python code was completely correct.

The failure came from the system configuration.

This highlights an important principle:

> Configuration deserves the same design attention as source code.

Poorly designed configuration can be just as expensive as poorly designed code.

---

# What Is Configuration?

Configuration is information that can change without modifying the application itself.

Typical examples include:

- database connection strings
- API keys
- logging levels
- storage locations
- service endpoints

A useful question is not:

> **Can this be configurable?**

Instead ask:

> **Should this be configurable?**

Modern AI coding tools frequently move values into configuration because it increases flexibility. However, every additional configuration option also increases the complexity of the system.

---

# Different Ways to Configure an Application

Configuration can live in several places.

## Hardcoded Values

Some values simply remain in code.

```python
BOOKING_TIMEOUT = 10
```

Advantages:

- simple
- discoverable
- easy to refactor
- fully supported by IDEs and type checkers

If a value never changes outside development, keeping it in code is often the simplest solution.

---

## Environment Variables

Environment variables are excellent for deployment-specific information.

Examples:

- `DATABASE_URL`
- `REDIS_URL`
- `LOG_LEVEL`

These typically differ between development, staging, and production.

---

## Centralized Settings Objects

In Python, a `BaseSettings` class (for example using Pydantic Settings) is often preferable to reading environment variables throughout the application.

Benefits include:

- centralized configuration
- type validation
- sensible defaults
- improved discoverability
- IDE support

Instead of scattering configuration access throughout the codebase, all configuration is collected in one location.

---

## Configuration Files

Configuration files such as YAML or JSON are useful when many related settings should be edited together.

Examples include:

- notification providers
- retry counts
- deployment-specific options

However, configuration files can become problematic when they begin expressing application behavior instead of simple values.

---

## Database Configuration

Some systems store configuration in a database.

Typical examples include:

- feature flags
- maintenance mode
- discount percentages

This enables runtime changes without redeployment.

However, runtime configuration also increases operational complexity because the application's behavior can change while it is running.

---

# What Should Be Configuration?

A useful rule of thumb is:

> **Configure deployment differences and business choices.**

Examples include:

- database URLs
- API keys
- logging levels
- storage locations

These genuinely differ between deployments.

Avoid configuring implementation details.

Examples of poor configuration include:

- validator class names
- algorithm versions
- concrete implementation types

If developers are the only people who will ever change a value, it often belongs in code rather than configuration.

---

# Beware of Configuration Becoming a Programming Language

Sometimes configuration begins describing business logic.

For example, cancellation rules stored in YAML instead of Python.

Although this appears flexible, the application still contains business logic.

It has simply moved into configuration.

This has several disadvantages:

- reduced type safety
- poorer IDE support
- more difficult refactoring
- harder navigation through the codebase

If every deployment uses the same behavior, expressing it directly in code is often clearer.

---

# What Can Go Wrong?

Configuration introduces its own failure modes.

## Incorrect Values

A configuration value can simply be wrong.

The production database accidentally pointing to staging is an example.

The code behaved exactly as instructed.

The configuration did not.

---

## Defaults

Defaults require careful thought.

Good default:

```python
log_level = "INFO"
```

Reasonable because the application still behaves safely.

Dangerous default:

```python
database_url = "postgres://localhost/booking"
```

A missing production database configuration could silently connect to the wrong database.

Some settings should fail immediately instead of guessing.

---

# Hidden Dependencies

Configuration values often become dependent on one another.

Example:

Selecting Stripe requires:

- Stripe API key

Selecting Adyen requires:

- Adyen Client ID
- Adyen Client Secret

Soon configuration rules become:

- If A is selected, B is required.
- If C changes, D becomes invalid.

The coupling has not disappeared.

It has simply moved outside the Python code.

Each additional configuration option increases the number of possible system states that must be understood and tested.

---

# Validating Configuration

One way to reduce mistakes is to validate configuration during application startup.

Examples include:

- ensuring production connects to the production database
- ensuring required credentials exist for the selected payment provider

Frameworks such as Pydantic Settings make this straightforward.

Startup validation prevents applications from running with invalid configurations.

Failing fast is usually preferable to discovering problems later in production.

---

# Convention Over Configuration

Validation is useful.

But sometimes it reveals a deeper insight.

If the same validation rules are written repeatedly, perhaps the values should not be independently configurable.

For example:

Instead of configuring:

- environment
- database connection string

independently,

the application can derive the correct database from the selected environment.

This removes an entire class of deployment mistakes.

The same principle applies elsewhere.

Rather than configuring every email template, the application can derive the template name using a naming convention.

Conventions reduce:

- documentation
- testing effort
- operational mistakes
- cognitive load

They eliminate decisions instead of validating them afterwards.

A good convention removes invalid states from the system entirely.

---

# Practical Guidelines

Before introducing a new configuration option, ask yourself:

1. Does this genuinely differ between deployments?
2. Will someone outside the development team change it?
3. Can this value be validated?
4. Would a convention eliminate the need for this configuration?

If a convention works for the vast majority of deployments, it is often the simpler and more maintainable design.

---

# Key Takeaways

- Configuration is part of your software design.
- Centralize configuration instead of scattering it throughout the application.
- Use typed, validated settings objects whenever possible.
- Configure deployment differences and genuine business choices.
- Keep implementation details in code.
- Be careful with defaults.
- Hidden dependencies between configuration values increase complexity.
- Validate configuration during application startup.
- When you repeatedly validate the same assumptions, consider replacing configuration with a convention.
- Good conventions eliminate entire categories of mistakes.

---

# Bridge to the Next Lesson

In this lesson, we examined one way developers prepare for future change by introducing configuration.

In the next lesson, we'll explore another common form of future-proofing:

**Generality vs Specificity.**

We'll see when designing generic, reusable solutions is worthwhile, and when a focused, specific implementation leads to a simpler, more maintainable system.