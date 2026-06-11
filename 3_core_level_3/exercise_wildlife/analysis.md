> Don't read any further until you tried coming up with a solution yourself!


# Solution & Analysis

This solution protects the `Mission` model by making the intended usage clearer and by moving important rules into the domain object itself.

The original version allowed callers to create a mission in any status and then freely change important fields afterward. That meant the lifecycle rules were mostly based on discipline: developers had to remember what was allowed.

In `solution.py`, mission creation now goes through `Mission.create(...)`. This makes the initial state explicit: every new mission starts as `PLANNED`. Callers no longer choose the starting status themselves.

The solution also moves lifecycle changes into named methods:

* `start()`
* `complete()`
* `cancel()`

Each method checks whether the transition is valid before changing the mission status. For example, only a planned mission can be started, and only an active mission can be completed. This keeps the lifecycle rules in one place.

Important fields such as `_status`, `_tracker_id`, and `_estimated_cost` are stored as internal fields. They are still technically accessible in Python, but the leading underscore signals that they should not be changed directly. Public read-only properties expose the values that other code needs:

* `status`
* `tracker_id`
* `estimated_cost`

The tracker can still be changed, but only through `assign_tracker(...)`. That method enforces the rule that the tracker may only be changed while the mission is still planned. Once the mission has started, completed, or been cancelled, changing the tracker is no longer allowed.

Validation is also kept inside the model. The mission checks that the species is not empty, the number of tracking days is valid, the tracker id is not empty, and the estimated cost is not negative. The same tracker validation is repeated in `assign_tracker(...)`, because that method introduces a new value after construction.

The main design improvement is that the correct path is now obvious:

* create the mission with `Mission.create(...)`
* change its lifecycle with methods
* read state through properties

The incorrect path is still possible in Python, but it now looks suspicious because it requires reaching into internal fields directly.

This is the core idea of a protected domain model in Python: not making misuse impossible, but making valid usage clear and invalid usage harder to write accidentally.