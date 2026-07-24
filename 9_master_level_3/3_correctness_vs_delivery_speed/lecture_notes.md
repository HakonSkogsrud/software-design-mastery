# Lecture Notes - Correctness vs Delivery Speed

## Overview

In this lesson, we explore the trade-off between **correctness** and **delivery speed**. Every software team faces pressure to deliver features quickly, but every shortcut increases the risk of defects reaching production. The challenge is not to maximize either speed or correctness, but to apply the right amount of confidence where it matters most.

Using a finance platform as an example, we'll look at correctness as a system-wide concern that involves architecture, development practices, deployment strategies, and team culture—not just writing bug-free code.

---

# The Trade-Off

Correctness and delivery speed pull in opposite directions.

Prioritizing **delivery speed** allows teams to:

- Ship features quickly
- Respond to customer feedback
- Experiment and iterate
- Maintain business momentum

Prioritizing **correctness** helps teams:

- Prevent expensive failures
- Build customer trust
- Reduce operational incidents
- Protect critical business processes

Neither extreme is desirable:

- Moving too quickly increases production risk.
- Pursuing perfect correctness slows delivery and reduces the ability to learn from real users.

The goal is **appropriate confidence**, not perfect correctness.

---

# Correctness Depends on Risk

Not every part of a system requires the same level of rigor.

### Lower-risk features

Examples include:

- Dashboard colors
- Sorting preferences
- Help text
- Cosmetic UI changes

Mistakes here are usually inexpensive and easy to fix.

### Higher-risk features

Examples include:

- Account balances
- Payment processing
- Portfolio valuation
- Tax reporting

Failures in these areas may:

- Lose money
- Damage customer trust
- Create regulatory or legal issues
- Affect many users

---

## Factors That Determine Correctness Requirements

Before deciding how much effort to spend on correctness, consider:

- **Domain risk** — How serious are the consequences of failure?
- **Number of users** — How many people could be affected?
- **Recoverability** — Can the mistake be reversed?
- **Detectability** — How quickly would the issue be noticed?
- **Blast radius** — How much of the system is affected?
- **Business criticality** — Is this functionality essential?

Correctness effort should always be proportional to operational risk.

---

# Correctness Starts Before Writing Code

One of AI's biggest impacts is that writing code has become much faster.

That makes it tempting to skip the design phase.

However, AI will implement a poor design just as efficiently as a good one.

Before implementing a feature—or asking AI to implement it—take time to think about the design.

Useful questions include:

- What are the important domain concepts?
- What assumptions are we making?
- Which invariants must always hold?
- Where should validation occur?
- What operational failures are possible?

This is **not** a waterfall approach.

The goal is not to predict every future requirement.

Instead, spend a few minutes understanding the problem before generating large amounts of code.

A short design discussion often prevents hours of debugging later.

> AI has reduced the cost of writing code. It has not reduced the value of making good design decisions.

---

# Add Simple Guardrails

Correctness is not only achieved through algorithms.

Many expensive failures can be prevented with inexpensive safeguards.

### Example

A production backend accidentally connects to a staging database.

Even if the application code is correct:

- Users see inconsistent data.
- Reports become unreliable.
- Engineers waste time diagnosing confusing behavior.

A simple startup validation that verifies the expected database can prevent this entire class of failures.

The lesson:

> Look for inexpensive checks that prevent expensive mistakes.

These kinds of guardrails greatly improve system resilience.

---

# Correctness Is a Team Responsibility

Correctness is created through team practices as much as through code.

Useful habits include:

- Reviewing business rules, not only implementation details
- Adding monitoring before releasing risky functionality
- Using feature flags
- Labeling pull requests by risk level
- Maintaining checklists for critical changes

Not every feature requires the same process.

The amount of review and verification should match the potential impact of failure.

---

# Reduce Risk Without Slowing Development

Correctness does not always require delaying releases.

Instead, reduce the consequences of mistakes.

Common strategies include:

- Beta programs
- Internal releases
- Canary deployments
- Staged rollouts
- Feature flags
- Automatic rollback
- Shadow mode (running new logic alongside existing logic before enabling it)

These approaches allow teams to continue delivering quickly while minimizing operational risk.

---

# AI and Correctness

AI coding assistants significantly increase development speed.

They can generate:

- Code
- Unit tests
- Refactorings
- Documentation

However, faster generation does **not** automatically mean greater correctness.

A common problem is that AI generates tests that verify the implementation it just produced.

If the implementation misunderstood the business rules, the tests may confirm the same mistake.

Therefore:

- More tests do **not** automatically mean more confidence.

Instead of only asking AI to generate tests, also ask questions such as:

- What assumptions does this implementation make?
- Which business rules are missing?
- Which edge cases should be tested?
- What invariants should always hold?

AI is excellent at exploring possibilities.

Humans remain responsible for determining what "correct" actually means.

> AI has made it cheaper to write tests. It has not made it cheaper to know what should be tested.

---

# Good Design Makes Correctness Easier

Architecture influences correctness.

Clear domain models, meaningful types, and explicit interfaces make software easier to understand and verify.

When intent is communicated clearly:

- Code reviews become easier.
- Testing becomes easier.
- AI has better context.
- Hidden assumptions become visible.

This reinforces two CARDS principles:

- **Clarity** — The design communicates intent.
- **Domain Integrity** — Invalid states are prevented through good modeling.

Good design reduces the amount of verification needed because fewer mistakes are possible in the first place.

---

# Key Takeaways

- Correctness is a form of risk management.
- Match correctness effort to the cost of failure.
- Think before implementing—AI accelerates coding, not design thinking.
- Add inexpensive guardrails that prevent costly operational mistakes.
- Use deployment strategies to reduce risk while maintaining delivery speed.
- Build team habits that consistently improve correctness.
- AI-generated code and tests still require human verification.
- Clear software design makes correctness easier to achieve.

---

# Bridge to the Next Lesson

This lesson focused on balancing confidence with speed.

In the final lesson of the Master Designer phase, we'll zoom out and look at the broader architectural question that underlies many of the trade-offs we've discussed:

**Short-Term Productivity vs Long-Term Maintainability**

We'll explore how seemingly small design decisions accumulate over time, and how experienced software designers know when to optimize for immediate progress—and when it's worth investing in a healthier system for the future.