> Don't read any further until you tried coming up with a solution yourself!

# Solution & Analysis

The goal of this exercise was not to eliminate errors, but to design how errors move through the system.

The original implementation hid failures by catching broad exceptions and silently skipping invalid rows. While this allowed the import to continue, it also produced incomplete datasets without making it obvious that something had gone wrong.

The refactored solution takes a different approach. It uses Pydantic to validate incoming data, translates validation failures into domain-specific exceptions, and lets those exceptions propagate to the application's boundary.

---

# 1. Using Pydantic at the Input Boundary

The first improvement is introducing a Pydantic model:

```python
class LabResultInput(BaseModel):
    ...
```

Rather than manually converting strings into `Decimal` and `date`, the importer delegates that responsibility to Pydantic.

This has several advantages:

- less parsing code
- consistent validation
- informative validation errors
- less opportunity for bugs

More importantly, it keeps the importer focused on its real responsibility: importing laboratory results.

---

# 2. Translating Validation Errors

Pydantic raises a `ValidationError` whenever input data cannot be converted.

Although this exception contains useful information, it belongs to the validation library—not to the laboratory domain.

Instead of allowing that exception to escape, the importer translates it into:

```python
InvalidLabResultError
```

This is an example of translating infrastructure or library failures into the language of your own application.

As a result, higher layers no longer depend on Pydantic.

If the validation library ever changes, only the importer needs to change.

---

# 3. Exceptions Carry Structured Context

The custom exception stores useful information about the failure:

- hospital name
- file path
- line number
- Pydantic validation errors

Instead of producing only a message such as:

```
Validation failed
```

the exception carries everything needed to understand what happened.

The application can log:

- which hospital failed
- which file failed
- which line failed
- which fields were invalid
- the values that caused the failure

This demonstrates an important design principle:

> Exception messages are for people. Exception data is for programs.

Structured exception data also makes automated logging, testing, and monitoring much easier.

---

# 4. The Importer Owns Translation

The importer catches exactly one type of exception:

```python
ValidationError
```

Its responsibility is to translate that into a domain-level failure.

Notice that the importer does **not** decide how the application should respond.

It simply reports:

> "I could not produce a valid laboratory result."

This creates a clean boundary between parsing and application behavior.

---

# 5. The Synchronizer Only Coordinates

The original implementation caught every exception inside the synchronizer.

That meant an import failure became:

```python
[]
```

which looks exactly like a successful import containing zero results.

In the refactored solution, the synchronizer no longer hides failures.

Its only responsibility is coordinating the import process.

This keeps the class focused and makes the flow of failures much easier to understand.

---

# 6. The Application Boundary Decides the Policy

The exceptions are handled in `main()`.

This is an important architectural decision.

The application boundary now decides what should happen when an import fails.

In this solution, the policy is:

- log the failure
- continue with the next hospital

A different application might instead:

- retry the import
- notify an operator
- stop the synchronization
- write the failure to a dead-letter queue

The important point is that this decision belongs at the application boundary—not inside the importer.

---

# 7. One Failure Does Not Stop Everything

Notice what happens during execution.

North Hospital fails.

The application logs the failure.

Then it immediately proceeds with South Hospital.

This demonstrates that failures can be isolated.

The system remains useful even though one external dependency produced invalid data.

This is a good example of designing for resilience.

---

# Key Takeaways

This solution illustrates several important software design principles.

- Use libraries such as Pydantic for generic validation instead of writing parsing logic yourself.
- Translate library-specific exceptions into domain-specific exceptions.
- Let custom exceptions carry structured context.
- Allow failures to propagate until they reach an appropriate application boundary.
- Keep coordinators focused on orchestration rather than error handling.
- Decide application policy at the boundary, not inside lower-level components.

Most importantly:

> Error handling is part of your architecture.

A well-designed system doesn't try to hide failures—it makes them visible, meaningful, and easy to handle.