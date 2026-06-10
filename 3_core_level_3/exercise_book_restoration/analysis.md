> Don't read any further until you tried coming up with a solution yourself!


# Solution & Analysis

The main problem in the original version was not just duplication. The deeper problem was that invalid state was still easy to represent.

A `RestorationJob` could be created directly with:

* a bad catalog number
* an empty title
* invalid humidity
* a negative page count
* etc

That meant the service was doing some validation, but the model itself was still weak.

## What changed

The solution (see `solution.py`) strengthens the model in two ways. First, it replaces dangerous primitives with explicit domain concepts:

* CatalogNumber
* HumidityPercent
* FragilePageCount
* ...

These types enforce their own rules when they are created. That means invalid values fail early instead of leaking deeper into the system.

Second, lifecycle transitions moved onto the model:

* `move_to_assessment`
* `start_restoration`
* `complete_job`

This makes the object responsible not only for being created in a valid state, but also for staying valid over time.

## Why this is better

The service is now simpler. It mainly orchestrates:

* converting raw input into validated domain concepts
* calculating the quote
* constructing the job

That improves:

* Domain Integrity: invalid jobs are much harder to create
* Clarity: the rules live closer to the concepts they belong to
* Resilience: changes to invariants are more localized

## What stayed outside the model

The pricing logic stayed outside the model in `calculate_restoration_quote`.

That's a good choice because the quote formula is not really part of what makes a restoration job valid. It's a policy decision that may change later without changing the meaning of a valid job.

## A trade-off

This solution wraps several primitive values in small types, which adds some extra code and some `.value` access.

The extra structure gives stronger guarantees and makes the domain rules more explicit, but you may not always need to introduce all the extra classes. As a middle ground, you could also do some of the validation checks directly in the `RestorationJob` class `__post_init__` method.