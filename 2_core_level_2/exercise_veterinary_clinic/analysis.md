> Don't read any further until you tried coming up with a solution yourself!


# Solution & Analysis

The original implementation stores animals and appointments in module-level variables. This means the application’s state is shared globally and accessed directly by the service.

While this works for a small example, it creates global coupling. `AppointmentService` knows exactly where data is stored and how it is retrieved. If the storage mechanism changes, the service will likely need to change as well.

This weakens Resilience because storage-related changes can ripple into business logic. It also weakens Separation because the service is responsible for both appointment scheduling and interacting directly with application state.

In the solution, the storage concerns are moved into an `AppointmentRepository`. The service no longer reads from global variables or appends directly to a shared list. Instead, it collaborates with a repository through a small set of focused methods.

This changes the dependency structure in an important way:

* Before, the service depended on global state.
* After, the service depends on a repository abstraction.

The service still depends on storage, but the dependency is now explicit and localized. This is an example of intentional coupling. We have not removed the dependency; we have given it a clearer shape.

An additional benefit is that storage decisions become easier to change. If the clinic later decides to store appointments in a database, a file, or an external system, most of those changes can be isolated to the repository. The appointment scheduling logic can remain largely unchanged.

This refactoring improves:

* Resilience because storage changes are less likely to affect business logic.
* Separation because persistence concerns are isolated from appointment scheduling.
* Alignment because each component now has a more focused responsibility.

See `solution.py` for a possible implementation. The important goal is not the specific repository implementation, but the shift from shared global state to a dedicated component that owns storage responsibilities.