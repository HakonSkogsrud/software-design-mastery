> Don't read any further until you tried coming up with a solution yourself!


# Solution & Analysis

The original implementation works, but `PricingService` depends on more information than it actually needs.

The main issue is that the service receives the entire `RentalRequest` object. While this is convenient, pricing only uses a small subset of the request’s fields. Customer information, notification preferences, and other request details are irrelevant to the pricing calculation.

This creates stamp coupling: one component depends on a large object even though it only needs part of it. The risk is that the dependency surface becomes wider than necessary. As `RentalRequest` grows over time, `PricingService` becomes indirectly coupled to changes that have nothing to do with pricing.

In the solution, the pricing service is refactored to depend only on the inputs that influence the price calculation. The service still receives the `Equipment` object because equipment is a meaningful part of the pricing domain. However, pricing-specific values such as rental duration, loyalty tier, and insurance choice are passed explicitly.

This change improves Alignment because the dependencies now match the responsibility of the service more closely. It also improves Resilience because unrelated changes to RentalRequest are less likely to affect pricing logic.

A useful rule of thumb is:

Pass objects when the object itself belongs to the receiver’s responsibility. Pass individual values when only a narrow slice of information is needed.

This does not mean objects should never be passed around. In this case, `Equipment` remains a reasonable dependency because pricing genuinely depends on equipment characteristics. The goal is not to eliminate coupling, but to make it intentional.

See `solution.py` for one possible implementation. Other solutions are possible as long as they reduce the dependency surface and keep pricing focused on pricing-related information.