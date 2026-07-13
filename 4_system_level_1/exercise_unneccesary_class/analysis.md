> Don't read any further until you tried coming up with a solution yourself!


# Solution & Analysis

## Why remove the class?

At first glance, `AvailabilityChecker` looks like a reasonable object. It groups related behavior and gives the code a nice name.

However, if we look more closely, the class doesn't actually behave like an object.

Ask yourself the following questions.

### Does it own any state?

No.

Every method receives all of the information it needs through its parameters.

The object itself never stores anything.

### Does it have an identity?

No.

Creating two `AvailabilityChecker` instances makes no difference.

```python
checker1 = AvailabilityChecker()
checker2 = AvailabilityChecker()
```

Both objects behave exactly the same.

### Does it manage a lifecycle?

No.

There is nothing to initialize, update, or clean up.

### Does it protect any invariants?

No.

The class doesn't ensure that any rules remain true over time because it doesn't own any data.

---

# What changed?

Instead of creating an object:

```python
checker = AvailabilityChecker()

checker.is_available(...)
```

we simply call:

```python
is_available(...)
```

The behavior is exactly the same.

The design is simpler because we've removed an unnecessary abstraction.

---

# Why is this an improvement?

The refactored version has several advantages.

- One fewer object to understand.
- No unnecessary object creation.
- Less indentation.
- Simpler API.
- Easier to compose with other functions.
- Easier to reuse in different contexts.

Most importantly, the abstraction now matches the problem.

We're simply transforming inputs into outputs.

---

# Would a class ever make sense?

Yes.

Suppose the requirements change.

For example:

- the booking calendar should be cached
- availability should be loaded from a database
- booking rules depend on hotel configuration
- availability checks should keep statistics
- multiple availability requests share common state

Now there is something for an object to own.

For example:

```python
checker = AvailabilityChecker(
    repository,
    pricing_policy,
)
```

The class now has responsibilities that persist over time.

Its complexity is justified because it manages state and coordinates multiple dependencies.

---

# Key Lesson

Ask yourself: "What responsibilities does this abstraction actually have?"

If the answer is simply:

- transform some inputs
- return a result

then a function is often the clearest solution.

If the answer involves:

- owning state
- protecting invariants
- managing lifecycle
- coordinating shared dependencies

then a class is likely the better abstraction.