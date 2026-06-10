> Don't read any further until you tried coming up with a solution yourself!


# Solution & Analysis

Let's analyse this exercise. Note that this is not the only correct answer. The goal is to practice reasoning about design forces using CARDS.

## Weakest CARD

The weakest CARD is probably *Resilience*.

The function works today, but it is not resilient to change. It mixes several decisions in one place:

* deciding whether the plant needs water
* deciding how much water to use
* creating a watering event
* storing the event
* printing output
* notifying the owner

So when the watering rules change, the function itself must change.

## What Changes When the New Requirement Arrives?

The new requirement sounds like just one more rule, but it affects several parts of the function.

You now need to change watering decision logic. The function must check both moisture level and weather forecast. So watering no longer depends only on `moisture_level`.

The event probably needs to record whether watering happened or was skipped. For example:

```python
{
    "plant_name": plant_name,
    "water_amount": 0,
    "moisture_level": moisture_level,
    "status": "skipped",
    "reason": "rain expected",
}
```

The notification can no longer just say "Sending notification for Basil". It now needs to explain the decision. So notification logic also changes.

This is a clear example of change amplification. One requirement affects:

* the watering rule
* the event structure
* the notification message
* possibly future reports based on watering history

The original code works, but the change does not stay local. That is weak Resilience.

## Other Affected CARDS

### Clarity

The function is called water_plant, but after the new requirement it may sometimes not water the plant. That name becomes less accurate.

A clearer name might be `handle_watering` or `process_watering_decision`.

This clarifies that the function is now about making a decision, not always performing an action.

### Separation

Separation is also affected.

The function mixes decision-making, state recording, output and notifications. Those responsibilities may need to evolve independently.

### Domain Integrity

There is also a possible Domain Integrity issue. For example, the code allows a completed watering event with 0 liters, which doesn't make a lot of sense (at least, my plants are not happy when I water them that way ;) ).


## A Reasonable Improvement

A simple first improvement is to extract the watering decision.

For example:

```python
def determine_water_amount(moisture_level, rain_expected):
    if rain_expected:
        return 0
    if moisture_level < 15:
        return 4
    if moisture_level < 30:
        return 2
    return 0
```

Then the main function can use that decision:

```python
rain_expected = weather_forecast["rain_expected_next_24h"]
water_amount = determine_water_amount(moisture_level, rain_expected)
```

This is not a perfect final design, but it improves the structure.

## Which CARDS Improve?

Resilience improves because watering-rule changes are now more local. For example, if the threshold changes from 30 to 35, or if rain rules become more detailed, the change mostly belongs in determine_water_amount.

Clarity also improves. The main function becomes easier to read because the decision has a name:

```python
determine_water_amount(...)
```

That name communicates intent better than a group of nested conditions.

Separation improves (slightly). The decision logic is separated from event recording and notification.

A even stronger version would return a decision object or dictionary, not just a number.

This gives the rest of the system a clearer decision to work with.

## Common Answers

"I would add another if statement"

That works, but it probably keeps the same structural problem. The code may become correct, but not more maintainable.

"I would extract the notification code"

That can help Separation, but it does not address the core issue: the watering decision is growing. It is a useful improvement, but not the most important first move.

"I would create a class"

That might be reasonable later, but it may be too much for the first step. A class only helps if it gives responsibilities a better home. Simply putting the same logic inside a class does not automatically improve the design.

## Key Takeaway

The original function works, but the problem is that a small rule change spreads through the function.

A good first refactoring does not need to be large. It should make one kind of future change easier and safer. Do things step-by-step!