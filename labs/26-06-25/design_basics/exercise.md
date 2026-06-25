# Design Basics Exercise

The code below has the desired functionality:

```python
def apply_discount(price: float, user_type: str) -> float:
    if user_type == "premium":
        return price * 0.8
    elif user_type == "student":
        return price * 0.9
    elif user_type == "parity":
        return price * 0.75
    else:
        return price
```

However, this code is difficult to work with:

- As you add more new user types, the function keeps getting longer and harder to read.
- Adjusting discount percentages is inconvenient, because you have to search through the entire function to find the right one.

> Assignment: improve this code so that it is easier to add user types and adjust discount percentages.