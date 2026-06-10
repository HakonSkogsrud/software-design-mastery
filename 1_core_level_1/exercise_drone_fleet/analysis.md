> Don't read any further until you tried coming up with a solution yourself!


# Solution & Analysis

The main issue is that schedule_battery_replacement knows too much about the internal structure of a drone.

It reaches through:

```python
drone["hardware"]["battery"]["health"]
drone["hardware"]["battery"]["cycles"]
drone["mission"]["status"]
```

That creates several forms of coupling.

First, there is stamp coupling. The function receives the entire drone structure, even though it only needs to know whether the drone is eligible for battery replacement.

Second, there is content coupling through deep dictionary navigation. The function depends on the exact shape of the nested data. If hardware is renamed, if battery moves somewhere else, or if mission["status"] becomes a more complex object, this function breaks.

Third, this violates the Law of Demeter. The function is not just talking to a drone. It is reaching into the drone’s hardware, then into its battery, then into individual battery fields.

That weakens Clarity, because the function mixes scheduling with battery and mission rules.

It also weakens Alignment, because the dependency points past the drone and into its internal representation.

And it weakens Resilience, because small internal data changes can break external code.

A better design is to give the drone object behavior that answers the question directly. And at the same type, you can move away from the fragile dictionary structure and introduce a few helpful dataclasses (see the `solution.py` file for an example of what that might look like).

Now the scheduling function no longer depends on nested dictionary keys. It simply asks the drone a question:

```python
drone.can_schedule_battery_replacement()
```

This improves Clarity, because the condition now expresses business intent.

It improves Alignment, because battery rules live with Battery, mission rules live with Mission, and scheduling only coordinates the decision.

It improves Resilience, because the internal structure of Battery or Mission can change without forcing changes in the scheduling function.