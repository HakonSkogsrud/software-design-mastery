# Lecture Notes - Build vs Buy

## Overview

In this lesson, we explore one of the most common architectural trade-offs you'll encounter as a software designer:

> **Should we build it ourselves, or should we adopt an existing solution?**

This is no longer just a question of implementation effort. Modern AI tools make it possible to generate working code in minutes, making custom implementations more attractive than ever.

The important insight, however, is that **build vs buy is fundamentally an ownership decision**.

Throughout this lesson we'll see that libraries, frameworks, APIs, and platforms offer much more than source code. They also provide years of accumulated expertise, maintenance, documentation, ecosystem integration, and future improvements.

As a software designer, your goal is to spend your engineering effort where it creates the most value for your users—not where it simply replaces existing infrastructure.

---

# Build vs Buy Is an Ownership Decision

When discussing build vs buy, many developers immediately think about code.

Instead, think about **ownership**.

When you build something yourself, you also become responsible for:

- Maintaining it
- Fixing bugs
- Supporting new requirements
- Keeping it compatible with new language versions
- Documenting it
- Helping other developers understand it
- Continuing its development over time

The implementation is only the beginning.

---

# A Personal Example

One of the most important software design lessons I learned came from an earlier startup.

We were building a website builder for musicians.

At the time, React already existed.

Instead of adopting it, we decided it didn't quite fit our needs and built our own rendering engine that generated HTML.

Initially this felt like a good decision.

We had complete control over how everything worked.

Over time, however, every new feature became more difficult.

Examples included:

- Responsive layouts
- Reusable components
- State management
- Performance improvements

Small architectural decisions in the rendering engine affected every feature built on top of it.

Eventually we realized we weren't just building a product for musicians anymore.

We had accidentally become developers of our own front-end framework.

Looking back, this was one of the reasons the company ultimately failed.

We spent our time solving framework problems instead of customer problems.

---

# Why AI Makes This Trade-Off Harder

AI has significantly lowered the cost of creating the **first version** of a solution.

Need a validation library?

Ask AI.

Need a rendering engine?

Ask AI.

Need a small framework?

Ask AI.

Within minutes you'll often have something that appears to work.

This creates an important illusion:

> If AI can generate it, why use an existing library?

The answer is simple:

The first version was never the expensive part.

Long-term ownership is.

---

# Example: Pydantic in a Finance Application

Suppose our finance application receives transaction data from external systems.

Using Pydantic, defining the input model is straightforward:

```python
class TransactionInput(BaseModel):
    account_id: str
    amount: Decimal
    currency: str
    description: str
```

Pydantic immediately provides:

- Input validation
- Type conversion
- Useful error messages
- Serialization support
- Strong typing

Later we discover a business requirement:

> Each organization only supports certain currencies.

At first glance, it might seem that Pydantic no longer fits our needs.

This is often where developers decide to build something themselves.

---

# The Temptation to Replace a Library

An AI assistant can quickly generate a custom validation class.

Initially this looks attractive.

However, requirements tend to grow.

Soon you need:

- Better validation
- Nested models
- Serialization
- Better error reporting
- Schema generation

Without realizing it, you've started rebuilding Pydantic.

---

# The Wrong Comparison

Many developers compare:

**Pydantic**

vs.

**A few hundred lines of AI-generated code**

This is the wrong comparison.

The real comparison is:

**Pydantic**

vs.

**Maintaining your own validation framework for years.**

---

# What You're Really Buying

When adopting a mature library like Pydantic, you're getting much more than code.

You're also getting:

- Years of production experience
- Bug fixes
- Performance improvements
- Documentation
- Typing integration
- Future compatibility with Python
- Continued development by the community

Most of this value isn't visible in the source code.

---

# Ecosystem Integration

Another advantage of buying is ecosystem support.

Pydantic integrates directly with FastAPI.

The same model automatically provides:

- Request validation
- Error responses
- OpenAPI documentation
- Schema generation

If you replace Pydantic with your own implementation, you don't only lose Pydantic.

You also lose the ecosystem that has grown around it.

This hidden integration is often far more valuable than the initial implementation itself.

---

# Build Around Existing Solutions

Using an existing library doesn't mean all logic belongs inside that library.

Our business rule is:

> An organization only supports specific currencies.

That is **business logic**, not generic validation.

A better design is:

- Use Pydantic for generic validation.
- Keep business rules in your own domain layer.

This gives each component a clear responsibility.

---

# CARDS Perspective

This design reinforces several CARDS principles.

### Separation

Keep generic infrastructure separate from business logic.

### Alignment

Business rules should not depend on the implementation details of a validation library.

### Resilience

If the validation library changes in the future, the business rules remain largely unaffected.

---

# Applying the Lesson

I encountered the same decision again while building Software Design Mastery.

The learning platform I use has limitations.

For example:

- Code discussions could be better.
- The API is limited.
- Some programming-specific features are missing.

For a while, I considered building my own course platform.

But then I remembered the lesson from my startup.

Building a learning management system is a completely different business from creating software engineering education.

Even if I could eventually build something better, it would require years of engineering effort.

Those are years I would rather spend improving the courses themselves.

Sometimes an imperfect existing solution is still the better architectural decision.

---

# Practical Heuristics

When deciding whether to build or buy, ask yourself:

- Is this where our product creates value?
- Do we want to become experts in this problem?
- What will this cost us to own over the next five years?
- What ecosystem would we lose by replacing the existing solution?

These questions are usually more valuable than comparing implementation effort.

---

# Key Takeaways

- **Build vs buy is fundamentally an ownership decision.**
- Existing libraries, frameworks, APIs, and platforms provide much more than source code.
- They also provide expertise, maintenance, documentation, ecosystem integration, and future improvements.
- AI has dramatically reduced the cost of building the first version of a solution.
- AI has **not** reduced the cost of owning that solution.
- Build the parts that make your product unique.
- Adopt existing solutions for generic capabilities whenever it makes sense.

---

# Looking Ahead

In this lesson we focused on deciding **whether something should exist in our codebase at all**.

Once we've decided to build something ourselves, another important question appears:

> **How much structure should we introduce from the beginning?**

In the next lesson we'll explore another common software design trade-off:

**Abstraction vs Duplication**.

We'll see that just because we're writing code ourselves doesn't necessarily mean we should immediately try to make it generic or reusable.