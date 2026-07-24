# Lecture Notes - Stability vs Speed of Change

## Overview

In the earlier phases of Software Design Mastery, we focused on making software easier to change. We learned how to reduce coupling, create stable abstractions, and design systems that remain maintainable as they grow.

As systems mature, however, a new challenge emerges. Not every part of a system should evolve at the same speed.

This lesson explores one of the most important architectural trade-offs:

> **How do you continue evolving a system without constantly breaking the people and software that depend on it?**

We'll discuss:

- The difference between internal and external interfaces
- Why stable interfaces enable faster long-term development
- Semantic Versioning and API versioning
- Stable user experiences
- How AI changes the risks around software evolution
- Practical guidelines for balancing stability and speed

---

# Stability vs Speed of Change

Software should evolve.

New requirements appear, performance improves, bugs are fixed, and better designs emerge over time.

But while developers often benefit from rapid change, the people using our software usually benefit from stability.

A mature system therefore doesn't try to maximize the speed of change everywhere.

Instead, it deliberately decides where change should happen quickly and where stability should be preserved.

---

# Internal vs External Interfaces

One of the most important distinctions is between **internal** and **external** interfaces.

## Internal interfaces

Internal interfaces are only used within your own codebase.

Examples include:

- Function signatures
- Internal classes
- Repository interfaces
- Service abstractions

Because you control all of the consumers, these interfaces can usually evolve relatively quickly.

Refactoring internal code is often inexpensive.

---

## External interfaces

External interfaces are consumed by someone outside the module—or even outside your organization.

Examples include:

- REST APIs
- GraphQL APIs
- Webhooks
- Event schemas
- SDKs
- Command-line interfaces

These interfaces become contracts.

Once customers, applications, or other teams depend on them, changing them becomes much more expensive.

Protecting these interfaces improves **Resilience** by reducing the impact of change.

---

# Stable Interfaces Enable Faster Development

It may seem that keeping interfaces stable slows development.

In reality, stable interfaces often make development faster.

When a public contract remains stable:

- implementations can evolve freely behind it
- consumers don't need to update continuously
- refactoring becomes safer
- teams become more confident making internal improvements

A stable interface acts as a protective boundary.

The implementation behind that boundary can change dramatically while the rest of the system continues working unchanged.

---

# Managing Change Predictably

Change itself is not the problem.

Unexpected change is.

Well-designed software communicates how change will happen.

Several techniques help make software evolution predictable.

---

## Semantic Versioning

Semantic Versioning communicates the expected impact of a new release.

A version number has three parts:

**Major.Minor.Patch**

For example:

```
2.4.7
```

### Patch release

- Bug fixes
- No breaking changes expected

Example:

```
2.4.7 → 2.4.8
```

---

### Minor release

- New functionality
- Backward compatible

Example:

```
2.4.7 → 2.5.0
```

---

### Major release

- Breaking changes may occur
- Consumers should review migration notes

Example:

```
2.4.7 → 3.0.0
```

Semantic Versioning is more than a numbering scheme.

It is a promise about the expected stability of an upgrade.

---

## API Versioning

Sometimes breaking changes cannot be avoided.

Rather than forcing every client to update immediately, APIs often expose multiple versions.

For example:

```
/api/v1/bookings
/api/v2/bookings
```

This allows:

- existing clients to continue working
- new clients to adopt the latest version
- gradual migration
- planned deprecation of older versions

Versioning slows interface evolution while allowing implementation to continue evolving internally.

---

# Stability Matters for Users Too

Software interfaces are not only consumed by programs.

They are also consumed by people.

Imagine an application where:

- menus move every month
- workflows constantly change
- buttons appear in different places
- terminology changes regularly

Even if each redesign is individually better, users must continually relearn the application.

Frequent change creates cognitive overhead.

Sometimes the best interface is not the newest one.

It's the one users already know.

A stable user experience is often just as valuable as a stable API.

---

# AI Changes the Equation

AI coding assistants dramatically increase the speed at which software can evolve.

Large refactorings that previously required days of work can now happen in minutes.

This is a significant productivity improvement.

However, AI also introduces new risks.

## AI can make larger changes

An AI assistant may update dozens or hundreds of files during a refactoring.

Large-scale improvements become much easier.

---

## AI may change public contracts unintentionally

An AI model often sees local consistency, not organizational boundaries.

For example, it may rename a field because it appears more consistent, without realizing that external customers depend on the existing API.

A local improvement can accidentally become a breaking change.

---

## AI may modify files you weren't expecting

AI tools sometimes update:

- serializers
- event definitions
- API schemas
- documentation
- SDKs
- test fixtures

If these changes aren't reviewed carefully, subtle breaking changes can slip into a release.

As AI becomes more capable, clearly defining stable interfaces becomes even more important.

They establish boundaries that should only change deliberately.

---

# A Practical Question

Whenever you consider changing an interface, ask:

> **Who depends on this?**

If the answer is:

- only this module

you can usually move quickly.

If the answer includes:

- other teams
- customers
- third-party integrations
- long-lived applications

then stability becomes much more valuable.

Interfaces that many consumers depend on effectively become infrastructure.

---

# Practical Guidelines

When balancing stability and speed of change:

- Move quickly inside stable boundaries.
- Keep implementation details flexible.
- Treat public interfaces as long-term contracts.
- Use Semantic Versioning to communicate the impact of releases.
- Introduce API versioning when breaking changes are unavoidable.
- Provide migration paths and deprecation periods.
- Review AI-generated changes carefully, especially when they affect public interfaces.
- Remember that predictable software builds trust.

---

# CARDS Connections

## Resilience

Stable interfaces reduce the impact of change and allow implementations to evolve without affecting consumers.

---

## Separation

Keeping internal implementations separate from public contracts allows both to evolve at different speeds.

---

## Clarity

Well-defined contracts, clear versioning, and predictable releases make software easier to understand and safer to maintain.

---

# Key Takeaways

- Different parts of a system should evolve at different speeds.
- Internal interfaces can usually change freely.
- External interfaces should be treated as long-term contracts.
- Stable interfaces often increase long-term development speed.
- Semantic Versioning communicates the expected impact of upgrades.
- API versioning allows breaking changes without disrupting existing consumers.
- Stable user interfaces improve usability and reduce unnecessary relearning.
- AI accelerates software evolution but also increases the risk of unintended breaking changes.
- Protecting stable boundaries becomes even more important as AI tools become more capable.

---

# Bridge to the Next Lesson

Stable interfaces protect systems from unnecessary change, but real applications rarely exist in isolation. Services exchange data, components collaborate, and external systems need to integrate with our software.

In the next lesson, **Isolation vs Integration**, we'll explore how to design systems that work together effectively without becoming tightly coupled, and how to choose the right balance between independence and collaboration.