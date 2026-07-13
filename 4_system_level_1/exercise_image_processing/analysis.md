> Don't read any further until you tried coming up with a solution yourself!

# Solution & Analysis

## Overview

There is no single correct solution to this exercise.

The important part is **how** the design evolves as new pressures appear.

A reasonable progression is:

```text
plain function
→ configured function
→ composed functions
→ stateful processor
→ retry policy
→ concurrent orchestration
```

The goal is **not** to end with a class.

The goal is to introduce a class only when the problem contains state that needs a clear owner.

---

# Starting Point — A Plain Function

The initial requirement is simple:

> Resize an image to a requested width and height.

```python
def resize_image(
    image: Image,
    width: int,
    height: int,
) -> Image:
    ...
```

A function is appropriate because:

- the operation is stateless
- the result depends only on its inputs
- there is no lifecycle
- there are no invariants to maintain

Introducing a class here would only add unnecessary structure.

---

# Requirement 1 — Standard Dimensions

Almost every image should be resized to **1200×800**.

Soon the call sites begin to look like this:

```python
resize_image(
    image,
    width=1200,
    height=800,
)
```

repeated throughout the codebase.

Rather than introducing a class, we can configure the existing function.

```python
resize_for_website = partial(
    resize_image,
    width=1200,
    height=800,
)
```

Usage becomes:

```python
resized = resize_for_website(image)
```

## Why this design?

Nothing about the problem has become stateful.

We simply want to avoid repeating configuration.

`partial()` lets us do exactly that while keeping the API small and explicit.

---

# Requirement 2 — Add a Watermark

Images now need a watermark.

Rather than extending `resize_image()`, we create another focused function.

```python
def add_watermark(
    image: Image,
    watermark: str,
) -> Image:
    ...
```

The workflow becomes:

```python
resized = resize_for_website(image)
result = add_watermark(
    resized,
    watermark,
)
```

## Why separate the functions?

Resizing and watermarking solve different problems.

Keeping them independent makes them:

- easier to test
- easier to reuse
- easier to replace

Instead of combining responsibilities, we compose them.

This supports **Separation** in CARDS.

---

# Requirement 3 — Hotel-Specific Watermarks

Each hotel always uses the same logo.

Rather than passing the watermark every time, we can create a configured processor.

A closure works well here.

```python
def create_image_processor(
    watermark: str,
):
    def process(image: Image) -> Image:
        resized = resize_for_website(image)

        return add_watermark(
            resized,
            watermark,
        )

    return process
```

Usage:

```python
process_amsterdam_image = create_image_processor(
    "amsterdam-logo.png",
)

result = process_amsterdam_image(image)
```

## Why a closure?

We now have shared configuration.

But we still do **not** have mutable state.

A closure groups configuration with behavior without introducing an object lifecycle.

A class would work, but it has not yet earned its complexity.

---

# Requirement 4 — Processing Statistics

The system now tracks:

- processed images
- failed images
- cache hits

This is the first requirement that introduces **persistent mutable state**.

That state needs an owner.

A class now becomes appropriate.

```python
class ImageProcessor:
    def __init__(
        self,
        watermark: str,
    ) -> None:
        self._watermark = watermark
        self._statistics = ProcessingStatistics()

    @property
    def statistics(self) -> ProcessingStatistics:
        return self._statistics
```

## Why does the class make sense now?

The processor owns data that changes over time.

It is responsible for keeping that data consistent.

This is exactly the kind of responsibility classes are designed for.

---

# Requirement 5 — Cache Processed Images

Repeated processing is expensive.

The processor now stores previous results.

The cache is owned by the processor because it depends on:

- image
- dimensions
- watermark

However, the implementation details should not clutter the public workflow.

Instead of embedding everything inside `process()`, we extract private helper methods.

```python
class ImageProcessor:
    ...

    def _cache_key(
        self,
        image: Image,
    ) -> CacheKey:
        ...

    def _get_cached(
        self,
        image: Image,
    ) -> Image | None:
        ...

    def _store_in_cache(
        self,
        image: Image,
        result: Image,
    ) -> None:
        ...
```

The processing workflow now reads much more clearly:

```python
def process(
    self,
    image: Image,
) -> Image:
    cached = self._get_cached(image)

    if cached is not None:
        return cached

    result = self._process_once(image)

    self._store_in_cache(
        image,
        result,
    )

    self._statistics.processed += 1

    return result
```

## Why is this better?

The processor still owns the cache.

But the workflow now communicates **what** happens instead of **how** it happens.

Private helper methods hide implementation details without introducing another abstraction.

Only when caching develops its own behavior—for example expiration policies, Redis integration, or eviction strategies—would introducing a dedicated cache object become worthwhile.

---

# Requirement 6 — Retry Failed Operations

Processing occasionally fails.

Retrying is **not** an image-processing concern.

It is an execution policy.

Rather than embedding retry loops inside the processing logic, we extract the retry behavior.

```python
result = retry(
    lambda: self._process_once(image),
    attempts=3,
)
```

## Why keep retry separate?

Retry behavior changes independently.

Future requirements might include:

- exponential backoff
- delays
- logging
- exception filtering

Keeping retry separate prevents those concerns from spreading throughout the processor.

This strengthens **Separation** and **Resilience**.

---

# Requirement 7 — Concurrent Processing

The system should process many images simultaneously.

Notice that the image transformations themselves do **not** need to become asynchronous.

Instead, concurrency can be introduced at the orchestration layer.

```python
results = await process_images(
    processor,
    images,
)
```

The processor itself remains focused on processing a single image.

## New design pressure

The processor now owns shared mutable state:

- statistics
- cache

If multiple threads use the same processor simultaneously, updates may no longer be safe.

Possible solutions include:

- locks
- thread-safe caches
- separate processor instances
- moving shared state elsewhere

Exactly which solution is best depends on the deployment environment.

The important insight is that concurrency introduces new pressures without necessarily changing the public API.

---

# Final Design

The final design combines several different abstractions.

Functions perform transformations:

```text
resize_image()
add_watermark()
```

A configured function captures repeated configuration:

```text
resize_for_website
```

A class owns persistent state:

```text
ImageProcessor
```

A retry function encapsulates execution policy:

```text
retry(...)
```

An asynchronous workflow coordinates multiple processing operations.

Each abstraction is introduced only when the problem requires it.

---

# CARDS Analysis

## Clarity

Each abstraction has one obvious responsibility.

The processing workflow is easy to read:

```text
check cache
→ process
→ store result
→ update statistics
```

---

## Alignment

Dependencies point toward meaningful concepts.

The processor coordinates image processing.

Retry logic remains an independent policy.

Image transformations remain standalone functions.

---

## Resilience

Each concern can evolve independently.

For example:

- changing retry behavior does not affect resizing
- changing watermarking does not affect caching
- changing caching does not affect concurrency

Small changes remain small.

---

## Domain Integrity

The immutable `Image` model prevents accidental mutation.

The processor owns its cache and statistics, preventing unrelated code from modifying them directly.

---

## Separation

The design separates:

- image transformations
- shared configuration
- state ownership
- retry policy
- workflow orchestration

Each concern remains focused and composable.

---

# Key Takeaway

Notice how the design evolved.

We did **not** begin with a large `ImageProcessor` class.

Instead, we started with a simple function.

Only when the problem introduced persistent state—statistics and caching—did a class become the right abstraction.

This is the central lesson of this exercise: choose the simplest abstraction that matches the current design pressure.

Don't optimize for imagined future requirements.

Let the structure evolve together with the system.