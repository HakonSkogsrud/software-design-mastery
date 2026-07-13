> Don't read any further until you tried coming up with a solution yourself!

# Solution & Analysis

There are two different design pressures in this exercise, and they lead to two different abstractions.

The first pressure is **decoupling the consumer**. The `summarize_document()` function doesn't care whether a document comes from a PDF, a Word file, or Google Docs. It only needs an object that can load a document. That is exactly what a **Protocol** expresses.

```python
class DocumentLoader(Protocol):
    def load_document(self) -> Document: ...
    def document_type(self) -> str: ...
```

Notice that the protocol is intentionally small. It only contains the behavior the consumer actually uses. Methods such as `read_file()` or `parse_document()` are implementation details and therefore do not belong in the protocol.

This is an example of **Alignment** from the CARDS framework: dependencies point toward the behavior the application requires, not toward implementation details.

---

The second pressure is **removing duplication**.

The PDF and Word loaders follow almost exactly the same process:

1. Read the file.
2. Parse the file.
3. Return a `Document`.

Instead of repeating that workflow in every subclass, we move it into an abstract base class.

```python
class FileDocumentLoader(ABC):
    def load_document(self) -> Document:
        raw_data = self.read_file()
        return self.parse_document(raw_data)
```

Each subclass now only implements the part that actually varies:

- how to parse a PDF;
- how to parse a Word document.

This makes the hierarchy meaningful. The subclasses genuinely belong to the same family because they share both behavior and workflow.

---

An important design decision is **not** putting `GoogleDocsLoader` into this hierarchy.

At first glance, it might seem similar—it also produces a `Document`. But its workflow is fundamentally different.

Instead of reading a local file, it downloads a document through an API.

Forcing it to inherit from `FileDocumentLoader` would make the hierarchy misleading. The base class would no longer represent a coherent family of implementations.

Instead, `GoogleDocsLoader` simply satisfies the `DocumentLoader` protocol.

This is a good example of the difference between the two abstractions:

- **Protocols describe capabilities.**
- **ABCs define families.**

---

Another important observation is that the protocol and the abstract base class solve different problems.

The protocol exists because the **consumer** needs an abstraction.

The abstract base class exists because the **implementations** benefit from shared behavior.

These are independent decisions. A protocol does not automatically imply an abstract base class, and an abstract base class does not automatically imply a protocol.

---

Finally, notice that we didn't introduce abstractions everywhere.

The `Document` dataclass remains a simple data object.

Small helper functions, if we had any, would simply stay functions.

Good software design is not about maximizing abstraction. It is about introducing exactly enough structure to reduce coupling and eliminate duplication, while keeping the design as simple as possible.

## CARDS Summary

- **Clarity:** The responsibilities of consumers and implementations are clearly separated.
- **Alignment:** The application depends on a `DocumentLoader`, not on concrete loader classes.
- **Resilience:** New file-based loaders can reuse the existing workflow, while unrelated loaders are free to evolve independently.
- **Separation:** File-loading logic, API-loading logic, and document summarization remain isolated from one another.
