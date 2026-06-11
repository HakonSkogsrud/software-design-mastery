> Don't read any further until you tried coming up with a solution yourself!


# Solution & Analysis

The original code has two related design problems.

First, both functions know what counts as a long rental. The condition is not duplicated in exactly the same context, but the business rule is still duplicated. If the threshold changes from 300 minutes to 240 minutes, both functions need to be updated. That weakens Resilience because a small policy change can easily become inconsistent.

Second, both functions are responsible for finding a scooter and handling the missing-scooter case. That makes the functions do more than their names suggest. `generate_customer_invoice()` should generate an invoice. `estimate_maintenance_credit()` should estimate a credit. Looking up scooters is a separate responsibility.

In `solution.py`, the refactor keeps the design intentionally small. The long-rental rule is extracted into a named function, which improves Clarity and removes the risky duplication. The scooter lookup is moved out of the business functions, so those functions now receive the scooter they operate on. This makes them easier to read, easier to test, and less coupled to the global scooter list.

The solution improves Clarity because each function has a more focused responsibility. It improves Resilience because the long-rental threshold now lives in one place. It also improves Separation slightly because lookup logic is separated from invoice and maintenance-credit logic.

The trade-off is that the caller now has a little more responsibility. It must find the scooter before calling the business functions. That is acceptable here because it makes the boundary between lookup and calculation clearer.

A larger abstraction such as a `RentalPolicy`, `PricingStrategy`, or `ScooterService` would probably be premature. The system has only one shared rule and two simple operations. Adding more structure now would reduce Clarity without enough benefit. This is where YAGNI matters: improve the design where there are real problems, but do not design a complicated system if that's not really necessary.