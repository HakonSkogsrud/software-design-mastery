# Lecture Notes - Generality vs Specificity

## Overview

In this lesson, we explored the trade-off between **Generality** and **Specificity**. General solutions provide flexibility, but they also introduce complexity. Specific solutions are often easier to understand and maintain, but they may eventually require refactoring as requirements evolve.

The goal is **not** to avoid generality. Instead, the goal is to introduce it only when it solves real, proven problems rather than imagined future ones.

This lesson concludes Level 1 by reinforcing a recurring theme from the previous lessons: **delay unnecessary complexity until it has earned its place.**

---

# Generality Is a Trade-Off

Software exists on a spectrum.

On one end are highly specific solutions that solve a single problem well.

On the other end are highly general solutions that can support many different use cases.

Neither approach is inherently better.

The key question is:

> **How much future flexibility is worth paying for today?**

Every increase in flexibility comes with costs, including additional concepts, abstractions, maintenance, testing, documentation, and onboarding effort.

---

# Thinking Ahead vs Building Ahead

Good software designers should think about the future.

However, there is an important distinction between:

- **Thinking ahead** — considering how requirements may evolve.
- **Building ahead** — implementing flexibility before there is evidence it is needed.

Planning for change is valuable.

Paying the cost of speculative complexity usually is not.

---

# Case Study: Building for the 1%

A useful example comes from the development of a SaaS platform for university programming education.

The original analytics requirement was simple:

> Show teachers how their students are progressing.

Instead of building a straightforward dashboard, the system evolved into a highly flexible analytics platform.

The design allowed teachers to create custom analytics blocks. Each block contained Python code that generated its own interface from the underlying data and executed on the backend.

Although technically elegant, this introduced significant complexity:

- Dashboard generation became slow because code had to execute on every request.
- Caching mechanisms had to be introduced.
- Cache invalidation became another maintenance concern.
- Teachers accidentally introduced bugs into their own analytics blocks.
- Support requests increased because users struggled to understand the customization system.

After all of that engineering effort, almost every teacher wanted exactly the same thing:

> **How many exercises have my students completed?**

### The Lesson

The system had been optimized for the **1%** of users who might someday require complete flexibility.

In doing so, it became more complicated for the **99%** who simply wanted a standard dashboard.

This illustrates an important architectural principle:

> Every layer of flexibility should benefit more people than it inconveniences.

---

# Generality Is Never Free

Generality is often discussed in terms of what it enables.

It is equally important to consider what it costs.

Typical costs include:

- additional abstractions
- more indirection
- increased maintenance
- larger testing surface
- more documentation
- greater onboarding effort
- increased support burden

These costs affect not only developers but often users as well.

Generality is therefore not just a coding decision—it is also a product and business decision.

---

# The Finance Reporting Example

Initially, the finance application only needs one report:

- a monthly financial summary.

A focused implementation consists of a single function that performs exactly that task.

A common temptation is to immediately replace this with a generic reporting framework:

- report engines
- registries
- plugin systems
- dynamically registered reports

Although flexible, such a framework introduces complexity before there is evidence that multiple report types actually require it.

The system has been optimized for hypothetical future requirements instead of actual business needs.

---

# This Trade-Off Exists at Every Level

The same question appears throughout software design.

### Function level

Should we write a focused function or create a generic engine?

### Module level

Should we have a few report functions or an extensible reporting framework?

### Application level

Should reporting simply be another feature or become its own service?

### Organization level

Should every team solve reporting independently or should the company build a shared reporting platform?

The answer always depends on the same question:

> **Does the additional flexibility justify the additional complexity?**

---

# YAGNI

YAGNI stands for:

> **You Aren't Gonna Need It**

It is often misunderstood.

YAGNI does **not** mean:

- never think ahead
- never design for change

Instead, it means:

> **Do not implement flexibility until there is evidence that it is actually needed.**

The principle encourages delaying speculative complexity while remaining prepared to evolve the design when necessary.

---

# Let Abstractions Emerge Naturally

Suppose the finance application grows and now supports several reports:

- monthly summaries
- tax summaries
- cashflow summaries

Only after implementing these reports do repeated patterns become visible.

Examples include:

- filtering transactions by date
- calculating transaction totals
- exporting report data

At this point, extracting shared functionality becomes a natural design improvement.

The abstraction is no longer speculative.

It has been justified by real variation.

A useful rule of thumb is:

> **Don't invent abstractions. Discover them.**

---

# Domain-Specific Code Communicates Better

Business software exists to solve business problems.

For that reason, domain-specific names often communicate intent more effectively than generic ones.

For example:

- `calculate_transaction_totals()`

communicates far more clearly than a generic function such as:

- `aggregate(data, strategy, configuration)`

Generic APIs may be reusable, but they often hide the actual business meaning.

Domain-specific terminology supports **Domain Integrity** by allowing the code to mirror the language of the business.

---

# Questions to Ask Before Generalizing

Whenever you are about to introduce a more generic design, ask yourself:

- How many concrete use cases exist today?
- Am I solving a real problem or an imagined one?
- Who benefits from this flexibility?
- Who pays for the added complexity?
- Could I introduce this abstraction later if it becomes necessary?

These questions help determine whether the abstraction has truly earned its place.

---

# The Common Theme of Level 1

Across the first four lessons, a clear pattern emerges.

### Build vs Buy

Delay ownership until it is worthwhile.

### Abstraction vs Duplication

Delay abstraction until repetition appears.

### Configuration vs Convention

Delay configuration until variation becomes real.

### Generality vs Specificity

Delay generality until multiple concrete use cases justify it.

The shared principle is:

> **Delay unnecessary complexity until it has earned its place.**

Good architecture is not about predicting the future perfectly.

It is about building systems that can evolve gracefully when the future eventually arrives.

---

# Key Takeaways

- Generality increases flexibility but always introduces additional complexity.
- Complexity affects code, products, performance, support, onboarding, and maintenance.
- Thinking ahead is valuable; building speculative flexibility often is not.
- Optimize for the users and use cases you actually have today.
- Let abstractions emerge from proven variation rather than imagined future requirements.
- Domain-specific solutions often communicate intent more clearly than generic frameworks.
- Every layer of flexibility should justify the complexity it introduces.

---

# Bridge to the Next Lesson

In this level, we focused on trade-offs involved in **introducing complexity** into a system. We explored when to build, when to abstract, when to configure, and when to generalize.

In the next level, the complexity is already present. Instead of deciding whether to introduce it, we'll learn how to manage communication and coordination between different parts of a growing system. We'll begin by exploring one of the most fundamental architectural decisions: **Synchronous vs Asynchronous communication**.