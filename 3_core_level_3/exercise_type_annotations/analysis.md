> Don't read any further until you tried coming up with a solution yourself!


# Solution & Analysis

This exercise focuses on adding type annotations to code that uses dictionaries and functions as arguments.

The most important part is the `price_adjusters` parameter. It's not just a list of values, but a collection of functions. Each function receives:

* a rental item
* the current subtotal

and returns the adjusted subtotal.

That means we can describe it with a callable type.

```python
type RentalItem = dict[str, Any]
type PriceAdjuster = Callable[[RentalItem, float], float]
```

`PriceAdjuster` describes the shape of the pricing functions:

```python
def weekend_discount(item: RentalItem, subtotal: float) -> float:
```

The `price_adjusters` argument is typed as an `Iterable[PriceAdjuster]`, not a `list[PriceAdjuster]`.

```python
def calculate_total(
    self,
    price_adjusters: Iterable[PriceAdjuster],
    include_insurance: bool,
) -> float:
```

This is intentional. The method only loops over the adjusters. It does not need indexing, sorting, or mutation. So `Iterable` is the more flexible input type.

The return type is `float`, because `calculate_total` returns a specific numeric result.

Note that the solution in `solution.py` is not perfect in terms of domain modeling. `RentalItem` is a dictionary, so it allows for any type of value to be stored under any key, which may lead to problem in a production environment. An improvement could be to replace that dictionary with a dataclass.