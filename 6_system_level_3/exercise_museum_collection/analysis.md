> Don't read any further until you tried coming up with a solution yourself!

# Solution & Analysis

This one does not have a single correct answer. The goal is to identify where event-driven architecture actually improves the design.

The key question you should ask yourself throughout the exercise is whether an operation is part of the core business transaction, or a response to a completed business action?

That distinction determines whether a direct function call or an event is the better choice.

Let's go over the use cases.

# `acquire_artwork()`

A typical solution might look like this.

### Keep as direct calls

- Store the artwork.
- Assign an inventory number.

These operations define what it means to successfully acquire an artwork.

If assigning an inventory number fails, the acquisition itself should probably fail.

These steps belong inside the core workflow.

### Good candidates for events

- Update collection statistics.
- Notify the conservation team.
- Publish the acquisition to the public website.

These are independent reactions.

The artwork has already been acquired.

If one of these follow-up actions changes in the future, we would prefer to add or modify an event handler rather than changing the acquisition workflow itself.

# `schedule_exhibition()`

### Keep as direct calls

- Reserve gallery space.
- Assign artworks.
- Verify that artworks are not double-booked.

These operations are tightly coupled.

Scheduling an exhibition is only successful if all of them succeed together.

Turning them into separate event handlers would introduce unnecessary complexity and could leave the system in an inconsistent state.

This use case probably does **not** benefit much from events.

# `loan_artwork()`

### Keep as direct calls

- Record the loan.
- Update artwork availability.

These represent the business transaction itself. If availability is not updated, the loan should not succeed.

### Good candidates for events

- Email the borrowing institution.
- Notify the insurance provider.
- Update the public collection catalogue.

Each of these is an independent reaction.

If another integration is added later—for example notifying a transportation company—we can simply subscribe another handler to an `ArtworkLoaned` event without modifying the existing use case.

# `generate_collection_report()`

### Keep as direct calls

- Build the report.

Everything else happens because the report now exists.

### Good candidates for events

- Cache the report.
- Email curators.
- Record reporting metrics.

These operations are loosely coupled.

Different organizations may choose different reporting mechanisms without affecting report generation itself.

# Looking for Business Events

One useful way to approach these decisions is to look for completed business actions. For example:

- `ArtworkAcquired`
- `ArtworkLoaned`
- `CollectionReportGenerated`

Notice that these describe something that happened.

They do not describe implementation details.

Avoid names like `SendEmail`, `UpdateCache`, or `KafkaArtworkMessage`. Remember that domain events should express business meaning.

# Immediate Consistency Matters

One of the biggest mistakes with event-driven architecture is assuming that every follow-up action should become an event. Some operations still belong together. For example:

- assigning an inventory number during acquisition
- verifying gallery availability while scheduling an exhibition
- updating artwork availability when recording a loan

These operations form one business transaction.

Separating them into independent event handlers would make the workflow harder to understand and could introduce consistency problems.

# Independent Reactions Are Better Candidates

In contrast, notifications, analytics, reporting, and external integrations usually evolve independently. Those are exactly the kinds of responsibilities that benefit from events.

Over time, organizations often ask for:

- another notification,
- another integration,
- another dashboard,
- another analytics system.

With direct calls, every new requirement modifies the existing workflow. With events, many of those changes become additions rather than modifications.

# Key Takeaways

- Keep operations that define the business transaction inside the use case.
- Move independent reactions into event handlers.
- Name events after business facts, not infrastructure.
- Introduce events where responsibilities are likely to evolve independently.
- Avoid turning every function call into an event.
